"""Two-page user guide for the Northfield Credibility Studio."""
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Northfield_Studio_User_Guide.pdf"

ORANGE = HexColor("#FF6A12")
INK = HexColor("#0A0A0A")
MUTED = HexColor("#4A4A4A")
RULE = HexColor("#E4E4E4")
PILL = HexColor("#FFF3EA")
CARD = HexColor("#F6F6F6")
ORANGE_DEEP = HexColor("#E24E00")


def styles():
    base = getSampleStyleSheet()
    s = {
        "kicker": ParagraphStyle(
            "kicker",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.4,
            textColor=ORANGE,
            tracking=1.2,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=23,
            textColor=INK,
            spaceAfter=3,
        ),
        "lede": ParagraphStyle(
            "lede",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.4,
            textColor=MUTED,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=INK,
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=11.2,
            textColor=HexColor("#2A2A2A"),
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "cell_tab": ParagraphStyle(
            "cell_tab",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.7,
            leading=10,
            textColor=INK,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.6,
            leading=10,
            textColor=HexColor("#333333"),
        ),
        "step": ParagraphStyle(
            "step",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=11.1,
            textColor=HexColor("#2A2A2A"),
            leftIndent=12,
            spaceAfter=2.5,
        ),
        "foot": ParagraphStyle(
            "foot",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.2,
            textColor=HexColor("#777777"),
        ),
        "call": ParagraphStyle(
            "call",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.1,
            textColor=INK,
        ),
    }
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(INK)
    canvas.rect(0, h - 18 * mm, w, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, h - 18 * mm, 4.2 * mm, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(12 * mm, h - 8.4 * mm, "NORTHFIELD CREDIBILITY STUDIO")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(w - 12 * mm, h - 8.4 * mm, "iLab 14-01  ·  Decidr  ·  31 July 2026")
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 0, w, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica", 7.2)
    canvas.drawString(12 * mm, 3.5 * mm, "Shareable walkthrough  ·  not a legal audit")
    canvas.drawRightString(w - 12 * mm, 3.5 * mm, f"Page {doc.page} of 2")
    canvas.restoreState()


def tab_table(s):
    rows = [
        [
            Paragraph("Tab", s["cell_tab"]),
            Paragraph("What it is", s["cell_tab"]),
            Paragraph("What to do", s["cell_tab"]),
        ],
        [
            Paragraph("Overview", s["cell_tab"]),
            Paragraph(
                "Landing page. Pack size (45 files, 743 chunks, 29 people) and the Northfield tension: POL-01 vs leftover PROC-02 vs Slack workaround vs CRM exceptions.",
                s["cell"],
            ),
            Paragraph("Read this first so the later scores make sense.", s["cell"]),
        ],
        [
            Paragraph("Command centre", s["cell_tab"]),
            Paragraph(
                "KPI dashboard of the ingested store. Tiles, ring gauges and charts. These numbers describe the files, not whether a claim is true.",
                s["cell"],
            ),
            Paragraph("Use it to see what kinds of evidence exist before you score a claim.", s["cell"]),
        ],
        [
            Paragraph("Data atlas", s["cell_tab"]),
            Paragraph(
                "Searchable tables: chunks, source files, and the 29-person roster. Filter by source type (policy, Slack, CRM, meeting…) or search text / doc id.",
                s["cell"],
            ),
            Paragraph("Look up POL-01, PROC-02, DEAL-014, or a person’s name before you trust a hit.", s["cell"]),
        ],
        [
            Paragraph("Claim workbench", s["cell_tab"]),
            Paragraph(
                "Main scoring screen. One testable sentence in, status + score + evidence table out. Pick a gold claim or type your own.",
                s["cell"],
            ),
            Paragraph("This is the tab that produces a meaning-bearing output. See page 2.", s["cell"]),
        ],
        [
            Paragraph("Evidence chat", s["cell_tab"]),
            Paragraph(
                "Same pipeline as the workbench, asked in plain language. The reply is a status, a score, and the files that moved it — not a free-form chatbot paragraph.",
                s["cell"],
            ),
            Paragraph("Type a claim or tap a suggested chip. Then open Pipeline trace.", s["cell"]),
        ],
        [
            Paragraph("Pipeline trace", s["cell_tab"]),
            Paragraph(
                "The last scored claim, split into eight stages: ingest → extract → retrieve → reason → weight → score → calibrate → explain.",
                s["cell"],
            ),
            Paragraph("Run a claim first. Then check whether POL-01 was retrieved and how stance was labelled.", s["cell"]),
        ],
        [
            Paragraph("Claim extraction", s["cell_tab"]),
            Paragraph(
                "Rule-based candidates: sentences with must / shall / required. Unreviewed. A human still has to keep role, action, condition.",
                s["cell"],
            ),
            Paragraph("Browse candidates; do not treat the list as gold claims.", s["cell"]),
        ],
        [
            Paragraph("Evaluation", s["cell_tab"]),
            Paragraph(
                "Recall against a small human gold list: did search recover the files we already know? Status match uses the current heuristic reasoner.",
                s["cell"],
            ),
            Paragraph("Click “Run gold evaluation”. Disagreement is useful, not a failure to hide.", s["cell"]),
        ],
        [
            Paragraph("Method", s["cell_tab"]),
            Paragraph(
                "Why each of the eight stages exists, plus hard rules (copied Slack counts once; Conflicted is a finished answer).",
                s["cell"],
            ),
            Paragraph("Read if you need to explain the method to a teammate.", s["cell"]),
        ],
    ]
    t = Table(rows, colWidths=[32 * mm, 86 * mm, 56 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, 1), PILL),
                ("BACKGROUND", (0, 2), (-1, -1), CARD),
                ("ROWBACKGROUNDS", (0, 2), (-1, -1), [CARD, white]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
                ("GRID", (0, 0), (-1, -1), 0.3, RULE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (0, 0), white),
            ]
        )
    )
    # Header cells need white text — Paragraphs already have INK. Rebuild header as white.
    return t


