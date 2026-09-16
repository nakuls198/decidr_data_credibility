# Stage 1 — Ingest

Combines Phase 1 and Phase 2 Northfield packs into deduplicated `documents.jsonl` and `chunks.jsonl`.

Phase 2 is the superset; Phase 1 documents with the same `doc_id` are dropped to avoid double-counting evidence.

```bash
python pipeline/01_ingest/run.py
```
