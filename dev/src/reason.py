"""
Stage 4: Evidence reasoning (stance classification).

Labels each retrieved chunk against a claim as support / contradict /
unrelated. Unrelated chunks get dropped here, not averaged in later
(Section 4.1: "a meeting note that mentions discounts in passing is not
evidence about the 15% threshold").

This ships a heuristic baseline (lexical overlap + negation/contrast
cues) so the pipeline runs end-to-end with no model download required.
It is intentionally weak -- the proposal's own plan is to compare this
against a small NLI model and a constrained LLM prompt on a hand-labelled
set (Section 2.1, "Evidence reasoning"), not to ship this heuristic as
the final answer.

Owner (per the Group Charter): Rohan Chaudhary (Evidence Linking & Retrieval Lead),
jointly with whoever runs the NLI/LLM comparison.
"""

from __future__ import annotations

import re
from typing import Tuple

from .retrieve import tokenize

NEGATION_CUES = {
    "not", "no", "never", "isn't", "wasn't", "cannot", "can't", "won't",
    "however", "except", "unless", "instead", "bypass", "skip", "skipped",
    "without", "workaround", "informally", "verbally", "no longer", "overrid",
}

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "to", "of", "and",
    "or", "for", "in", "on", "at", "by", "with", "as", "that", "this",
    "it", "its", "if", "must", "shall", "may", "will", "has", "have",
}


def _content_tokens(text: str) -> set:
    return {t for t in tokenize(text) if t not in STOPWORDS and len(t) > 2}


def classify_stance(claim_text: str, evidence_text: str) -> Tuple[str, float]:
    """
    Return (stance, confidence). stance is one of
    "support" / "contradict" / "unrelated".

    Heuristic: score lexical overlap between claim and evidence as a
    proxy for relatedness; if related, look for negation/contrast cues
    near the overlapping terms to guess contradiction vs. support.
    This is a placeholder for a real NLI model -- see module docstring.
    """
    claim_tokens = _content_tokens(claim_text)
    evidence_tokens = _content_tokens(evidence_text)
    if not claim_tokens:
        return "unrelated", 0.0

    overlap = claim_tokens & evidence_tokens
    overlap_ratio = len(overlap) / max(1, len(claim_tokens))

    if overlap_ratio < 0.15:
        return "unrelated", round(1 - overlap_ratio, 2)

    evidence_lower = evidence_text.lower()
    has_negation = any(cue in evidence_lower for cue in NEGATION_CUES)

    if has_negation:
        # weak signal: related + a contrast/negation cue nearby -> guess contradiction
        return "contradict", round(min(0.4 + overlap_ratio, 0.75), 2)

    return "support", round(min(0.4 + overlap_ratio, 0.8), 2)


def reason_over_hits(claim_text: str, hits) -> list:
    """
    hits: list of retrieve.RetrievalHit
    Returns list of dicts with stance/stance_confidence attached,
    unrelated hits filtered out.
    """
    reasoned = []
    for h in hits:
        stance, conf = classify_stance(claim_text, h.text)
        if stance == "unrelated":
            continue
        reasoned.append({
            "chunk_id": h.chunk_id,
            "doc_id": h.doc_id,
            "source_type": h.source_type,
            "retrieval_score": h.score,
            "stance": stance,
            "stance_confidence": conf,
            "text": h.text,
        })
    return reasoned