def tab_table_white_header(s):
    header = ParagraphStyle(
        "hdr",
        parent=s["cell_tab"],
        textColor=white,
        fontName="Helvetica-Bold",
        fontSize=7.8,
    )
    rows_src = [
        ("Tab", "What it is", "What to do"),
        (
            "Overview",
            "Landing page. Pack size (45 files, 743 chunks, 29 people) and the Northfield tension: POL-01 vs leftover PROC-02 vs Slack workaround vs CRM exceptions.",
            "Read this first so later scores make sense.",
        ),
        (
            "Command centre",
            "KPI dashboard of the ingested store. Tiles, ring gauges and charts. These numbers describe the files, not whether a claim is true.",
            "See what kinds of evidence exist before you score a claim.",
        ),
        (
            "Data atlas",
            "Searchable tables: chunks, source files, and the 29-person roster. Filter by source type or search text / document id.",
            "Look up POL-01, PROC-02, DEAL-014, or a person’s name before you trust a hit.",
        ),
        (
            "Claim workbench",
            "Main scoring screen. One testable sentence in; status + score + evidence table out. Pick a gold claim or type your own.",
            "This is the tab that produces a meaning-bearing output. See page 2.",
        ),
        (
            "Evidence chat",
            "Same pipeline as the workbench, asked in plain language. Reply is a status, a score, and the files that moved it — not a chatbot paragraph.",
            "Type a claim or tap a suggested chip. Then open Pipeline trace.",
        ),
        (
            "Pipeline trace",
            "The last scored claim, split into eight stages: ingest → extract → retrieve → reason → weight → score → calibrate → explain.",
            "Run a claim first. Check whether POL-01 was retrieved and how stance was labelled.",
        ),
        (
            "Claim extraction",
            "Rule-based candidates: sentences with must / shall / required. Unreviewed. A human still has to keep role, action, condition.",
            "Browse candidates; do not treat the list as gold claims.",
        ),
        (
            "Evaluation",
            "Recall against a small human gold list: did search recover the files we already know? Status match uses the current heuristic reasoner.",
            "Click Run gold evaluation. Disagreement is useful, not something to hide.",
        ),
        (
            "Method",
            "Why each of the eight stages exists, plus hard rules (copied Slack counts once; Conflicted is a finished answer).",
            "Read if you need to explain the method to a teammate.",
        ),
    ]
    data = []
    for i, (a, b, c) in enumerate(rows_src):
        st_a = header if i == 0 else s["cell_tab"]
        st_b = header if i == 0 else s["cell"]
        st_c = header if i == 0 else s["cell"]
        data.append([Paragraph(a, st_a), Paragraph(b, st_b), Paragraph(c, st_c)])
    t = Table(data, colWidths=[32 * mm, 87 * mm, 55 * mm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("GRID", (0, 0), (-1, -1), 0.25, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0, INK),
    ]
    for r in range(1, len(data)):
        bg = PILL if r == 1 else (CARD if r % 2 == 0 else white)
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), bg))
    t.setStyle(TableStyle(style_cmds))
    return t


