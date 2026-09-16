"""Load Northfield stores and run the eight-stage credibility pipeline."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "data" / "outputs"
GOLD_PATH = ROOT / "data" / "gold" / "gold_claims.json"

from src.schema import Chunk, Document, read_jsonl
from src.retrieve import BM25Retriever, tokenize
from src.reason import classify_stance, reason_over_hits
from src.weight import apply_weights, AUTHORITY_WEIGHTS
from src.score import score_claim
from src.explain import explain_template
from src.extract import extract_claims_rule_based
from src.calibrate import enough_labels_to_calibrate
from src.evaluate import recall_at_k


def load_chunks() -> list[Chunk]:
    rows = read_jsonl(str(OUTPUTS / "chunks.jsonl"))
    return [Chunk(**{k: v for k, v in r.items() if k in Chunk.__dataclass_fields__}) for r in rows]


def load_documents() -> list[Document]:
    rows = read_jsonl(str(OUTPUTS / "documents.jsonl"))
    return [Document(**{k: v for k, v in r.items() if k in Document.__dataclass_fields__}) for r in rows]


def load_roster() -> list[dict]:
    path = OUTPUTS / "roster.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "people" in data:
        return data["people"]
    if isinstance(data, list):
        return data
    return []


def load_gold() -> dict:
    return json.loads(GOLD_PATH.read_text())


def corpus_profile(chunks: list[Chunk], documents: list[Document], roster: list[dict]) -> dict:
    chunk_types = Counter(c.source_type for c in chunks)
    doc_types = Counter(d.source_type for d in documents)
    phases = Counter(c.phase for c in chunks)
    superseded = sum(1 for c in chunks if c.metadata.get("superseded"))
    return {
        "chunk_count": len(chunks),
        "document_count": len(documents),
        "roster_count": len(roster),
        "chunk_types": dict(chunk_types),
        "doc_types": dict(doc_types),
        "phases": dict(phases),
        "superseded_chunks": superseded,
        "assessment_date": "2026-07-31",
        "company": "Northfield Software Ltd",
        "partner": "Decidr",
        "group": "iLab 14-01",
    }


def build_retriever(chunks: list[Chunk]) -> BM25Retriever:
    return BM25Retriever(chunks)


def candidate_claims(chunks: list[Chunk], limit: int = 40) -> tuple[list[dict], int]:
    claims = extract_claims_rule_based(chunks)
    out = []
    for c in claims[:limit]:
        out.append(asdict(c) if hasattr(c, "__dataclass_fields__") else c)
    return out, len(claims)


def run_claim(
    claim_text: str,
    claim_id: str,
    retriever: BM25Retriever,
    chunks: list[Chunk],
    top_k: int = 15,
    prior: float = 0.5,
    method: str = "bayesian",
) -> dict[str, Any]:
    hits = retriever.search(claim_text, top_k=top_k)
    hit_rows = []
    for h in hits:
        stance, conf = classify_stance(claim_text, h.text)
        hit_rows.append(
            {
                "chunk_id": h.chunk_id,
                "doc_id": h.doc_id,
                "source_type": h.source_type,
                "retrieval_score": round(float(h.score), 4),
                "stance": stance,
                "stance_confidence": conf,
                "text": h.text,
                "kept": stance != "unrelated",
            }
        )

    reasoned = reason_over_hits(claim_text, hits)
    superseded_lookup = {c.doc_id: bool(c.metadata.get("superseded", False)) for c in chunks}
    weighted = apply_weights(reasoned, superseded_lookup=superseded_lookup)
    scored = score_claim(weighted, prior=prior, method=method)
    explanation = explain_template(claim_text, scored, weighted)

    return {
        "claim_id": claim_id,
        "claim_text": claim_text,
        "method": method,
        "prior": prior,
        "top_k": top_k,
        "query_tokens": tokenize(claim_text),
        "hits": hit_rows,
        "weighted": weighted,
        "scored": scored,
        "explanation": explanation,
        "n_retrieved": len(hits),
        "n_kept": len(weighted),
        "n_dropped": len(hits) - len(weighted),
        "calibration": enough_labels_to_calibrate(4)[1],
    }


def evaluate_gold(retriever: BM25Retriever, chunks: list[Chunk], top_k: int = 15) -> list[dict]:
    gold = load_gold()
    rows = []
    for item in gold["claims"]:
        expected = item["expected_supporting_doc_ids"] + item.get(
            "expected_contradicting_or_caveat_doc_ids", []
        )
        recall = recall_at_k(retriever, item["claim_text"], expected, top_k=top_k)
        result = run_claim(
            item["claim_text"], item["claim_id"], retriever, chunks, top_k=top_k
        )
        rows.append(
            {
                "claim_id": item["claim_id"],
                "layer": item.get("layer"),
                "process": item.get("process"),
                "claim_text": item["claim_text"],
                "expected_status": item.get("expected_status"),
                "actual_status": result["scored"]["status"],
                "score": result["scored"]["credibility_score"],
                "confidence": result["scored"]["confidence"],
                "retrieval_recall": recall,
                "match": result["scored"]["status"] == item.get("expected_status"),
                "expected_ids": expected,
                "retrieved_ids": [h["doc_id"] for h in result["hits"]],
            }
        )
    return rows


def authority_legend() -> dict:
    return dict(AUTHORITY_WEIGHTS)
