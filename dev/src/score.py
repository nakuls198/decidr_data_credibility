"""
Stage 6: Credibility scoring.

Combines weighted support/contradiction into a posterior credibility
score plus a status label. Two implementations, matching Section 4.1's
fallback plan exactly:

  - weighted_checklist_score(): a transparent, always-available baseline.
  - bayesian_log_odds_score(): a small, honest Bayesian update (log-odds
    form of Bayes' rule, each weighted piece of evidence nudges belief
    up or down). This is the "Bayesian update if we can specify a prior
    and likelihood without pretending to have fitted a large model"
    version the proposal describes -- not a fitted statistical model.

Status labels sit on top of the number and are not the same thing as
confidence (Section 4.1: "we can be highly confident that a claim is
conflicted").

Owner (per the Group Charter): Shreyash Narayane (Credibility Modelling Lead).
"""

from __future__ import annotations

import math
from typing import List, Dict, Any, Tuple

from .schema import STATUS_LABELS

# Minimum total weight of evidence before we're willing to call
# something other than "Not enough evidence".
MIN_EVIDENCE_WEIGHT = 0.3


def _split_support_contradict(weighted_evidence: List[Dict[str, Any]]) -> Tuple[float, float, int, int]:
    support_w = sum(e["final_weight"] for e in weighted_evidence if e["stance"] == "support")
    contradict_w = sum(e["final_weight"] for e in weighted_evidence if e["stance"] == "contradict")
    n_support = sum(1 for e in weighted_evidence if e["stance"] == "support")
    n_contradict = sum(1 for e in weighted_evidence if e["stance"] == "contradict")
    return support_w, contradict_w, n_support, n_contradict


def weighted_checklist_score(weighted_evidence: List[Dict[str, Any]]) -> float:
    """Simple, transparent baseline: weighted support share of all weighted evidence."""
    support_w, contradict_w, _, _ = _split_support_contradict(weighted_evidence)
    total = support_w + contradict_w
    if total == 0:
        return 0.5   # no signal either way
    return round(support_w / total, 4)


def bayesian_log_odds_score(weighted_evidence: List[Dict[str, Any]], prior: float = 0.5) -> float:
    """
    logit(posterior) = logit(prior) + sum(signed, weighted evidence)

    Each piece of evidence nudges the log-odds up (support) or down
    (contradict) by its final_weight. This is a lightweight stand-in for
    a fitted Bayesian model -- defensible as "a prior updated by
    evidence", not as a calibrated statistical estimate. Calibration
    (stage 7) is what tells us whether the resulting numbers can be
    trusted as probabilities.
    """
    prior = min(max(prior, 1e-6), 1 - 1e-6)
    logit = math.log(prior / (1 - prior))
    for e in weighted_evidence:
        sign = 1 if e["stance"] == "support" else -1
        logit += sign * e["final_weight"]
    posterior = 1 / (1 + math.exp(-logit))
    return round(posterior, 4)


def credible_interval(weighted_evidence: List[Dict[str, Any]], prior: float = 0.5,
                       n_resamples: int = 200) -> List[float]:
    """
    Cheap uncertainty band: bootstrap the evidence list (sample with
    replacement) and recompute the Bayesian score each time. Not a
    substitute for a properly specified posterior, but it is an honest
    way to show "how much does this score move if the evidence set
    shifts a little" without pretending to have fitted a distribution.
    """
    import random
    if not weighted_evidence:
        return [0.5, 0.5]
    scores = []
    for _ in range(n_resamples):
        sample = [random.choice(weighted_evidence) for _ in weighted_evidence]
        scores.append(bayesian_log_odds_score(sample, prior=prior))
    scores.sort()
    lo = scores[int(0.05 * len(scores))]
    hi = scores[int(0.95 * len(scores)) - 1]
    return [lo, hi]


def status_from_score(score: float, weighted_evidence: List[Dict[str, Any]]) -> str:
    support_w, contradict_w, n_support, n_contradict = _split_support_contradict(weighted_evidence)
    total_w = support_w + contradict_w

    if total_w < MIN_EVIDENCE_WEIGHT:
        return "Not enough evidence"

    # Conflicted: meaningful weight on both sides, neither dominant.
    if n_support > 0 and n_contradict > 0:
        minority_share = min(support_w, contradict_w) / total_w
        if minority_share >= 0.35:
            return "Conflicted"

    if score >= 0.75:
        return "Supported"
    if score >= 0.6:
        return "Likely"
    if score <= 0.25:
        return "Unsupported"
    if score <= 0.4:
        return "Unlikely"
    return "Conflicted"


def confidence_from_evidence(weighted_evidence: List[Dict[str, Any]]) -> str:
    """
    Confidence is separate from the score itself: it is about how much
    (and how independent) the evidence is, not which way it points.
    """
    total_w = sum(e["final_weight"] for e in weighted_evidence)
    n_independent = len({round(e["independence_weight"], 3) for e in weighted_evidence}) if weighted_evidence else 0
    if total_w >= 1.2 and len(weighted_evidence) >= 3:
        return "High"
    if total_w >= MIN_EVIDENCE_WEIGHT:
        return "Medium"
    return "Low"


def score_claim(weighted_evidence: List[Dict[str, Any]], prior: float = 0.5,
                 method: str = "bayesian") -> Dict[str, Any]:
    if method == "bayesian":
        score = bayesian_log_odds_score(weighted_evidence, prior=prior)
        ci = credible_interval(weighted_evidence, prior=prior)
    elif method == "weighted_checklist":
        score = weighted_checklist_score(weighted_evidence)
        ci = None
    else:
        raise ValueError(f"Unknown scoring method: {method}")

    status = status_from_score(score, weighted_evidence)
    confidence = confidence_from_evidence(weighted_evidence)

    support_ids = [e["chunk_id"] for e in weighted_evidence if e["stance"] == "support"]
    contradict_ids = [e["chunk_id"] for e in weighted_evidence if e["stance"] == "contradict"]

    return {
        "credibility_score": score,
        "credible_interval": ci,
        "status": status,
        "confidence": confidence,
        "supporting_evidence": support_ids,
        "contradicting_evidence": contradict_ids,
    }