def chart_table(s):
    rows_src = [
        ("Chart / number", "Where", "What it means"),
        (
            "KPI tiles (45 / 743 / 29 / date)",
            "Overview, Command centre",
            "How big the pack is. Not a credibility score.",
        ),
        (
            "Ring gauges (audit, tasks, meeting, process %)",
            "Command centre",
            "Share of chunks from the four largest source types. Shows the store is heavy on logs and tasks, lighter on policy.",
        ),
        (
            "Chunks by source type (bar + line)",
            "Command centre",
            "Same counts, two views: how many searchable pieces came from audit log, tasks, meetings, CRM, Slack, policy, etc.",
        ),
        (
            "Chunks by phase (donut)",
            "Command centre",
            "How much of the store is Phase 1 vs Phase 2. Most live chunks come from the Phase 2 pack.",
        ),
        (
            "Starting authority weights (bar)",
            "Command centre",
            "How the scorer starts: in-force policy outweighs a process leftover; Slack is weakest. Not the final score of a claim.",
        ),
        (
            "Roster by function (bar)",
            "Command centre",
            "Headcount by team. Context for “who said this”, not evidence by itself.",
        ),
        (
            "Kept vs unrelated retrieval bars",
            "Pipeline trace",
            "Which document ids came back from search, and which were dropped as unrelated to the claim.",
        ),
        (
            "Recall @ k bars + match tiles",
            "Evaluation",
            "For each gold claim, did the known files appear in the top-k hits? Orange = status matched the gold label; grey = it did not.",
        ),
        (
            "Verdict / score / confidence / interval",
            "Workbench, Chat, Trace",
            "The actual claim output. Status is the answer; confidence is how much independent evidence there was; interval is a range, not a fake 0–100.",
        ),
    ]
    header = ParagraphStyle("hdr2", parent=s["cell_tab"], textColor=white, fontSize=7.8)
    data = []
    for i, (a, b, c) in enumerate(rows_src):
        st = header if i == 0 else s["cell"]
        sta = header if i == 0 else s["cell_tab"]
        data.append([Paragraph(a, sta), Paragraph(b, st), Paragraph(c, st)])
    t = Table(data, colWidths=[52 * mm, 38 * mm, 84 * mm])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.8),
        ("GRID", (0, 0), (-1, -1), 0.25, RULE),
    ]
    for r in range(1, len(data)):
        cmds.append(("BACKGROUND", (0, r), (-1, r), CARD if r % 2 == 0 else white))
    t.setStyle(TableStyle(cmds))
    return t


