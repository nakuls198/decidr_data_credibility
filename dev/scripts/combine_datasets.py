#!/usr/bin/env python3
"""
Merge Phase 1 and Phase 2 raw Northfield packs into a single combined folder.

Phase 2 is the superset (meetings, CRM, comms, audit). Phase 1-only files
(e.g. labelled_claims_sample.csv) are copied in when absent from Phase 2.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKIP = {".ds_store", "readme.md"}


def combine(phase1: Path, phase2: Path, out: Path) -> dict:
    phase1 = phase1.resolve()
    phase2 = phase2.resolve()
    out = out.resolve()

    if not phase1.is_dir():
        raise SystemExit(f"Phase 1 directory not found: {phase1}")
    if not phase2.is_dir():
        raise SystemExit(f"Phase 2 directory not found: {phase2}")

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(phase2, out)

    added = []
    for src in sorted(phase1.rglob("*")):
        if not src.is_file() or src.name.lower() in SKIP:
            continue
        rel = src.relative_to(phase1)
        dest = out / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            added.append(str(rel))

    claims = phase1 / "labelled_claims_sample.csv"
    if claims.exists():
        shutil.copy2(claims, out / "labelled_claims_sample.csv")

    return {
        "combined_dir": str(out),
        "phase2_files": sum(1 for _ in phase2.rglob("*") if _.is_file()),
        "phase1_only_added": added,
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Combine Phase 1 + Phase 2 raw data.")
    ap.add_argument("--phase1", default=str(root / "data/raw/phase1/northfield"))
    ap.add_argument("--phase2", default=str(root / "data/raw/phase2/northfield"))
    ap.add_argument("--out", default=str(root / "data/combined"))
    args = ap.parse_args()

    stats = combine(Path(args.phase1), Path(args.phase2), Path(args.out))
    print(f"Combined dataset -> {stats['combined_dir']}")
    print(f"  Phase 2 base files: {stats['phase2_files']}")
    print(f"  Phase 1-only additions: {len(stats['phase1_only_added'])}")
    for rel in stats["phase1_only_added"]:
        print(f"    + {rel}")


if __name__ == "__main__":
    main()
