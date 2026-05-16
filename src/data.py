"""Synthetic data engine anchored to Danske Bank Forward'28 public targets."""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

# ── Forward'28 targets (public) ───────────────────────────────────────────────
TARGETS_2028 = {
    "roe":            14.5,   # %
    "cost_income":    43.0,   # %
    "total_income":   63.0,   # DKK bn
    "cet1":           16.0,   # %
    "aum":            1_200,  # DKK bn (estimated 2028 from 1,010 in Q1 2026 at 7% pa)
    "nnm_annual":     35,     # DKK bn net new money per year
}

ACTUALS_Q1_2026 = {
    "roe":            13.0,
    "cost_income":    46.0,
    "total_income":   57.0,
    "cet1":           15.5,
    "aum":            1_010,
    "nnm_q1":         6.0,
}

MARKETS = ["Denmark", "Sweden", "Finland", "Norway"]
MARKET_WEIGHTS = [0.48, 0.26, 0.14, 0.12]    # AUM share by market

QUARTERS = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Q2 2025",
            "Q3 2025", "Q4 2025", "Q1 2026"]


def generate_aum_history() -> pd.DataFrame:
    """AUM and net new money by quarter, by market."""
    base_total = 890
    rows = []
    for i, q in enumerate(QUARTERS):
        total = base_total * (1.07 ** (i / 4)) + RNG.normal(0, 8)
        for market, w in zip(MARKETS, MARKET_WEIGHTS):
            noise = RNG.normal(0, w * total * 0.02)
            rows.append({
                "quarter": q,
                "market": market,
                "aum": round(total * w + noise, 1),
                "nnm": round(RNG.normal(w * 6, w * 2), 2),
            })
    return pd.DataFrame(rows)


def generate_kpi_history() -> pd.DataFrame:
    """Quarterly group-level KPIs with noise around a linear path to 2028 targets."""
    rows = []
    for i, q in enumerate(QUARTERS):
        t = i / 16   # fraction toward end of 2028
        rows.append({
            "quarter": q,
            "roe":          round(13.0 + t * 1.5 + RNG.normal(0, 0.3), 2),
            "cost_income":  round(46.0 - t * 3.0 + RNG.normal(0, 0.4), 2),
            "total_income": round(57.0 + t * 6.0 + RNG.normal(0, 0.5), 2),
            "cet1":         round(15.5 + t * 0.5 + RNG.normal(0, 0.1), 2),
        })
    return pd.DataFrame(rows)


def generate_commercial_metrics() -> pd.DataFrame:
    """Advisory penetration, insurance penetration, lending growth by market and quarter."""
    rows = []
    base = {
        "Denmark":  {"advisory_pct": 62, "insurance_pct": 34, "lending_growth": 3.1},
        "Sweden":   {"advisory_pct": 54, "insurance_pct": 28, "lending_growth": 2.8},
        "Finland":  {"advisory_pct": 49, "insurance_pct": 24, "lending_growth": 2.2},
        "Norway":   {"advisory_pct": 57, "insurance_pct": 31, "lending_growth": 3.4},
    }
    for i, q in enumerate(QUARTERS):
        for market, b in base.items():
            rows.append({
                "quarter": q,
                "market": market,
                "advisory_pct":  round(b["advisory_pct"] + i * 0.4 + RNG.normal(0, 0.5), 1),
                "insurance_pct": round(b["insurance_pct"] + i * 0.3 + RNG.normal(0, 0.4), 1),
                "lending_growth": round(b["lending_growth"] + RNG.normal(0, 0.2), 2),
            })
    return pd.DataFrame(rows)


def generate_client_segments() -> pd.DataFrame:
    """Client count and AUM by segment (DKK threshold bands)."""
    return pd.DataFrame([
        {"segment": "Private Banking (>5M DKK)",    "clients": 8_420,  "aum_share": 52},
        {"segment": "Affluent (1–5M DKK)",           "clients": 31_200, "aum_share": 32},
        {"segment": "Mass Affluent (0.5–1M DKK)",    "clients": 74_500, "aum_share": 16},
    ])


def generate_actions() -> pd.DataFrame:
    """Simulated meeting action log."""
    today = pd.Timestamp("2026-05-16")
    return pd.DataFrame([
        {"action": "Finalise Q1 2026 NNM deep-dive for Group ExCo", "owner": "PB Analytics",  "due": "2026-05-23", "status": "In progress"},
        {"action": "Update Aladdin advisory penetration report for SE/FI launch", "owner": "Investment Products", "due": "2026-05-30", "status": "Not started"},
        {"action": "Prepare Forward'28 mid-year strategy review deck", "owner": "Execution Office", "due": "2026-06-13", "status": "In progress"},
        {"action": "Review insurance cross-sell targets for NO market", "owner": "Wealth Planning", "due": "2026-05-28", "status": "Completed"},
        {"action": "Align KPI dashboard with Group Finance definitions", "owner": "PB Analytics", "due": "2026-06-06", "status": "In progress"},
        {"action": "Draft client segmentation framework update (post-Aladdin)", "owner": "Investment Products", "due": "2026-06-20", "status": "Not started"},
        {"action": "Stakeholder alignment: lending penetration targets DK", "owner": "Private Banking DK", "due": "2026-05-21", "status": "Completed"},
        {"action": "Prepare NNM variance analysis Q1 vs plan", "owner": "PB Analytics", "due": "2026-05-20", "status": "Completed"},
    ])
