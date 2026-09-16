"""
Evaluation harness (Prathamesh Nemade -- Calibration & Evaluation Lead).

This is NOT stage 7 (calibrate.py handles Brier score / ECE once a real
labelled set exists). This module answers the earlier, cheaper question
the proposal also commits to (Section 3.1): does retrieval actually
recover the source ids we already know are there for data/gold_claims.json?
That is the retrieval test, run before anyone trusts a probability.

Run directly:
    python -m src.evaluate --chunks outputs/chunks.jsonl --gold data/gold_claims.json
"""

from __future__ import annotations

import argparse
import json
from typing import List

from .schema import Chunk, read_jsonl
from .retrieve import BM25Retriever
from .pipeline import run_pipeline


def _load_chunks(path: str) -> List[Chunk]:
    rows = read_jsonl(path)
    return [Chunk(**{k: v for k, v in r.items() if k in Chunk.__dataclass_fields__}) for r in rows]


def recall_at_k(retriever: BM25Retriever, claim_text: str, expected_doc_ids: List[str],
                 top_k: int = 15) -> float:
    if not expected_doc_ids:
        return float("nan")
    hits = retriever.search(claim_text, top_k=top_k)
    found_doc_ids = {h.doc_id for h in hits}
    hit_count = sum(1 for d in expected_doc_ids if d in found_doc_ids)
    return float(hit_count / len(expected_doc_ids))


def run(chunks_path: str, gold_path: str, top_k: int = 15) -> None:
    chunks = _load_chunks(chunks_path)
    retriever = BM25Retriever(chunks)
    gold = json.load(open(gold_path, encoding="utf-8"))

    print(f"{'claim_id':10s} {'retrieval_recall':17s} {'status (expected -> actual)':40s}")
    print("-" * 70)

    for item in gold["claims"]:
        expected_ids = item["expected_supporting_doc_ids"] + item.get("expected_contradicting_or_caveat_doc_ids", [])
        recall = recall_at_k(retriever, item["claim_text"], expected_ids, top_k=top_k)

        result = run_pipeline(item["claim_text"], item["claim_id"], retriever, top_k=top_k)
        actual_status = result["scored_claim"].status
        expected_status = item.get("expected_status", "?")
        match = "OK" if actual_status == expected_status else "CHECK"

        print(f"{item['claim_id']:10s} {recall:<17} {expected_status:>18s} -> {actual_status:<18s} [{match}]")


def main():
    ap = argparse.ArgumentParser(description="Check retrieval recall + status agreement on gold claims.")
    ap.add_argument("--chunks", default="outputs/chunks.jsonl")
    ap.add_argument("--gold", default="data/gold_claims.json")
    ap.add_argument("--top_k", type=int, default=15)
    args = ap.parse_args()
    run(args.chunks, args.gold, args.top_k)


if __name__ == "__main__":
    main()
