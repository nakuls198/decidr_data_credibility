# Stage 8 — Explain

Implementation: `src/llm_explain.py`

Produces a **deterministic thought-process trace** (6 steps) plus a narrative explanation.

- Without `OPENAI_API_KEY`: template narrative from `src/explain.py`
- With `OPENAI_API_KEY`: LLM rewrites the narrative only — **never changes the score**

Thought-process steps shown in the Claim Workbench UI:

1. Frame the claim
2. Classify dispute type (RULE / HAPPENED / PRACTICE / GAP)
3. Must-fetch documents from rulebook
4. Retrieve & reason (stance filtering)
5. Weight evidence (authority + independence)
6. Score & verdict
