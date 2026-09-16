#!/usr/bin/env python3
"""Generate a brief PDF report for Northfield Credibility Studio."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "Northfield_Credibility_Studio_Brief_Report.pdf"


class Report(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Northfield Credibility Studio  |  iLab 14-01 / Decidr", new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title: str) -> None:
        self.ln(3)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(200, 70, 10)
        self.multi_cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text: str) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def bullet(self, text: str) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, f"  -  {text}", new_x="LMARGIN", new_y="NEXT")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = Report()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 9, "Northfield Credibility Studio", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 6, f"Brief technical report  |  {date.today().strftime('%d %B %Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(
        0,
        6,
        "Assessing the credibility of organisational knowledge from fragmented data",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)

    pdf.section_title("1. Project overview")
    pdf.body(
        "This system implements the iLab 14-01 group proposal: a credibility assessment pipeline "
        "for Northfield Software Ltd (Decidr partner dataset). Organisational knowledge is scattered "
        "across policies, process documents, interviews, meetings, Slack communications, CRM records, "
        "project tasks, and audit logs. The pipeline retrieves evidence for a claim, weighs sources "
        "by authority, scores credibility, and returns an inspectable verdict, including Conflicted "
        "when formal rules and practised behaviour disagree."
    )

    pdf.section_title("2. Data preparation")
    pdf.body(
        "Phase 1 and Phase 2 Northfield data packs were combined into one working dataset. "
        "Phase 2 is the superset. Documents with the same ID in both phases are deduplicated "
        "(Phase 2 kept) to avoid double-counting evidence."
    )
    pdf.bullet("Combined raw folder: data/combined/ (45 files + labelled sample claims)")
    pdf.bullet("Pipeline output: data/outputs/chunks.jsonl (743 searchable text chunks)")
    pdf.bullet("Gold claims: data/gold/gold_claims.json (25 human-scored test claims)")
    pdf.bullet("Rulebook: rulebook/ (process clusters P1-P8 and dispute-type guidance)")

    pdf.section_title("3. Backend pipeline (eight stages)")
    stages = [
        (
            "Stage 1 - Ingest",
            "Reads Phase 1 + Phase 2 markdown and CSV files. Splits markdown on headings; "
            "one chunk per CSV row. Writes documents.jsonl and chunks.jsonl.",
        ),
        (
            "Stage 2 - Extract",
            "Rule-based claim extraction using modal verbs (must, shall, required) and role names. "
            "Outputs unreviewed candidate claims.",
        ),
        (
            "Stage 3 - Retrieve",
            "BM25 keyword search finds top-k evidence chunks. Rulebook must-fetch IDs are injected "
            "so linked documents are not missed.",
        ),
        (
            "Stage 4 - Reason",
            "Each chunk is labelled support, contradict, or unrelated via lexical overlap and "
            "negation cues. Unrelated chunks are dropped.",
        ),
        (
            "Stage 5 - Weight",
            "Authority tier applied (policy 1.0 down to comms 0.35). Superseded/draft penalties. "
            "Duplicate Slack copies collapse to one independent source.",
        ),
        (
            "Stage 6 - Score",
            "Bayesian log-odds update from weighted evidence produces a 0-1 score and status label.",
        ),
        (
            "Stage 7 - Label",
            "Batch run on gold and labelled sample claims. Writes labelled_claims.jsonl.",
        ),
        (
            "Stage 8 - Explain",
            "Deterministic 6-step thought-process trace plus narrative. Optional LLM rewrites prose "
            "only; it never changes the score.",
        ),
    ]
    for title, desc in stages:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
        pdf.body(desc)

    pdf.add_page()
    pdf.section_title("4. Rulebook and weightage")
    pdf.body("The Northfield Rulebook encodes client guidance. Four dispute types determine which sources win:")
    pdf.bullet("RULE: approved in-force policy beats stale/draft documents")
    pdf.bullet("HAPPENED: CRM and audit log beat Slack memory for recorded events")
    pdf.bullet("PRACTICE: meetings and interviews; copied Slack threads count as one source")
    pdf.bullet("GAP: if no owner is formally assigned, verdict is Unsupported (gap)")
    pdf.body(
        "Process clusters (P1-P8) link related document IDs. Must-fetch documents are boosted during "
        "retrieval and weighting. Formal and practised claims are scored separately, never averaged."
    )

    pdf.section_title("5. Verdict labels")
    pdf.body(
        "Supported (score >= 0.75) | Likely (>= 0.6) | Conflicted (weight on both sides) | "
        "Unlikely (<= 0.4) | Unsupported (<= 0.25) | Not enough evidence. "
        "Confidence (High/Medium/Low) reflects evidence completeness, separate from score direction."
    )

    pdf.section_title("6. Streamlit UI")
    pdf.body(
        "The dashboard uses a black background and orange accent (#FF6A12), matching the reference design. "
        "Launch with: streamlit run app.py"
    )
    pages = [
        ("Overview", "Introduction, eight-stage method strip, corpus KPIs, usage guide."),
        ("Command centre", "KPI dashboard: counts, source-type charts, circular gauges, bar/line charts."),
        ("Data atlas", "Browse ingested documents and chunks by source type and phase."),
        ("Claim workbench", "Score claims; shows verdict, thought-process trace, evidence table."),
        ("Evidence chat", "Ask questions with retrieved chunk citations."),
        ("Claim extraction", "View rule-based candidate claims from the corpus."),
        ("Evaluation", "Compare verdicts against gold expected statuses and retrieval recall."),
        ("Method", "Authority weights, status thresholds, pipeline documentation."),
    ]
    for name, desc in pages:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5, name, new_x="LMARGIN", new_y="NEXT")
        pdf.body(desc)

    pdf.section_title("7. How to run")
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(50, 50, 50)
    for line in [
        "cd ~/Documents/northfield_credibility_studio",
        "source .venv/bin/activate",
        "python pipeline/run_all.py",
        "streamlit run app.py",
    ]:
        pdf.multi_cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.body("Optional: set OPENAI_API_KEY for LLM explanations (score remains deterministic).")

    pdf.section_title("8. Folder layout")
    pdf.set_font("Courier", "", 9)
    for line in [
        "pipeline/   01_ingest, 02_extract, 07_label, run_all.py",
        "src/        retrieve, reason, weight, score, explain, rulebook",
        "services/   engine.py (orchestrates pipeline for UI)",
        "ui/         black + orange theme",
        "data/outputs/  chunks.jsonl, labelled_claims.jsonl",
    ]:
        pdf.multi_cell(0, 5, line, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "Team: iLab 14-01 - Decidr x Northfield Software Ltd | Assessment date: 31 July 2026",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.output(str(OUT))
    print(f"Created: {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
