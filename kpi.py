"""
kpi.py — KPI computation layer

Computes all aggregations needed by the dashboard:
  - Top-line KPIs (total revenue, profit, margin, units)
  - Monthly trend
  - Revenue by region / category / channel
  - Year-over-year growth
  - Margin heatmap pivot
"""

import pandas as pd
import config


def compute(df: pd.DataFrame) -> dict:
    total_rev    = df["revenue"].sum()
    total_profit = df["profit"].sum()
    avg_margin   = df["margin_pct"].mean()
    total_units  = df["units"].sum()

    monthly_rev  = df.groupby("month")["revenue"].sum()
    rev_by_region= df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    rev_by_cat   = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    rev_by_ch    = df.groupby("channel")["revenue"].sum()
    profit_by_cat= df.groupby("category")["profit"].sum().sort_values(ascending=False)

    margin_heatmap = df.pivot_table(
        values="margin_pct", index="region",
        columns="category", aggfunc="mean",
    )

    yoy = df.groupby(["year", "category"])["revenue"].sum().unstack()

    # MoM growth
    mom_growth = monthly_rev.pct_change().dropna() * 100

    return {
        "total_rev":      total_rev,
        "total_profit":   total_profit,
        "avg_margin":     avg_margin,
        "total_units":    total_units,
        "monthly_rev":    monthly_rev,
        "rev_by_region":  rev_by_region,
        "rev_by_cat":     rev_by_cat,
        "rev_by_ch":      rev_by_ch,
        "profit_by_cat":  profit_by_cat,
        "margin_heatmap": margin_heatmap,
        "yoy":            yoy,
        "mom_growth":     mom_growth,
    }


def print_summary(kpis: dict) -> None:
    print("\n  ── KPI Summary ──────────────────────────────────")
    print(f"  Total Revenue  : ${kpis['total_rev']/1e9:.3f}B")
    print(f"  Total Profit   : ${kpis['total_profit']/1e9:.3f}B")
    print(f"  Avg Margin     : {kpis['avg_margin']:.1f}%  "
          f"(target {config.TARGET_MARGIN_PCT}%)")
    print(f"  Total Units    : {kpis['total_units']:,}")
    print(f"\n  Revenue by Region:")
    for reg, rev in kpis["rev_by_region"].items():
        print(f"    {reg:<10} ${rev/1e9:.3f}B")
