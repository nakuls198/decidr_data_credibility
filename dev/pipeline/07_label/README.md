# Stage 7 — Label claims

Runs the full credibility pipeline on gold claims and the Phase 1 labelled sample CSV.

Output:
- `data/outputs/labelled_claims.jsonl` — verdict, score, explanation per claim
- `data/outputs/labelling_summary.json` — aggregate stats

```bash
python pipeline/07_label/run.py
```
