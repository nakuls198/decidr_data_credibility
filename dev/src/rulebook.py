"""
Rulebook integration — dispute types, process clusters, must-fetch IDs.

Loads the team's Northfield Rulebook CSVs and applies Kai/Bianca guidance
when retrieving and scoring claims (RULE / HAPPENED / PRACTICE / GAP).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

DISPUTE_TYPES = ("RULE", "HAPPENED", "PRACTICE", "GAP")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _split_ids(raw: str) -> list[str]:
    if not raw or raw.strip() in {"—", "-", ""}:
        return []
    parts = []
    for token in raw.replace("|", ";").split(";"):
        token = token.strip()
        if token and token not in {"—", "-"}:
            parts.append(token.split()[0].upper().replace("_", "-"))
    return parts


class Rulebook:
    def __init__(self, root: Path):
        self.root = root
        self.processes = _read_csv(root / "rulebook_process_master.csv")
        self.disputes = _read_csv(root / "rulebook_dispute_rules.csv")
        self.layers = _read_csv(root / "rulebook_layer_rows.csv")

    def guess_dispute_type(self, claim_text: str) -> str:
        text = claim_text.lower()
        if any(w in text for w in ("crm", "recorded", "deal", "closed won", "audit")):
            return "HAPPENED"
        if any(w in text for w in ("assigned", "owner", "accountable", "who may")):
            return "GAP"
        if any(w in text for w in ("actually", "practice", "workaround", "urgent", "informally")):
            return "PRACTICE"
        return "RULE"

    def process_for_claim(self, claim_text: str) -> dict[str, Any] | None:
        text = claim_text.lower()
        best = None
        best_score = 0
        for row in self.processes:
            name = (row.get("topic_name") or "").lower()
            topic_id = row.get("topic_id") or ""
            score = sum(1 for w in name.split() if len(w) > 3 and w in text)
            if topic_id.lower() in text:
                score += 3
            if score > best_score:
                best_score = score
                best = row
        return best

    def must_fetch_ids(self, claim_text: str, dispute_type: str | None = None) -> list[str]:
        dispute_type = dispute_type or self.guess_dispute_type(claim_text)
        proc = self.process_for_claim(claim_text)
        if not proc:
            return []

        ids = _split_ids(proc.get("linked_doc_ids", ""))
        if dispute_type == "HAPPENED":
            ids.extend(_split_ids(proc.get("crm_truth_sources", "")))
        elif dispute_type == "PRACTICE":
            ids.extend(_split_ids(proc.get("practice_sources", "")))
        elif dispute_type == "RULE":
            ids.extend(_split_ids(proc.get("in_force_rule", "")))

        seen: set[str] = set()
        out: list[str] = []
        for doc_id in ids:
            doc_id = doc_id.upper()
            if doc_id not in seen:
                seen.add(doc_id)
                out.append(doc_id)
        return out

    def dispute_guidance(self, dispute_type: str) -> dict[str, str]:
        for row in self.disputes:
            if row.get("dispute_type") == dispute_type:
                return row
        return {}

    def boost_for_doc(self, doc_id: str, dispute_type: str, claim_text: str) -> float:
        """Authority boost when rulebook says this doc should win for this dispute."""
        must = self.must_fetch_ids(claim_text, dispute_type)
        if doc_id.upper() in {m.upper() for m in must}:
            return 1.25
        proc = self.process_for_claim(claim_text)
        if not proc:
            return 1.0
        demote = proc.get("superseded_by") or ""
        if doc_id.upper() in demote.upper():
            return 0.5
        return 1.0
