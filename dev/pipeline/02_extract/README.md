# Stage 2 — Extract claims

Rule-based extraction of candidate claims (modal verbs + role names) from chunks.

Output: `data/outputs/claims.jsonl` — **unreviewed** candidates requiring human pass.

```bash
python pipeline/02_extract/run.py
```
