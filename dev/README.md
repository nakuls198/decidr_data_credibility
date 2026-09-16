# Northfield Credibility Studio

**iLab 14-01 · Decidr · Northfield Software Ltd**

End-to-end pipeline for assessing the credibility of organisational knowledge from fragmented data (policies, CRM, Slack, interviews, meetings). Combines Phase 1 and Phase 2 Northfield datasets into one working store, applies a rulebook-guided weighting methodology, and surfaces verdicts through a black-and-orange Streamlit dashboard.

## Project structure

```
northfield_credibility_studio/
├── app.py                    # Streamlit UI (launch here)
├── config/settings.yaml      # Paths and pipeline defaults
├── data/
│   ├── raw/phase1/           # Symlink → Phase 1 pack
│   ├── raw/phase2/           # Symlink → Phase 2 pack
│   ├── combined/             # Merged raw folder (optional inspection)
│   ├── outputs/              # Pipeline JSONL outputs
│   └── gold/                 # Human-scored gold claims
├── pipeline/
│   ├── 01_ingest/            # Combine Phase 1 + 2 → chunks.jsonl
│   ├── 02_extract/           # Candidate claim extraction
│   ├── 07_label/             # Batch label gold + sample claims
│   ├── 08_explain/           # (logic in src/llm_explain.py)
│   └── run_all.py            # Run full pipeline
├── rulebook/                 # Process clusters, dispute rules, layer rows
├── src/                      # Core library (retrieve, reason, weight, score)
├── services/engine.py        # Orchestrates pipeline for UI
└── ui/                       # Black + orange theme components
```

## Eight-stage method

| Stage | Folder / module | What it does |
|-------|-----------------|--------------|
| 1 Ingest | `pipeline/01_ingest` | Merge Phase 1 + Phase 2 (dedupe by doc_id), write `chunks.jsonl` |
| 2 Extract | `pipeline/02_extract` | Rule-based claim candidates from chunks |
| 3 Retrieve | `src/retrieve.py` | BM25 keyword search + rulebook must-fetch injection |
| 4 Reason | `src/reason.py` | Stance: support / contradict / unrelated |
| 5 Weight | `src/weight.py` | Authority tier, superseded penalty, independence collapse |
| 6 Score | `src/score.py` | Bayesian log-odds → status label |
| 7 Label | `pipeline/07_label` | Batch verdicts on gold + labelled sample |
| 8 Explain | `src/llm_explain.py` | Thought-process trace + narrative (template or LLM) |

## Quick start

```bash
cd ~/Documents/northfield_credibility_studio
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run full pipeline (ingest → extract → label)
python pipeline/run_all.py

# Launch dashboard
streamlit run app.py
```

Optional LLM explanations: set `OPENAI_API_KEY` in your environment. The score is always computed by the deterministic pipeline; the LLM only narrates the result.

## Rulebook & weightage

See `rulebook/NORTHFIELD_RULEBOOK.md` for process clusters (P1–P8) and dispute types:

- **RULE** — official written policy wins over stale/draft docs
- **HAPPENED** — CRM / audit log wins over Slack memory
- **PRACTICE** — meetings + interviews; copied Slack = one source
- **GAP** — if no owner is named, verdict is Unsupported (gap)

Authority weights (starting assumptions in `src/weight.py`):

| Source type | Weight |
|-------------|--------|
| policy | 1.0 |
| process_doc | 0.8 |
| meeting | 0.6 |
| interview | 0.55 |
| crm / audit_log | 0.5 |
| comms | 0.35 |

Status labels: Supported · Likely · Conflicted · Unlikely · Unsupported · Not enough evidence

## Team (iLab 14-01)

| Role | Member |
|------|--------|
| Group Leader / Documentation | Kushal Joshi |
| Data & Evidence Pipeline | Bhavika Lalwani |
| Evidence Linking & Retrieval | Rohan Chaudhary |
| Claim Extraction & NLP | Nakul Sidiginamola |
| Credibility Modelling | Shreyash Narayane |
| Calibration & Evaluation | Prathamesh Nemade |
