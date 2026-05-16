"""Brand palette and shared styling constants."""

# ── Core palette ──────────────────────────────────────────────────────────────
DB_NAVY      = "#003F63"   # Primary — Pantone 2955 C
DB_BLUE      = "#005E8E"   # Mid blue — interactive elements
DB_LIGHT     = "#E8F1F8"   # Tint of primary for panel backgrounds
DB_WHITE     = "#FFFFFF"
DB_OFFWHITE  = "#F4F7FA"   # Page background
DB_BORDER    = "#D0DCE8"   # Card borders and dividers
DB_TEXT      = "#1A2B3C"   # Primary text — ~17:1 on white
DB_MUTED     = "#4B5563"   # Secondary text — ~8:1 on white (was #6B7A8D at ~4.1:1)

# ── Semantic colours ──────────────────────────────────────────────────────────
DB_GREEN     = "#1B7340"   # Positive / on track
DB_AMBER     = "#B76E00"   # Caution / approaching target
DB_RED       = "#B5221B"   # At risk / below target
DB_GREEN_BG  = "#EAF5EE"
DB_AMBER_BG  = "#FDF3E3"
DB_RED_BG    = "#FAEAEA"

# ── Chart colour sequence ─────────────────────────────────────────────────────
MARKET_COLORS = {
    "Denmark": DB_NAVY,
    "Sweden":  DB_BLUE,
    "Finland": "#00839E",
    "Norway":  "#6BBBCA",
}

SEGMENT_COLORS = [DB_NAVY, DB_BLUE, "#6BBBCA"]

# ── Plotly layout base ────────────────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor=DB_WHITE,
    plot_bgcolor=DB_WHITE,
    font=dict(family="Inter, Arial, sans-serif", color=DB_TEXT, size=13),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        font=dict(size=12, color=DB_TEXT),
    ),
    xaxis=dict(
        showgrid=False, linecolor=DB_BORDER, tickcolor=DB_BORDER,
        tickfont=dict(color=DB_TEXT, size=12),
    ),
    yaxis=dict(
        gridcolor=DB_BORDER, linecolor=DB_BORDER, tickcolor=DB_BORDER,
        tickfont=dict(color=DB_TEXT, size=12),
    ),
)

# ── Streamlit CSS injection ───────────────────────────────────────────────────
PAGE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Force light mode everywhere */
:root {{ color-scheme: light !important; }}

html, body, [class*="css"] {{
    font-family: 'Inter', Arial, sans-serif;
    background-color: {DB_OFFWHITE} !important;
    color: {DB_TEXT} !important;
}}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, section.main {{
    background-color: {DB_OFFWHITE} !important;
}}

[data-testid="stSidebar"] {{
    background-color: {DB_WHITE} !important;
}}

/* ── Tab bar ── */
[data-testid="stTabs"] {{
    border-bottom: 2px solid {DB_BORDER};
    margin-bottom: 4px;
}}

[data-testid="stTabs"] button {{
    font-family: 'Inter', Arial, sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: {DB_TEXT} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 18px !important;
    margin-bottom: -2px;
    border-radius: 0 !important;
    transition: color 0.15s ease, border-color 0.15s ease;
}}

[data-testid="stTabs"] button:hover {{
    color: {DB_NAVY} !important;
    background: {DB_LIGHT} !important;
}}

[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {DB_NAVY} !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {DB_NAVY} !important;
    background: transparent !important;
}}

[data-testid="stTabs"] button p {{
    font-size: 0.85rem !important;
    color: inherit !important;
}}

/* ── Top header bar ── */
.db-header {{
    background-color: {DB_NAVY};
    color: white;
    padding: 18px 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}}
.db-header h1 {{
    margin: 0;
    font-size: 1.35rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: white;
}}
.db-header .subtitle {{
    font-size: 0.82rem;
    opacity: 0.7;
    font-weight: 300;
    color: white;
    margin-top: 3px;
}}

