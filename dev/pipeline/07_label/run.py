#!/usr/bin/env python3
"""
Stage 7 — Label claims in the dataset with credibility verdicts.

Runs the full retrieve → reason → weight → score → explain pipeline
on gold claims and labelled sample rows, writing labelled_claims.jsonl.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services.engine import build_retriever, load_chunks, load_gold, run_claim  # noqa: E402
from src.schema import write_jsonl  # noqa: E402


def _load_sample_claims(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "claim_id": row["claim_id"],
                    "claim_text": row["reference_claim"],
                    "expected_status": row.get("reference_status"),
                    "category": row.get("claim_category"),
                    "source": "labelled_sample",
                }
            )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 7: Label claims with verdicts.")
    ap.add_argument("--top-k", type=int, default=15)
    ap.add_argument("--method", default="bayesian")
    args = ap.parse_args()

    chunks = load_chunks()
    retriever = build_retriever(chunks)
    gold = load_gold()

    claims: list[dict] = []
    for item in gold.get("claims", []):
        claims.append({**item, "source": "gold"})

    sample_path = ROOT / "data/combined/labelled_claims_sample.csv"
    if not sample_path.exists():
        sample_path = ROOT / "data/raw/phase1/northfield/labelled_claims_sample.csv"
    for row in _load_sample_claims(sample_path):
        if not any(c["claim_id"] == row["claim_id"] for c in claims):
            claims.append(row)

    labelled = []
    for item in claims:
        result = run_claim(
            item["claim_text"],
            item["claim_id"],
            retriever,
            chunks,
            top_k=args.top_k,
            method=args.method,
        )
        labelled.append(
            {
                "claim_id": item["claim_id"],
                "claim_text": item["claim_text"],
                "category": item.get("category") or item.get("process"),
                "layer": item.get("layer"),
                "expected_status": item.get("expected_status"),
                "actual_status": result["scored"]["status"],
                "credibility_score": result["scored"]["credibility_score"],
                "confidence": result["scored"]["confidence"],
                "match": result["scored"]["status"] == item.get("expected_status"),
                "explanation": result["explanation"],
                "thought_process": result.get("thought_process", []),
                "n_evidence": result["n_kept"],
            }
        )
        print(f"  {item['claim_id']}: {result['scored']['status']} (expected: {item.get('expected_status', '—')})")

    out = ROOT / "data/outputs/labelled_claims.jsonl"
    write_jsonl(str(out), labelled)

    summary = {
        "total": len(labelled),
        "matched": sum(1 for r in labelled if r.get("match")),
        "by_status": {},
    }
    for row in labelled:
        s = row["actual_status"]
        summary["by_status"][s] = summary["by_status"].get(s, 0) + 1

    summary_path = ROOT / "data/outputs/labelling_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nLabelled {len(labelled)} claims -> {out}")
    print(f"Summary -> {summary_path}")


if __name__ == "__main__":
    main()
