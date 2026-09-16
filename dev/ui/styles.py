"""Black + vivid orange KPI theme, matching the dashboard reference."""

ORANGE = "#FF6A12"
ORANGE_DEEP = "#FF4E00"
INK = "#0A0A0A"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;650;800&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
  background: #0A0A0A !important;
  color: #F4F4F4;
  font-family: 'Outfit', sans-serif;
}

.stApp header { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }

.block-container {
  padding-top: 1.15rem !important;
  padding-bottom: 2.4rem !important;
  max-width: 1320px;
}

[data-testid="stSidebar"] {
  background: #070707 !important;
  border-right: 1px solid #1A1A1A;
}
[data-testid="stSidebar"] * { color: #F2F2F2 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding: 0.42rem 0.7rem !important;
  border-radius: 10px;
  margin-bottom: 2px;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: #FF6A12 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * {
  color: #0A0A0A !important;
  font-weight: 700 !important;
}

h1, h2, h3, .hero-title, .display {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 800 !important;
  letter-spacing: -0.045em;
  color: #FFFFFF !important;
}

.hero {
  padding: 1.35rem 1.5rem 1.25rem;
  border-radius: 22px;
  background:
    radial-gradient(420px 180px at 100% 120%, rgba(255,106,18,0.28), transparent 62%),
    #111111;
  border: 1px solid #1E1E1E;
  margin-bottom: 1rem;
}
.eyebrow {
  font-size: 0.72rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #FF6A12;
  font-weight: 650;
  margin-bottom: 0.4rem;
}
.eyebrow.light { color: rgba(255,255,255,0.72); }
.hero p { color: #A3A3A3; font-size: 0.98rem; line-height: 1.5; margin: 0.4rem 0 0; }
.display {
  font-size: clamp(2.35rem, 4.6vw, 3.55rem);
  line-height: 0.92;
  margin: 0;
}

.tile, .glass {
  background:
    radial-gradient(220px 140px at 108% 118%, rgba(255,106,18,0.38), transparent 58%),
    #141414;
  border: 1px solid #1F1F1F;
  border-radius: 18px;
  padding: 1.05rem 1.15rem;
  margin-bottom: 0.85rem;
  position: relative;
  overflow: hidden;
}
.tile-orange, .panel-orange, .glass-cream {
  background: linear-gradient(145deg, #FF7A28 0%, #FF4E00 100%);
  border: none;
  border-radius: 18px;
  padding: 1.05rem 1.15rem;
  margin-bottom: 0.85rem;
  color: #FFFFFF;
}
.tile-orange h3, .tile-orange p, .tile-orange span,
.panel-orange h3, .panel-orange p, .panel-orange span,
.glass-cream h3, .glass-cream p, .glass-cream span { color: #FFFFFF !important; }
.panel-orange p, .glass-cream p { color: rgba(255,255,255,0.86) !important; }

.kpi {
  font-family: 'Outfit', sans-serif;
  font-size: 2.35rem;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 0.95;
  letter-spacing: -0.04em;
}
.tile-orange .kpi, .panel-orange .kpi { color: #FFFFFF; }
.kpi-label {
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #8A8A8A;
  margin-top: 0.45rem;
  font-weight: 650;
}
.tile-orange .kpi-label, .panel-orange .kpi-label { color: rgba(255,255,255,0.78); }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.85rem;
  margin: 0 0 1rem;
}
.ring-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.85rem;
  margin: 0 0 1rem;
}

.ring-card {
  background:
    radial-gradient(180px 120px at 100% 100%, rgba(255,106,18,0.32), transparent 60%),
    #141414;
  border: 1px solid #1F1F1F;
  border-radius: 18px;
  padding: 1rem 0.7rem 1.05rem;
  text-align: center;
}
.ring-svg { position: relative; width: 132px; height: 132px; margin: 0 auto 0.35rem; }
.ring-svg svg { width: 132px; height: 132px; }
.ring-svg .track { fill: none; stroke: #242424; stroke-width: 8; }
.ring-svg .prog {
  fill: none;
  stroke: #FF6A12;
  stroke-width: 8;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: 60px 60px;
}
.ring-svg .prog.white { stroke: #FFFFFF; }
.ring-val {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.55rem; font-weight: 800; letter-spacing: -0.04em; color: #fff;
}
.ring-cap { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #8A8A8A; font-weight: 650; }

.badge {
  display: inline-block;
  padding: 0.18rem 0.62rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  margin-right: 0.3rem;
}
.b-supported { background: #16A34A; color: #05140A; }
.b-likely { background: #4ADE80; color: #052E16; }
.b-conflicted { background: #FF6A12; color: #0A0A0A; }
.b-unlikely { background: #9A3412; color: #FFE8DC; }
.b-unsupported { background: #7F1D1D; color: #FFE4E4; }
.b-notenough, .b-not { background: #262626; color: #E5E5E5; }
.b-high { background: #FF6A12; color: #0A0A0A; }
.b-medium { background: #404040; color: #F4F4F4; }
.b-low { background: #171717; color: #A3A3A3; border: 1px solid #3F3F3F; }
.b-support { background: #14532D; color: #DCFCE7; }
.b-contradict { background: #7F1D1D; color: #FEE2E2; }
.b-unrelated { background: #262626; color: #D4D4D4; }

.stage { display: flex; gap: 0.4rem; flex-wrap: wrap; margin: 0.15rem 0 0.95rem; }
.stage span {
  border: 1px solid #2A2A2A;
  background: #141414;
  padding: 0.28rem 0.62rem;
  border-radius: 999px;
  font-size: 0.74rem;
  color: #D4D4D4;
  font-weight: 650;
}
.stage span:nth-child(odd) { background: #FF6A12; color: #0A0A0A; border-color: #FF6A12; }

.trace-step { border-left: 3px solid #FF6A12; padding: 0.15rem 0 0.15rem 0.9rem; }

[data-testid="stMetric"] {
  background:
    radial-gradient(160px 100px at 110% 120%, rgba(255,106,18,0.3), transparent 60%),
    #141414;
  border: 1px solid #1F1F1F;
  border-radius: 16px;
  padding: 0.75rem 0.9rem;
}
[data-testid="stMetricValue"] {
  color: #FFFFFF !important;
  font-family: Outfit, sans-serif;
  font-weight: 800 !important;
}
[data-testid="stMetricLabel"] { color: #8A8A8A !important; }

.stChatMessage { background: #141414 !important; border-radius: 16px; border: 1px solid #1F1F1F; }
div[data-testid="stChatInput"] textarea { color: #F4F4F4 !important; }

.stButton > button {
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-family: Outfit, sans-serif !important;
}
.stButton > button[kind="primary"] {
  background: #FF6A12 !important;
  color: #0A0A0A !important;
  border: none !important;
}
.stButton > button[kind="secondary"] {
  background: #141414 !important;
  color: #F4F4F4 !important;
  border: 1px solid #2A2A2A !important;
}

[data-testid="stDataFrame"] { border: 1px solid #1F1F1F; border-radius: 14px; overflow: hidden; }
hr { border-color: #1F1F1F !important; }
.small { color: #A3A3A3; font-size: 0.86rem; line-height: 1.5; }
.small b { color: #FFFFFF; }

div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input {
  background: #141414 !important;
  color: #F4F4F4 !important;
  border-radius: 12px !important;
}
"""


def badge(status: str) -> str:
    key = (status or "").lower().replace(" ", "").replace("enough", "enough")
    mapping = {
        "supported": "b-supported",
        "likely": "b-likely",
        "conflicted": "b-conflicted",
        "unlikely": "b-unlikely",
        "unsupported": "b-unsupported",
        "notenoughevidence": "b-notenough",
        "high": "b-high",
        "medium": "b-medium",
        "low": "b-low",
        "support": "b-support",
        "contradict": "b-contradict",
        "unrelated": "b-unrelated",
    }
    cls = mapping.get(key, "b-not")
    return f'<span class="badge {cls}">{status}</span>'
