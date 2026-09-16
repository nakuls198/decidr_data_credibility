#!/usr/bin/env python3
"""
Run the full Northfield credibility pipeline end-to-end.

Stages:
  1. Ingest     — combine Phase 1 + Phase 2 → chunks.jsonl
  2. Extract    — candidate claims from chunks
  7. Label      — score & label gold + sample claims
  (3–6 run inside the label/workbench engine per claim)
  8. Explain    — thought-process + narrative (template or LLM)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_stage(script: Path, label: str) -> None:
    print(f"\n{'=' * 60}\n  {label}\n{'=' * 60}")
    subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT)


def main() -> None:
    # Optional: merge raw folders for inspection
    combine = ROOT / "scripts/combine_datasets.py"
    if combine.exists():
        print("Combining raw Phase 1 + Phase 2 folders...")
        subprocess.run([sys.executable, str(combine)], check=True, cwd=ROOT)

    run_stage(ROOT / "pipeline/01_ingest/run.py", "Stage 1 — Ingest")
    run_stage(ROOT / "pipeline/02_extract/run.py", "Stage 2 — Extract claims")
    run_stage(ROOT / "pipeline/07_label/run.py", "Stage 7 — Label claims")

    print("\n✓ Pipeline complete. Outputs in data/outputs/")
    print("  Launch UI:  streamlit run app.py")


if __name__ == "__main__":
    main()
