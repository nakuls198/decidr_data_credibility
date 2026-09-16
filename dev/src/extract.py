"""
Stage 2: Claim extraction.

Turns chunks into candidate Claims: one-sentence propositions of the form
"who (a role) may/must do what, under which condition". This module
ships a rule-based baseline that needs no API key, plus a clearly marked
hook for an LLM-assisted extractor (Section 4.1 of the proposal: an LLM
may propose candidates, but every candidate still needs a role, an
action and a condition, and still needs a human pass before it is
trusted).

Owner (per the Group Charter): Nakul Sidiginamola (Claim Extraction & NLP Lead).
Treat CANDIDATE_PATTERNS and ROLE_NAMES below as a starting point, not the
final word -- they are intentionally simple so the baseline is inspectable.

Run directly:
    python -m src.extract --chunks outputs/chunks.jsonl --out outputs/claims.jsonl
"""

from __future__ import annotations

import argparse
import re
from typing import List, Optional

from .schema import Chunk, Claim, read_jsonl, write_jsonl

# Modal / obligation language that tends to mark a testable rule rather
# than narrative or background text.
MODAL_RE = re.compile(
    r"\b(must|shall|is required to|are required to|requires?|may not|"
    r"is responsible for|are responsible for|needs? to|has to|have to|"
    r"is authorised to|is authorized to)\b",
    re.IGNORECASE,
)

# A crude sentence splitter -- good enough for policy/process prose,
# which is mostly short declarative sentences and bullet points.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

# Roles worth tagging as `responsible_role` when they appear in a
# candidate sentence. Extend this from org_chart_and_roster.md.
ROLE_NAMES = [
    "Head of Finance & People Ops", "Head of Sales", "Head of Engineering",
    "Head of Customer Success & Delivery", "Head of Customer Success",
    "Product Manager", "PM", "Account Executive", "AE", "Sales",
    "Finance", "Engineering", "QA Lead", "Customer Success",
]


def candidate_sentences(text: str) -> List[str]:
    text = re.sub(r"[*_`>#-]", " ", text)          # strip common markdown noise
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]


def guess_role(sentence: str) -> Optional[str]:
    for role in ROLE_NAMES:
        if role.lower() in sentence.lower():
            return role
    return None


def guess_layer(chunk: Chunk) -> str:
    """
    Very rough first pass at the formal / practised / gap / draft / stale
    tag described in the proposal. This should be refined once real
    claim review starts -- it is deliberately conservative.
    """
    if chunk.source_type == "policy" and chunk.metadata.get("superseded"):
        return "stale"
    if chunk.doc_id.startswith("POL-04"):          # known DRAFT policy
        return "draft"
    if chunk.source_type in {"policy", "process_doc"}:
        return "formal"
    if chunk.source_type in {"interview", "meeting", "comms"}:
        return "practised"
    return "unclassified"


def extract_claims_rule_based(chunks: List[Chunk]) -> List[Claim]:
    claims: List[Claim] = []
    counter = 0
    for chunk in chunks:
        for sentence in candidate_sentences(chunk.text):
            if len(sentence.split()) < 5:
                continue
            if not MODAL_RE.search(sentence):
                continue
            counter += 1
            claims.append(Claim(
                claim_id=f"C-AUTO-{counter:04d}",
                claim_text=sentence,
                responsible_role=guess_role(sentence),
                layer=guess_layer(chunk),
                origin_doc_id=chunk.doc_id,
                origin_chunk_id=chunk.chunk_id,
                extraction_confidence=0.4,   # rule-based baseline: deliberately modest
            ))
    return claims


def extract_claims_llm(chunk: Chunk, client=None) -> List[Claim]:
    """
    TODO (Nakul): wire up an LLM call here.

    Contract to preserve: every returned Claim must still have a role,
    an action and a condition, phrased as one atomic sentence. Do not
    return "POL-01 exists" style claims -- those describe a document,
    not the organisation (see Section 3, Project Problems).
    """
    raise NotImplementedError("LLM-assisted extraction not wired up yet; use the rule-based baseline.")


def run(chunks_path: str, out_path: str) -> None:
    rows = read_jsonl(chunks_path)
    chunks = [Chunk(**{k: v for k, v in r.items() if k in Chunk.__dataclass_fields__}) for r in rows]
    claims = extract_claims_rule_based(chunks)
    write_jsonl(out_path, claims)
    print(f"{len(claims)} candidate claims extracted from {len(chunks)} chunks -> {out_path}")
    print("NOTE: these are unreviewed rule-based candidates. Per the proposal's scope, "
          "none of these should be trusted without a human pass.")


def main():
    ap = argparse.ArgumentParser(description="Extract candidate claims from ingested chunks.")
    ap.add_argument("--chunks", default="outputs/chunks.jsonl")
    ap.add_argument("--out", default="outputs/claims.jsonl")
    args = ap.parse_args()
    run(args.chunks, args.out)


if __name__ == "__main__":
    main()
