"""Shared record types for the ingestion stage."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    doc_id: str
    path: str
    source_type: str
    phase: str
    title: str
    n_chunks: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    source_type: str
    phase: str
    heading: Optional[str]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def write_jsonl(path: str, records: List[Any]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
