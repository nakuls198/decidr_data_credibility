#!/usr/bin/env python3
"""Stage 1 — Ingest Phase 1 + Phase 2 into documents.jsonl and chunks.jsonl."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingest import run  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 1: Ingest Northfield data packs.")
    ap.add_argument("--phase1", default=str(ROOT / "data/raw/phase1/northfield"))
    ap.add_argument("--phase2", default=str(ROOT / "data/raw/phase2/northfield"))
    ap.add_argument("--out", default=str(ROOT / "data/outputs"))
    args = ap.parse_args()
    run(args.phase1, args.phase2, args.out)


if __name__ == "__main__":
    main()
