"""Synthetic data engine anchored to publicly disclosed Forward'28 strategy targets."""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

# ── Forward'28 targets (announced April 2026) ────────────────────────────────
TARGETS_2028 = {
    "roe":            14.5,   # % — >14.5% target
    "cost_income":    43.0,   # % — ≤43% target
    "total_income":   63.0,   # DKK bn — group total income target
    "cet1":           16.0,   # % — operating target (~16%); direction is lower from current 17.3%
    "aum":            1_350,  # DKK bn — estimated 2028 from ~1,012bn end-2025 at ~7% pa
    "nnm_annual":     35,     # DKK bn — management target; not published as reported metric
}

# Anchored to FY 2025 actuals (Fact Book Q4 2025, published February 2026)
ACTUALS_Q1_2026 = {
    "roe":            13.3,   # % — FY 2025 group ROE
    "cost_income":    45.5,   # % — FY 2025 group cost/income ratio
    "total_income":   56.8,   # DKK bn — FY 2025 group total income (estimate)
    "cet1":           17.3,   # % — FY 2025 group CET1; target is lower (~16%)
    "aum":            1_012,  # DKK bn — group-wide AUM end-2025 (>DKK 1tn per Q4 2025 results)
    "nnm_q1":         6.0,    # DKK bn — synthetic; not published by group
}

MARKETS = ["Denmark", "Sweden", "Finland", "Norway"]
# Weights derived from FY 2024 net interest income split (Fact Book Q4 2024, p.28)
# DK 8,988m / SE 806m / FI 2,253m / NO 512m (Norway divested Q4 2024; kept illustrative)
MARKET_WEIGHTS = [0.65, 0.18, 0.12, 0.05]

QUARTERS = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025", "Q2 2025",
            "Q3 2025", "Q4 2025", "Q1 2026"]


def generate_aum_history() -> pd.DataFrame:
    """AUM and net new money by quarter, by market.

    Base calibrated to group-wide AUM of ~DKK 883bn in Q1 2024, growing at ~7% pa
    to reach ~DKK 1,012bn by end-2025 (per Q4 2025 earnings results).
    NNM is synthetic — not published as a reported metric.
    """
    base_total = 883
    rows = []
    for i, q in enumerate(QUARTERS):
        total = base_total * (1.07 ** (i / 4)) + RNG.normal(0, 7)
        for market, w in zip(MARKETS, MARKET_WEIGHTS):
            noise = RNG.normal(0, w * total * 0.015)
            rows.append({
                "quarter": q,
                "market": market,
                "aum": round(total * w + noise, 1),
                "nnm": round(RNG.normal(w * 8, w * 1.8), 2),
            })
    return pd.DataFrame(rows)


def generate_kpi_history() -> pd.DataFrame:
    """Quarterly group-level KPIs anchored to FY 2024/2025 actuals, trending toward 2028 targets.

    FY 2024 actuals (Fact Book Q4 2024): ROE 13.4%, C/I 45.6%, total income 56.4bn, CET1 17.8%
    FY 2025 actuals (Fact Book Q4 2025): ROE 13.3%, C/I 45.5%, total income ~56.8bn, CET1 17.3%
    """
    rows = []
    for i, q in enumerate(QUARTERS):
        t = i / 16   # fraction toward end of 2028 (series runs Q1 2024 → Q1 2026)
        rows.append({
            "quarter": q,
            "roe":          round(13.3 + t * 1.2 + RNG.normal(0, 0.25), 2),
            "cost_income":  round(45.5 - t * 2.5 + RNG.normal(0, 0.35), 2),
            "total_income": round(56.8 + t * 6.2 + RNG.normal(0, 0.5), 2),
            "cet1":         round(17.5 - t * 1.5 + RNG.normal(0, 0.12), 2),
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
