"""
data_gen.py — Multi-dimensional synthetic sales dataset (2 years, 4 regions)
"""
import math
import numpy as np
import pandas as pd
import config


def generate() -> pd.DataFrame:
    np.random.seed(config.SEED)
    months = pd.date_range(config.START_DATE, periods=config.N_MONTHS, freq="MS")
    rows   = []

    for month in months:
        for region in config.REGIONS:
            for cat in config.CATEGORIES:
                for ch in config.CHANNELS:
                    base     = np.random.randint(50_000, 300_000)
                    trend    = (months.get_loc(month) / len(months)) * 35_000
                    seasonal = 22_000 * math.sin(2 * math.pi * month.month / 12)
                    revenue  = round(base + trend + seasonal + np.random.normal(0, 6_000), 2)
                    units    = int(revenue / np.random.uniform(200, 800))
                    cost     = round(revenue * np.random.uniform(0.44, 0.66), 2)
                    rows.append({
                        "month":    month,
                        "region":   region,
                        "category": cat,
                        "channel":  ch,
                        "revenue":  revenue,
                        "units":    units,
                        "cost":     cost,
                        "profit":   round(revenue - cost, 2),
                        "year":     month.year,
                        "quarter":  f"Q{month.quarter}",
                    })

    df = pd.DataFrame(rows)
    df["margin_pct"] = (df["profit"] / df["revenue"] * 100).round(1)
    print(f"Generated {len(df):,} rows  |  "
          f"Total revenue: ${df['revenue'].sum()/1e9:.2f}B")
    return df
