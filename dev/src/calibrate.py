"""
Stage 7: Calibration.

If the system says 80%, it should be right about four times in five on
labelled claims. This module has real, correct implementations of the
standard checks (Brier score, Expected Calibration Error, a reliability
table) -- but per the proposal (Section 4.1 and 3.3), calibration is a
planned check, not a claimed result, until a labelled set exists that is
big enough to make a reliability plot meaningful. `enough_labels_to_calibrate`
is the guard that stops the team from generating a pretty but meaningless
calibration curve off four labelled rows.

Owner (per the Group Charter): Prathamesh Nemade (Calibration & Evaluation Lead).

Run directly (once outputs/scored_claims.jsonl and gold labels exist):
    python -m src.calibrate --scored outputs/scored_claims.jsonl --gold data/gold_claims.json
"""

from __future__ import annotations

import argparse
import json
from typing import List, Tuple

MIN_LABELLED_CLAIMS = 30   # below this, a reliability diagram is decoration, not evidence


def enough_labels_to_calibrate(n_labelled: int) -> Tuple[bool, str]:
    if n_labelled < MIN_LABELLED_CLAIMS:
        return False, (
            f"Only {n_labelled} labelled claims available (need >= {MIN_LABELLED_CLAIMS}). "
            "Calibration has not been run; treat any stated confidence level as unverified."
        )
    return True, f"Calibrated on {n_labelled} labelled claims."


def brier_score(predicted_probs: List[float], outcomes: List[int]) -> float:
    """Mean squared error between predicted probability and the 0/1 outcome. Lower is better."""
    assert len(predicted_probs) == len(outcomes) and len(predicted_probs) > 0
    return round(sum((p - o) ** 2 for p, o in zip(predicted_probs, outcomes)) / len(outcomes), 4)


def expected_calibration_error(predicted_probs: List[float], outcomes: List[int],
                                n_bins: int = 10) -> float:
    """
    Standard ECE: bucket predictions into n_bins equal-width bins by
    predicted probability, compare each bin's average prediction to its
    actual positive rate, weight by bin size.
    """
    assert len(predicted_probs) == len(outcomes) and len(predicted_probs) > 0
    bins = [[] for _ in range(n_bins)]
    for p, o in zip(predicted_probs, outcomes):
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append((p, o))

    n = len(predicted_probs)
    ece = 0.0
    for bucket in bins:
        if not bucket:
            continue
        avg_pred = sum(p for p, _ in bucket) / len(bucket)
        avg_actual = sum(o for _, o in bucket) / len(bucket)
        ece += (len(bucket) / n) * abs(avg_pred - avg_actual)
    return round(ece, 4)


def reliability_table(predicted_probs: List[float], outcomes: List[int],
                       n_bins: int = 10) -> List[dict]:
    """Per-bin breakdown, useful for plotting a reliability diagram in the notebook."""
    bins = [[] for _ in range(n_bins)]
    for p, o in zip(predicted_probs, outcomes):
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append((p, o))

    table = []
    for i, bucket in enumerate(bins):
        lo, hi = i / n_bins, (i + 1) / n_bins
        if bucket:
            avg_pred = sum(p for p, _ in bucket) / len(bucket)
            avg_actual = sum(o for _, o in bucket) / len(bucket)
        else:
            avg_pred, avg_actual = None, None
        table.append({
            "bin_range": [round(lo, 2), round(hi, 2)],
            "n": len(bucket),
            "avg_predicted": avg_pred,
            "avg_actual": avg_actual,
        })
    return table


def main():
    ap = argparse.ArgumentParser(description="Calibration check (Brier score, ECE).")
    ap.add_argument("--scored", required=True, help="JSONL with credibility_score per claim_id")
    ap.add_argument("--gold", required=True, help="JSON with claim_id -> 1/0 ground-truth outcome")
    args = ap.parse_args()

    scored = [json.loads(l) for l in open(args.scored, encoding="utf-8")]
    gold = json.load(open(args.gold, encoding="utf-8"))

    pairs = [(row["credibility_score"], gold[row["claim_id"]])
             for row in scored if row["claim_id"] in gold]

    ok, msg = enough_labels_to_calibrate(len(pairs))
    print(msg)
    if not ok:
        return

    probs = [p for p, _ in pairs]
    outcomes = [o for _, o in pairs]
    print("Brier score:", brier_score(probs, outcomes))
    print("ECE:", expected_calibration_error(probs, outcomes))


if __name__ == "__main__":
    main()
