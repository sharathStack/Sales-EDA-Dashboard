"""
dashboard.py — Power BI–style 8-panel matplotlib sales dashboard

Panels:
  Row 0: 4 × KPI cards  (Revenue, Profit, Margin, Units)
  Row 1: Monthly trend  |  Region bar  |  Channel pie
  Row 2: Category profit bar  |  Margin heatmap  |  YoY comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import config

BG      = "#F0F4F8"
CARD_BG = "#FFFFFF"
C1  = "#2563EB"   # blue
C2  = "#10B981"   # green
C3  = "#F59E0B"   # amber
C4  = "#EF4444"   # red
C5  = "#8B5CF6"   # purple
TXT = "#1E293B"
SUB = "#64748B"


def _style(ax):
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TXT, labelsize=8)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color("#E2E8F0")
    ax.grid(axis="y", alpha=0.25, color="#E2E8F0")
    ax.title.set_color(TXT)
    ax.title.set_fontweight("bold")
    ax.title.set_fontsize(9)
    ax.xaxis.label.set_color(SUB)
    ax.yaxis.label.set_color(SUB)


def _money(x, _): return f"${x/1e6:.0f}M"
def _pct(x, _):   return f"{x:.1f}%"


def plot(kpis: dict) -> None:
    fig = plt.figure(figsize=(22, 13), facecolor=BG)
    fig.suptitle("Sales Performance Dashboard  │  2023–2024",
                 fontsize=16, fontweight="bold", color=TXT, y=0.99)

    gs = gridspec.GridSpec(
        3, 4, figure=fig,
        hspace=0.52, wspace=0.36,
        top=0.94, bottom=0.05, left=0.04, right=0.97,
    )

    # ── KPI cards ─────────────────────────────────────────────────────────────
    kpi_data = [
        (f"${kpis['total_rev']/1e9:.2f}B",   "Total Revenue",  C1, "FY 2023-2024"),
        (f"${kpis['total_profit']/1e9:.2f}B","Total Profit",   C2, "Gross profit"),
        (f"{kpis['avg_margin']:.1f}%",        "Avg Margin",     C3,
         f"Target: {config.TARGET_MARGIN_PCT}%"),
        (f"{kpis['total_units']/1e6:.1f}M",  "Units Sold",     C4, "All channels"),
    ]
    for i, (val, label, color, sub) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(CARD_BG)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.add_patch(plt.Rectangle((0,0), 1, 1, transform=ax.transAxes,
                                    fill=False, edgecolor=color, linewidth=2.5))
        ax.text(0.5, 0.65, val,   transform=ax.transAxes, ha="center",
                fontsize=20, fontweight="bold", color=color)
        ax.text(0.5, 0.35, label, transform=ax.transAxes, ha="center",
                fontsize=9,  color=TXT)
        ax.text(0.5, 0.12, sub,   transform=ax.transAxes, ha="center",
                fontsize=7.5, color=SUB)

    # ── Monthly revenue trend ─────────────────────────────────────────────────
    ax_trend = fig.add_subplot(gs[1, :2])
    _style(ax_trend)
    x = range(len(kpis["monthly_rev"]))
    ax_trend.plot(list(x), kpis["monthly_rev"].values, color=C1,
                   linewidth=2.2, label="Monthly Revenue")
    ax_trend.fill_between(list(x), kpis["monthly_rev"].values, alpha=0.10, color=C1)
    ax_trend.axhline(config.TARGET_REVENUE_M * 1e6, color=C3, linewidth=1.2,
                      linestyle="--", alpha=0.7, label=f"Target ${config.TARGET_REVENUE_M}M")
    ax_trend.yaxis.set_major_formatter(mticker.FuncFormatter(_money))
    ax_trend.set_title("Monthly Revenue Trend")
    ax_trend.set_xticks(list(x)[::3])
    ax_trend.set_xticklabels(
        [d.strftime("%b %y") for d in kpis["monthly_rev"].index[::3]],
        rotation=25, fontsize=7,
    )
    ax_trend.legend(fontsize=8)

    # ── Revenue by region ─────────────────────────────────────────────────────
    ax_reg = fig.add_subplot(gs[1, 2])
    _style(ax_reg)
    rb = kpis["rev_by_region"]
    bars = ax_reg.barh(rb.index, rb.values / 1e9, color=[C1,C2,C3,C4], alpha=0.85)
    ax_reg.set_title("Revenue by Region ($B)")
    ax_reg.set_xlabel("$B")
    ax_reg.invert_yaxis()
    for bar, v in zip(bars, rb.values / 1e9):
        ax_reg.text(v + 0.01, bar.get_y() + bar.get_height()/2,
                    f"{v:.2f}B", va="center", fontsize=8)

    # ── Channel mix pie ───────────────────────────────────────────────────────
    ax_pie = fig.add_subplot(gs[1, 3])
    ax_pie.set_facecolor(CARD_BG)
    rc = kpis["rev_by_ch"]
    wedges, texts, autos = ax_pie.pie(
        rc.values, labels=rc.index, autopct="%1.0f%%",
        colors=[C1, C2, C3], startangle=90,
        textprops={"fontsize": 9},
    )
    for at in autos: at.set_fontsize(9)
    ax_pie.set_title("Revenue by Channel", fontweight="bold", color=TXT, fontsize=9)

    # ── Profit by category ────────────────────────────────────────────────────
    ax_cat = fig.add_subplot(gs[2, 0])
    _style(ax_cat)
    pc = kpis["profit_by_cat"]
    ax_cat.bar(pc.index, pc.values / 1e9, color=C2, alpha=0.85)
    ax_cat.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:.1f}B"))
    ax_cat.set_title("Profit by Category ($B)")
    ax_cat.tick_params(axis="x", rotation=18)

    # ── Margin heatmap ────────────────────────────────────────────────────────
    ax_hm = fig.add_subplot(gs[2, 1])
    ax_hm.set_facecolor(CARD_BG)
    sns.heatmap(kpis["margin_heatmap"], ax=ax_hm, cmap="YlGn",
                annot=True, fmt=".1f", cbar_kws={"shrink": 0.80},
                linewidths=0.4, annot_kws={"size": 8})
    ax_hm.set_title("Avg Margin % by Region & Category", fontweight="bold",
                     fontsize=9, color=TXT)
    ax_hm.tick_params(axis="x", rotation=22, labelsize=7.5)
    ax_hm.tick_params(axis="y", labelsize=7.5)

    # ── YoY revenue comparison ────────────────────────────────────────────────
    ax_yoy = fig.add_subplot(gs[2, 2:])
    _style(ax_yoy)
    yoy    = kpis["yoy"]
    cats   = yoy.columns.tolist()
    x      = np.arange(len(cats))
    years  = sorted(yoy.index.tolist())
    yoy_colors = [C1, C2]
    for j, (yr, col) in enumerate(zip(years, yoy_colors)):
        offset = -0.2 + j * 0.38
        ax_yoy.bar(x + offset, yoy.loc[yr] / 1e9, 0.36,
                   label=str(yr), color=col, alpha=0.85)
    ax_yoy.set_xticks(x)
    ax_yoy.set_xticklabels(cats, rotation=15, fontsize=8.5)
    ax_yoy.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"${v:.1f}B"))
    ax_yoy.set_title("Year-over-Year Revenue by Category ($B)")
    ax_yoy.legend(fontsize=9)

    plt.savefig(config.CHART_OUTPUT, dpi=config.CHART_DPI,
                bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Dashboard saved → {config.CHART_OUTPUT}")
