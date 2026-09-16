"""
Stage 5: Evidence weighting.

An approved in-force policy is not equal to a random Slack message
(Section 4.1). This module turns each reasoned hit into a final_weight
by combining:

  - authority_tier   : approved-formal / draft-unapproved / informal-testimony / secondhand
  - recency_weight   : mild decay for older evidence (drafts/superseded already
                        penalised via authority_tier, this is a secondary signal)
  - independence_weight : near-duplicate excerpts (e.g. the same Slack workaround
                        copied into three later messages -- see COMMS-02/03/04 in
                        the report) collapse to ONE independent source instead of
                        three, so copies don't manufacture confidence.

Owner (per the Group Charter): Shreyash Narayane (Credibility Modelling Lead).
The weights below (AUTHORITY_WEIGHTS, DUPLICATE_SIMILARITY_THRESHOLD) are the
team's stated starting assumptions from the proposal -- vary them and see
whether the final status actually moves (Section 4.1: "if the status never
moves, the weighting stage is not earning its place").
"""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import List, Dict, Any

# Starting weights per source_type, standing in for `authority_tier` until
# each piece of evidence is individually tagged approved/draft/informal.
AUTHORITY_WEIGHTS = {
    "policy": 1.0,
    "process_doc": 0.8,
    "overview": 0.75,       # decision-rights table, role descriptions, etc.
    "meeting": 0.6,
    "interview": 0.55,
    "crm": 0.5,
    "audit_log": 0.5,
    "tasks": 0.4,
    "comms": 0.35,          # Slack/email: real, but easiest to copy/repeat
    "labelled_sample": 0.5,
    "other": 0.3,
}

DRAFT_DOC_IDS = {"POL-04"}          # known DRAFT / not-in-force at time of writing
SUPERSEDED_PENALTY = 0.3            # multiplicative penalty for superseded docs
DRAFT_PENALTY = 0.5

DUPLICATE_SIMILARITY_THRESHOLD = 0.82   # excerpts at/above this ratio count as copies


def authority_tier_and_weight(source_type: str, doc_id: str, superseded: bool) -> tuple:
    base = AUTHORITY_WEIGHTS.get(source_type, 0.3)
    tier = "approved-formal" if source_type in {"policy", "process_doc"} else \
           "informal-testimony" if source_type in {"interview", "comms", "meeting"} else \
           "secondhand"

    if doc_id in DRAFT_DOC_IDS:
        tier = "draft-unapproved"
        base *= DRAFT_PENALTY
    if superseded:
        tier = "secondhand"
        base *= SUPERSEDED_PENALTY

    return tier, float(base)


def independence_weights(evidence_texts: List[str]) -> List[float]:
    """
    Given excerpt texts (same order as the evidence list), return a
    per-item weight in (0, 1]: 1.0 if the excerpt looks unique, and a
    fraction (1 / cluster size) if it closely resembles one or more
    other excerpts already seen -- so three copies of the same
    workaround count as one independent source, not three.
    """
    clusters: List[List[int]] = []   # list of index-clusters
    assigned = [-1] * len(evidence_texts)

    for i, text in enumerate(evidence_texts):
        placed = False
        for ci, cluster in enumerate(clusters):
            rep_text = evidence_texts[cluster[0]]
            ratio = SequenceMatcher(None, text.lower(), rep_text.lower()).ratio()
            if ratio >= DUPLICATE_SIMILARITY_THRESHOLD:
                cluster.append(i)
                assigned[i] = ci
                placed = True
                break
        if not placed:
            clusters.append([i])
            assigned[i] = len(clusters) - 1

    weights = [0.0] * len(evidence_texts)
    for cluster in clusters:
        w = 1.0 / len(cluster)
        for i in cluster:
            weights[i] = float(w)
    return weights


def apply_weights(reasoned_hits: List[Dict[str, Any]], superseded_lookup: Dict[str, bool] | None = None) -> List[Dict[str, Any]]:
    """
    reasoned_hits: output of reason.reason_over_hits (list of dicts with
    stance/source_type/doc_id/text already filled in).

    Adds authority_tier, recency_weight (placeholder 1.0 until real dates
    are wired through), independence_weight and final_weight in place.
    """
    superseded_lookup = superseded_lookup or {}
    texts = [h["text"] for h in reasoned_hits]
    indep_weights = independence_weights(texts)

    for h, iw in zip(reasoned_hits, indep_weights):
        superseded = superseded_lookup.get(h["doc_id"], False)
        tier, authority_w = authority_tier_and_weight(h["source_type"], h["doc_id"], superseded)
        recency_w = 1.0   # TODO: derive from evidence_date once dates are parsed in stage 1
        h["authority_tier"] = tier
        h["recency_weight"] = recency_w
        h["independence_weight"] = iw
        h["final_weight"] = float(authority_w * recency_w * iw * h.get("stance_confidence", 1.0))

    return reasoned_hits
