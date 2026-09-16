#!/usr/bin/env python3
"""Stage 2 — Extract candidate claims from chunks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.extract import main as extract_main  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 2: Extract claims.")
    ap.add_argument("--chunks", default=str(ROOT / "data/outputs/chunks.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "data/outputs/claims.jsonl"))
    args, _ = ap.parse_known_args()
    sys.argv = ["extract", "--chunks", args.chunks, "--out", args.out]
    extract_main()


if __name__ == "__main__":
    main()
