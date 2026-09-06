"""Stage 1: Data ingestion."""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import zipfile
from pathlib import Path
from typing import Iterable, List, Tuple, Optional

from .schema import Document, Chunk, write_jsonl

# Folder-name -> source_type mapping shared by both phases.
FOLDER_SOURCE_TYPE = {
    "00_overview": "overview",
    "02_policies": "policy",
    "03_process_docs": "process_doc",
    "04_interviews": "interview",
    "05_meetings": "meeting",
    "06_communications": "comms",
    "07_crm": "crm",
    "08_project_tasks": "tasks",
    "09_audit_log": "audit_log",
}

# Files handled as one-row-per-chunk CSVs rather than markdown.
CSV_FILENAMES = {
    "crm_deals.csv",
    "project_tasks.csv",
    "system_audit_log.csv",
    "labelled_claims_sample.csv",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


# ---------------------------------------------------------------------------
# Source abstraction: a plain directory or a .zip, treated identically
# ---------------------------------------------------------------------------

def iter_source_files(root: str) -> Iterable[Tuple[str, str]]:
    """
    Yield (relative_path, text) for every real content file under `root`.

    `root` may be a directory (Phase 1, as released) or a .zip file
    (Phase 2, as released). Mac resource-fork junk (__MACOSX/, "._*") is
    skipped automatically.
    """
    root_path = Path(root)

    if root_path.is_dir():
        for path in sorted(root_path.rglob("*")):
            if path.is_file() and _is_content_file(path.name):
                rel = str(path.relative_to(root_path))
                yield rel, path.read_text(encoding="utf-8", errors="replace")

    elif root_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(root_path) as zf:
            for info in sorted(zf.infolist(), key=lambda i: i.filename):
                name = info.filename
                if info.is_dir() or "__MACOSX" in name:
                    continue
                base = os.path.basename(name)
                if not _is_content_file(base):
                    continue
                # Zips from Decidr wrap everything in one top folder
                # (e.g. "phase2_model_development/02_policies/POL-01...").
                # Strip that single top-level folder so downstream folder
                # lookups (FOLDER_SOURCE_TYPE) still work.
                parts = Path(name).parts
                rel = str(Path(*parts[1:])) if len(parts) > 1 else name
                with zf.open(info) as fh:
                    text = fh.read().decode("utf-8", errors="replace")
                yield rel, text
    else:
        raise ValueError(f"Don't know how to read source: {root}")


def _is_content_file(filename: str) -> bool:
    if filename.startswith("._") or filename == ".DS_Store":
        return False
    return filename.lower().endswith((".md", ".csv"))


# ---------------------------------------------------------------------------
# doc_id derivation
# ---------------------------------------------------------------------------

_ID_PREFIX_RE = re.compile(r"^([A-Z]+-\d+)")


def derive_doc_id(rel_path: str) -> str:
    stem = Path(rel_path).stem
    m = _ID_PREFIX_RE.match(stem.upper())
    if m:
        return m.group(1)
    # No POL-01 style prefix -- fall back to a readable slug, e.g.
    # "company_overview" -> "COMPANY-OVERVIEW", "crm_deals" -> "CRM-DEALS".
    return stem.upper().replace("_", "-")


def source_type_for(rel_path: str) -> str:
    if Path(rel_path).name == "labelled_claims_sample.csv":
        return "labelled_sample"
    parts = Path(rel_path).parts
    top = parts[0] if parts else ""
    return FOLDER_SOURCE_TYPE.get(top, "other")


def is_superseded(rel_path: str) -> bool:
    return "superseded" in Path(rel_path).parts or "SUPERSEDED" in rel_path.upper()


# ---------------------------------------------------------------------------
# Markdown chunking: split on headings, keep any preamble as chunk 0
# ---------------------------------------------------------------------------

def chunk_markdown(text: str) -> List[Tuple[Optional[str], str]]:
    """Return [(heading_or_None, chunk_text), ...]."""
    lines = text.splitlines()
    chunks: List[Tuple[Optional[str], List[str]]] = []
    current_heading: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) <= 2:  # split on H1/H2, keep H3+ inside a chunk
            if current_lines:
                chunks.append((current_heading, current_lines))
            current_heading = m.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        chunks.append((current_heading, current_lines))

    result = []
    for heading, body_lines in chunks:
        body = "\n".join(body_lines).strip()
        if body:
            result.append((heading, body))
    return result if result else [(None, text.strip())]


