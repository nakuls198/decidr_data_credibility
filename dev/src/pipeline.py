"""
Orchestrator: chains stages 3-8 for one claim (ingestion and extraction
are run separately and up front -- see ingest.py / extract.py -- since
they operate on the whole pack, not one claim at a time).

    ingest (once)  ->  extract (once)  ->  [ retrieve -> reason -> weight
                                              -> score -> explain ]  per claim
                                              -> calibrate (once labels exist)

Run directly:
    python -m src.pipeline --chunks outputs/chunks.jsonl \
        --claim "New-business discounts of 15% or more need Finance approval before Closed Won" \
        --claim_id C01
"""

from __future__ import annotations

import argparse
import json
from typing import Optional

from .schema import Chunk, ScoredClaim, read_jsonl
from .retrieve import BM25Retriever
from .reason import reason_over_hits
from .weight import apply_weights
from .score import score_claim
from .explain import explain_template


def _load_chunks(path: str):
    rows = read_jsonl(path)
    return [Chunk(**{k: v for k, v in r.items() if k in Chunk.__dataclass_fields__}) for r in rows]


def run_pipeline(claim_text: str, claim_id: str, retriever: BM25Retriever,
                  top_k: int = 15, prior: float = 0.5, method: str = "bayesian") -> dict:
    """Runs stages 3 through 8 for a single claim and returns a full trail, not just a number."""

    hits = retriever.search(claim_text, top_k=top_k)
    reasoned = reason_over_hits(claim_text, hits)

    superseded_lookup = {c.doc_id: c.metadata.get("superseded", False) for c in retriever.chunks}
    weighted = apply_weights(reasoned, superseded_lookup=superseded_lookup)

    scored = score_claim(weighted, prior=prior, method=method)
    explanation = explain_template(claim_text, scored, weighted)

    result = ScoredClaim(
        claim_id=claim_id,
        claim_text=claim_text,
        credibility_score=scored["credibility_score"],
        credible_interval=scored["credible_interval"],
        status=scored["status"],
        confidence=scored["confidence"],
        supporting_evidence=scored["supporting_evidence"],
        contradicting_evidence=scored["contradicting_evidence"],
        explanation=explanation,
        calibration_note="Not run (see calibrate.py -- requires a labelled set).",
    )

    return {
        "scored_claim": result,
        "evidence_trail": weighted,   # full per-chunk detail, for debugging / the demo UI
    }


def main():
    ap = argparse.ArgumentParser(description="Run the pipeline end-to-end for one claim.")
    ap.add_argument("--chunks", default="outputs/chunks.jsonl")
    ap.add_argument("--claim", required=True)
    ap.add_argument("--claim_id", default="C-ADHOC-01")
    ap.add_argument("--top_k", type=int, default=15)
    ap.add_argument("--prior", type=float, default=0.5)
    ap.add_argument("--method", choices=["bayesian", "weighted_checklist"], default="bayesian")
    args = ap.parse_args()

    chunks = _load_chunks(args.chunks)
    retriever = BM25Retriever(chunks)

    result = run_pipeline(args.claim, args.claim_id, retriever,
                           top_k=args.top_k, prior=args.prior, method=args.method)
    sc = result["scored_claim"]

    print(f"\nClaim {sc.claim_id}: {sc.claim_text}")
    print(f"Status: {sc.status}  |  Score: {sc.credibility_score}  |  "
          f"CI: {sc.credible_interval}  |  Confidence: {sc.confidence}")
    print(f"Supporting evidence: {sc.supporting_evidence}")
    print(f"Contradicting evidence: {sc.contradicting_evidence}")
    print(f"\nExplanation:\n{sc.explanation}")


if __name__ == "__main__":
    main()
