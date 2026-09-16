# Northfield Credibility Studio

iLab 14-01 / Decidr. One folder for the Phase 1 pack, the Phase 2 pack, the ingested store, the eight-stage Python pipeline, and the Streamlit studio.

## Run

```bash
cd ~/Desktop/decidr_northfield_studio
chmod +x run_studio.sh
./run_studio.sh
```

Opens at [http://localhost:8501](http://localhost:8501).

## What is in here

| Path | What |
|---|---|
| `src/` | Pipeline from `pipeline.zip` (ingest → extract → retrieve → reason → weight → score → calibrate → explain) |
| `data/phase1/` | Raw Phase 1 Northfield files (overview, policies, process docs, interviews) plus `labelled_claims_sample.csv` |
| `data/phase2/` | Raw Phase 2 pack (Phase 1 carry-overs plus interviews 01–10, meetings, comms, CRM, tasks, audit log) |
| `data/outputs/chunks.jsonl` | Working store from local ingest: 45 documents, 743 chunks |
| `data/outputs/documents.jsonl` | File-level documents |
| `data/outputs/roster.json` | 29-person roster |
| `data/gold/gold_claims.json` | Human test claims for retrieval / status checks |
| `data/how_we_score_claims.md` | Scoring sheet |
| `vendor/pipeline.zip` | Original pipeline archive |
| `app.py` | Streamlit studio |

Phase 2 arrived as an extracted folder (`phase2_model_development`), not a zip and not a trained model pack. Ingest keeps Phase 2 when a `doc_id` exists in both phases, and keeps the Phase 1 labelled-claims sample (4 chunks) that Phase 2 does not re-ship.

Re-ingest:

```bash
.venv/bin/python -m src.ingest --phase1 data/phase1 --phase2 data/phase2 --out data/outputs
```

## Honest limits

- Retrieval baseline is BM25 (keyword). Meaning search is optional.
- Stance (support / contradict) is a heuristic. It can mis-label a policy that uses contrast language.
- Calibration will not invent a reliability plot on four sample rows.
- Conflicted is a valid finished status.