def chunk_csv(text: str) -> List[Tuple[Optional[str], str]]:
    """One chunk per row: 'col: value; col: value; ...'."""
    reader = csv.DictReader(io.StringIO(text))
    chunks = []
    for i, row in enumerate(reader):
        parts = [f"{k}: {v}" for k, v in row.items() if v not in (None, "")]
        chunks.append((f"row {i}", "; ".join(parts)))
    return chunks


# ---------------------------------------------------------------------------
# Main ingestion driver
# ---------------------------------------------------------------------------

def ingest_source(root: str, phase: str) -> Tuple[List[Document], List[Chunk]]:
    documents: List[Document] = []
    chunks: List[Chunk] = []

    for rel_path, text in iter_source_files(root):
        filename = Path(rel_path).name
        if filename.lower() == "readme.md":
            continue

        doc_id = derive_doc_id(rel_path)
        source_type = source_type_for(rel_path)
        superseded = is_superseded(rel_path)

        if filename in CSV_FILENAMES or (source_type in {"crm", "tasks", "audit_log"}):
            raw_chunks = chunk_csv(text)
        else:
            raw_chunks = chunk_markdown(text)

        doc = Document(
            doc_id=doc_id,
            path=rel_path,
            source_type=source_type,
            phase=phase,
            title=filename,
            n_chunks=len(raw_chunks),
            metadata={"superseded": superseded},
        )
        documents.append(doc)

        for i, (heading, body) in enumerate(raw_chunks):
            chunks.append(Chunk(
                chunk_id=f"{doc_id}::{i}",
                doc_id=doc_id,
                source_type=source_type,
                phase=phase,
                heading=heading,
                text=body,
                metadata={"superseded": superseded},
            ))

    return documents, chunks


def run(phase1: Optional[str], phase2: Optional[str], out_dir: str) -> None:
    """
    Ingests whichever of phase1 / phase2 are given.

    Important, easy-to-miss data fact: Phase 2, as released, is not a
    diff on top of Phase 1 -- it re-ships the same overview/policy/
    process/interview files byte-for-byte (verified: e.g. POL-01 and
    INT-02 are identical between the two releases) and then adds the
    genuinely new material (remaining interviews, meetings,
    communications log, CRM, tasks, audit log). If both are ingested
    naively you get every carried-over document twice, with duplicate
    doc_ids and chunk_ids, which silently double-counts evidence at the
    weighting/scoring stage. So: when a doc_id exists in both phases,
    Phase 2's copy is kept and Phase 1's is dropped, rather than kept
    side by side as if they were two independent sources.
    """
    phase1_docs, phase1_chunks = ingest_source(phase1, phase="phase1") if phase1 else ([], [])
    phase2_docs, phase2_chunks = ingest_source(phase2, phase="phase2") if phase2 else ([], [])

    phase2_doc_ids = {d.doc_id for d in phase2_docs}
    dropped = [d for d in phase1_docs if d.doc_id in phase2_doc_ids]
    kept_phase1_docs = [d for d in phase1_docs if d.doc_id not in phase2_doc_ids]
    kept_phase1_chunks = [c for c in phase1_chunks if c.doc_id not in phase2_doc_ids]

    if phase1:
        print(f"phase1: {len(phase1_docs)} documents, {len(phase1_chunks)} chunks "
              f"({len(dropped)} dropped as exact carry-overs already in phase2)")
    if phase2:
        print(f"phase2: {len(phase2_docs)} documents, {len(phase2_chunks)} chunks")

    all_docs = kept_phase1_docs + phase2_docs
    all_chunks = kept_phase1_chunks + phase2_chunks

    os.makedirs(out_dir, exist_ok=True)
    write_jsonl(os.path.join(out_dir, "documents.jsonl"), all_docs)
    write_jsonl(os.path.join(out_dir, "chunks.jsonl"), all_chunks)
    print(f"TOTAL (deduplicated): {len(all_docs)} documents, {len(all_chunks)} chunks -> {out_dir}")


def main():
    ap = argparse.ArgumentParser(description="Ingest the Northfield data pack(s).")
    ap.add_argument("--phase1", help="Path to phase1_framework_development/ (folder)")
    ap.add_argument("--phase2", help="Path to phase2_model_development.zip (or its extracted folder)")
    ap.add_argument("--out", default="outputs", help="Where to write documents.jsonl / chunks.jsonl")
    args = ap.parse_args()

    if not args.phase1 and not args.phase2:
        ap.error("Provide at least one of --phase1 / --phase2")

    run(args.phase1, args.phase2, args.out)


if __name__ == "__main__":
    main()
