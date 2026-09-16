"""
Shared data structures for the credibility-scoring pipeline.

These mirror the `claims` / `evidence` table design from the team's
data-exploration notes and the Group Proposal Report (Section 4.1).
Every stage of the pipeline (ingest -> extract -> retrieve -> reason ->
weight -> score -> calibrate -> explain) reads and writes these shapes,
so changing a field here can ripple through every stage -- change with
the team's agreement, not solo.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import json


# ---------------------------------------------------------------------------
# Stage 1: ingestion output
# ---------------------------------------------------------------------------

@dataclass
class Document:
    """One source file (a policy, a process doc, an interview, a CSV, ...)."""

    doc_id: str                      # e.g. "POL-01", "INT-02", "CRM-DEALS"
    path: str                        # path the text was read from
    source_type: str                 # policy / process_doc / interview / meeting /
                                      # comms / crm / tasks / audit_log / labelled_sample
    phase: str                       # "phase1" or "phase2"
    title: Optional[str] = None
    n_chunks: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    """One retrievable unit of text belonging to a Document."""

    chunk_id: str                    # f"{doc_id}::{index}"
    doc_id: str
    source_type: str
    phase: str
    heading: Optional[str]           # markdown heading this chunk sits under, if any
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Stage 2: claim extraction output
# ---------------------------------------------------------------------------

@dataclass
class Claim:
    """
    One atomic, testable proposition: who (a role) may or must do what,
    under which condition. See Section 3 ("Project Problems") of the
    proposal for why claims must stay atomic -- a formal rule and its
    practised exception are two claims, not one.
    """

    claim_id: str
    claim_text: str
    category: Optional[str] = None          # e.g. "Financial control", "Process step"
    responsible_role: Optional[str] = None
    layer: Optional[str] = None             # formal / practised / gap / draft / stale
    origin_doc_id: Optional[str] = None
    origin_chunk_id: Optional[str] = None
    extraction_confidence: float = 0.5
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None


# ---------------------------------------------------------------------------
# Stage 3-5: evidence, after retrieval / reasoning / weighting
# ---------------------------------------------------------------------------

@dataclass
class Evidence:
    """One retrieved chunk, evaluated against one claim."""

    evidence_id: str
    claim_id: str
    chunk_id: str
    source_doc_id: str
    source_type: str

    retrieval_score: float = 0.0            # stage 3: raw retriever score
    stance: Optional[str] = None            # stage 4: support / contradict / unrelated
    stance_confidence: float = 0.0          # stage 4

    authority_tier: Optional[str] = None    # stage 5: approved-formal / draft-unapproved /
                                             #          informal-testimony / secondhand
    recency_weight: float = 1.0             # stage 5
    independence_weight: float = 1.0        # stage 5: 1.0 for a unique source, <1.0 if it is
                                             #          a duplicate/copy of another cited source
    directness: Optional[str] = None        # stage 5: direct-participant / heard-about
    final_weight: float = 0.0               # stage 5: combined weight used by scoring

    excerpt: str = ""
    notes: str = ""


# ---------------------------------------------------------------------------
# Stage 6-8: scored claim
# ---------------------------------------------------------------------------

STATUS_LABELS = [
    "Supported",
    "Likely",
    "Conflicted",
    "Unlikely",
    "Unsupported",
    "Not enough evidence",
]


@dataclass
class ScoredClaim:
    claim_id: str
    claim_text: str
    credibility_score: float                # posterior probability, 0-1
    credible_interval: Optional[List[float]] = None   # [low, high], if estimated
    status: str = "Not enough evidence"
    confidence: str = "Low"                 # High / Medium / Low, separate from the score
    supporting_evidence: List[str] = field(default_factory=list)   # evidence_ids
    contradicting_evidence: List[str] = field(default_factory=list)
    explanation: str = ""
    calibration_note: Optional[str] = None  # filled by stage 7, or a statement it could not run


# ---------------------------------------------------------------------------
# JSONL helpers used by every stage
# ---------------------------------------------------------------------------

def write_jsonl(path: str, rows: List[Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            d = asdict(row) if hasattr(row, "__dataclass_fields__") else row
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
