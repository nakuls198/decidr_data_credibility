"""
Stage 3: Evidence retrieval.

Given a claim, find the chunks that might support or contradict it.
Ships a real, working BM25 keyword baseline (rank_bm25) -- this is the
baseline the proposal insists on beating before trusting anything fancier
(Section 4.1: "a dense index that cannot beat a keyword search on this
pack is not progress"). A semantic/embedding retriever is stubbed
alongside it as an optional add-on with a guarded import, so the module
still runs with zero extra dependencies installed.

Owner (per the Group Charter): Rohan Chaudhary (Evidence Linking & Retrieval Lead).

Run directly:
    python -m src.retrieve --chunks outputs/chunks.jsonl \
        --claim "New-business discounts of 15% or more need Finance approval" --top_k 10
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import List, Dict, Any

from rank_bm25 import BM25Okapi

from .schema import Chunk, read_jsonl

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text.lower())


@dataclass
class RetrievalHit:
    chunk_id: str
    doc_id: str
    source_type: str
    score: float
    text: str


class BM25Retriever:
    """Keyword baseline. Build once per run, query many times."""

    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self._corpus_tokens = [tokenize(c.text) for c in chunks]
        self._bm25 = BM25Okapi(self._corpus_tokens)

    def search(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        scores = self._bm25.get_scores(tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [
            RetrievalHit(
                chunk_id=self.chunks[i].chunk_id,
                doc_id=self.chunks[i].doc_id,
                source_type=self.chunks[i].source_type,
                score=float(scores[i]),
                text=self.chunks[i].text,
            )
            for i in ranked if scores[i] > 0
        ]


class SemanticRetriever:
    """
    Optional add-on. Only import sentence-transformers if this class is
    actually instantiated, so nobody is forced to install a heavy model
    just to run the BM25 baseline.

    TODO (Rohan): once BM25 recall on the known discount-chain ids
    (POL-01, PROC-02, COMMS-01..04) is measured, decide whether this is
    worth the extra dependency, per Section 3.2's retrieval question.
    """

    def __init__(self, chunks: List[Chunk], model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "pip install sentence-transformers to use SemanticRetriever"
            ) from e
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode([c.text for c in chunks], normalize_embeddings=True)

    def search(self, query: str, top_k: int = 10) -> List[RetrievalHit]:
        import numpy as np
        q = self.model.encode([query], normalize_embeddings=True)[0]
        sims = self.embeddings @ q
        ranked = np.argsort(-sims)[:top_k]
        return [
            RetrievalHit(
                chunk_id=self.chunks[i].chunk_id,
                doc_id=self.chunks[i].doc_id,
                source_type=self.chunks[i].source_type,
                score=float(sims[i]),
                text=self.chunks[i].text,
            )
            for i in ranked
        ]


def hybrid_search(bm25: BM25Retriever, query: str, top_k: int = 10,
                   semantic: "SemanticRetriever | None" = None) -> List[RetrievalHit]:
    """Merge keyword and (optional) semantic hits, de-duplicated by chunk_id, score-sorted."""
    hits: Dict[str, RetrievalHit] = {h.chunk_id: h for h in bm25.search(query, top_k)}
    if semantic is not None:
        for h in semantic.search(query, top_k):
            if h.chunk_id not in hits or h.score > hits[h.chunk_id].score:
                hits[h.chunk_id] = h
    return sorted(hits.values(), key=lambda h: h.score, reverse=True)[:top_k]


def _load_chunks(path: str) -> List[Chunk]:
    rows = read_jsonl(path)
    return [Chunk(**{k: v for k, v in r.items() if k in Chunk.__dataclass_fields__}) for r in rows]


def main():
    ap = argparse.ArgumentParser(description="Retrieve evidence chunks for a claim (BM25 baseline).")
    ap.add_argument("--chunks", default="outputs/chunks.jsonl")
    ap.add_argument("--claim", required=True)
    ap.add_argument("--top_k", type=int, default=10)
    args = ap.parse_args()

    chunks = _load_chunks(args.chunks)
    retriever = BM25Retriever(chunks)
    hits = retriever.search(args.claim, args.top_k)

    print(f"Query: {args.claim}\n")
    for h in hits:
        print(f"[{h.score:6.2f}] {h.doc_id:22s} ({h.source_type:12s}) {h.text[:100].replace(chr(10), ' ')}")


if __name__ == "__main__":
    main()
