# Pipeline stages

Run everything: `python pipeline/run_all.py`

Or step by step:

```bash
# 0. (Optional) Merge raw folders for inspection
python scripts/combine_datasets.py

# 1. Ingest Phase 1 + Phase 2
python pipeline/01_ingest/run.py

# 2. Extract candidate claims
python pipeline/02_extract/run.py

# 7. Label gold + sample claims with verdicts
python pipeline/07_label/run.py
```

Stages 3–6 (retrieve, reason, weight, score) run inside `services/engine.py` per claim.
Stage 8 (explain + thought process) runs in `src/llm_explain.py`.

Outputs land in `data/outputs/`:

- `documents.jsonl` — one row per source file
- `chunks.jsonl` — searchable evidence units
- `claims.jsonl` — extracted candidate claims
- `labelled_claims.jsonl` — scored gold + sample rows
- `labelling_summary.json` — aggregate stats
