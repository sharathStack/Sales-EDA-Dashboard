"""
main.py — Sales EDA Dashboard entry point

Run order:
  1. Generate 2-year multi-dimensional sales dataset
  2. Compute all KPIs (revenue, profit, margin, YoY, etc.)
  3. Print KPI summary to terminal
  4. Render full Power BI-style 8-panel dashboard
"""

import config
from data_gen  import generate
from kpi       import compute, print_summary
from dashboard import plot


def main():
    print("=" * 55)
    print("  SALES EDA DASHBOARD  —  Power BI Style")
    print("=" * 55)

    print("\n[1] Generating sales data...")
    df = generate()

    print("\n[2] Computing KPIs...")
    kpis = compute(df)
    print_summary(kpis)

    print("\n[3] Rendering dashboard...")
    plot(kpis)

    print("\n  Done ✓")


if __name__ == "__main__":
    main()