def callout(text, s):
    inner = Paragraph(text, s["call"])
    t = Table([[inner]], colWidths=[174 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PILL),
                ("BOX", (0, 0), (-1, -1), 0, PILL),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBEFORE", (0, 0), (0, 0), 3, ORANGE),
            ]
        )
    )
    return t


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=22 * mm,
        bottomMargin=14 * mm,
        title="Northfield Credibility Studio — how to use the app",
        author="Rohan Chaudhary · iLab 14-01",
    )
    story = []

    story.append(Paragraph("HOW TO USE THE APP", s["kicker"]))
    story.append(Paragraph("A two-page walkthrough for someone opening the studio for the first time.", s["h1"]))
    story.append(
        Paragraph(
            "This Streamlit app scores <b>testable claims</b> against Northfield’s fragmented files "
            "(policies, leftover process docs, interviews, meetings, Slack, CRM, tasks, audit log). "
            "It is a credibility trail, not a chatbot that hides disagreement. "
            "Open the folder <b>decidr_northfield_studio</b>, run <b>./run_studio.sh</b>, then go to "
            "<b>http://localhost:8501</b>. Use the orange sidebar on the left to switch tabs.",
            s["lede"],
        )
    )
    story.append(Paragraph("The nine tabs", s["h2"]))
    story.append(tab_table_white_header(s))
    story.append(Spacer(1, 6))
    story.append(
        callout(
            "<b>What a claim looks like.</b> One sentence with a role, an action and a condition. "
            "Example: “Head of Finance and People Ops must approve new-business discounts of 15% or more in the CRM before Closed Won.” "
            "Formal policy and practised workaround are two different claims.",
            s,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("CHARTS, SCORES, AND HOW TO GET AN OUTPUT", s["kicker"]))
    story.append(Paragraph("Numbers on screen, and what to click", s["h1"]))
    story.append(Paragraph("Charts and tiles", s["h2"]))
    story.append(chart_table(s))

    story.append(Paragraph("How to get a meaningful output", s["h2"]))
    story.append(
        Paragraph(
            "<b>1.</b>  Open <b>Claim workbench</b> (or Evidence chat if you prefer typing in the box).",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>2.</b>  Pick a gold claim from the dropdown, or type one sentence. Keep it specific (who / what / under what condition).",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>3.</b>  Leave defaults if unsure: retrieve top-k = 15, score method = bayesian, prior = 0.5. Click <b>Run pipeline</b>.",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>4.</b>  Read the four tiles: <b>Verdict</b> (Supported / Likely / Conflicted / Unlikely / Unsupported / Not enough evidence), "
            "<b>Score</b> (0–1), <b>Confidence</b> (High / Medium / Low — how much independent evidence, not how “true”), "
            "and <b>Interval</b> (a range around the score).",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>5.</b>  Scroll the evidence table. Each row is a file chunk: document id, source type, stance (support / contradict / unrelated), weight, and a text preview. "
            "Policy should outweigh Slack. Copied Slack threads share weight so they are not three confirmations.",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>6.</b>  Open <b>Pipeline trace</b> for the same run. Check retrieval actually found POL-01 / PROC-02 / COMMUNICATIONS-LOG / CRM-DEALS when those files matter. "
            "If a known policy is missing from the shortlist, do not trust the score.",
            s["step"],
        )
    )
    story.append(
        Paragraph(
            "<b>7.</b>  Optional: <b>Evaluation</b> → Run gold evaluation, to see whether search recovers the files on the human gold list.",
            s["step"],
        )
    )

    story.append(Paragraph("How to read Conflicted", s["h2"]))
    story.append(
        Paragraph(
            "<b>Conflicted is a valid finished answer.</b> For the discount-approval example, POL-01 (Harriet, CRM, from 1 Mar 2025) "
            "can sit against PROC-02 (Victor, 2022 leftover), Diane’s Slack bypass, and CRM rows that did not follow policy. "
            "The studio should surface that split, not average it into a fake 80%. "
            "Confidence can still be High when both sides are well evidenced.",
            s["body"],
        )
    )

    story.append(
        callout(
            "<b>Honest limits (do not oversell).</b> Search is keyword BM25, not meaning search. "
            "Stance is a lexical heuristic — POL-01 can be labelled “contradict” because the policy uses contrast language. "
            "Calibration will not draw a reliability plot on four gold rows. "
            "This is not a legally defensible audit tool. Inspect the evidence table; do not quote the score alone.",
            s,
        )
    )
    story.append(Spacer(1, 5))
    story.append(
        Paragraph(
            "Folder to share: <b>decidr_northfield_studio</b> (leave out .venv). Raw Phase 1 = data/phase1 · raw Phase 2 = data/phase2 · working store = data/outputs.",
            s["foot"],
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUT


if __name__ == "__main__":
    path = build()
    print(path)