/* ── KPI cards ── */
.kpi-card {{
    background: {DB_WHITE};
    border: 1px solid {DB_BORDER};
    border-radius: 8px;
    padding: 18px 20px;
    height: 100%;
}}
.kpi-card .label {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {DB_MUTED};
    margin-bottom: 6px;
}}
.kpi-card .value {{
    font-size: 1.9rem;
    font-weight: 700;
    color: {DB_TEXT};
    line-height: 1.1;
}}
.kpi-card .delta {{
    font-size: 0.8rem;
    margin-top: 4px;
    font-weight: 600;
    color: {DB_TEXT};
}}
.kpi-card .target-line {{
    font-size: 0.76rem;
    color: {DB_MUTED};
    margin-top: 4px;
}}

/* ── Section headers ── */
.section-header {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {DB_NAVY};
    padding: 14px 0 8px 0;
    border-bottom: 1.5px solid {DB_BORDER};
    margin-bottom: 16px;
}}

/* ── RAG badges ── */
.rag-on   {{ color: {DB_GREEN}; background: {DB_GREEN_BG}; padding: 2px 9px; border-radius: 4px; font-size: 0.73rem; font-weight: 700; }}
.rag-watch {{ color: {DB_AMBER}; background: {DB_AMBER_BG}; padding: 2px 9px; border-radius: 4px; font-size: 0.73rem; font-weight: 700; }}
.rag-risk  {{ color: {DB_RED};   background: {DB_RED_BG};   padding: 2px 9px; border-radius: 4px; font-size: 0.73rem; font-weight: 700; }}

/* ── Action table ── */
.action-table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
.action-table th {{
    background: {DB_NAVY};
    color: {DB_WHITE};
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 10px 14px;
    text-align: left;
}}
.action-table td {{ padding: 10px 14px; border-bottom: 1px solid {DB_BORDER}; vertical-align: top; color: {DB_TEXT}; font-size: 0.84rem; }}
.action-table tr:hover td {{ background: {DB_LIGHT}; color: {DB_TEXT}; }}

/* ── Status pills ── */
.status-done      {{ color: {DB_GREEN}; background: {DB_GREEN_BG}; padding: 3px 9px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; white-space: nowrap; }}
.status-progress  {{ color: {DB_AMBER}; background: {DB_AMBER_BG}; padding: 3px 9px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; white-space: nowrap; }}
.status-notstart  {{ color: {DB_TEXT};  background: {DB_BORDER};   padding: 3px 9px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; white-space: nowrap; }}

/* ── Progress bars ── */
.progress-wrap {{ background: {DB_BORDER}; border-radius: 100px; height: 5px; margin-top: 10px; overflow: hidden; }}
.progress-fill       {{ height: 5px; border-radius: 100px; background: {DB_NAVY}; }}
.progress-fill-warn  {{ height: 5px; border-radius: 100px; background: {DB_AMBER}; }}
.progress-fill-risk  {{ height: 5px; border-radius: 100px; background: {DB_RED}; }}

/* ── Card panels ── */
.panel {{
    background: {DB_WHITE};
    border: 1px solid {DB_BORDER};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 24px 40px 24px !important; max-width: 1280px; }}
div[data-testid="stDecoration"] {{ display: none; }}
div[data-testid="stToolbar"] {{ display: none; }}
</style>
"""


def rag_badge(status: str) -> str:
    mapping = {"On Track": "rag-on", "Watch": "rag-watch", "At Risk": "rag-risk"}
    return f'<span class="{mapping.get(status, "rag-watch")}">{status}</span>'


def status_pill(status: str) -> str:
    mapping = {
        "Completed":   "status-done",
        "In progress": "status-progress",
        "Not started": "status-notstart",
    }
    return f'<span class="{mapping.get(status, "status-notstart")}">{status}</span>'


def progress_bar(pct: float, color: str = "default") -> str:
    pct = min(max(pct, 0), 100)
    cls = "progress-fill"
    if color == "warn":
        cls = "progress-fill-warn"
    elif color == "risk":
        cls = "progress-fill-risk"
    return f'<div class="progress-wrap"><div class="{cls}" style="width:{pct:.1f}%"></div></div>'
