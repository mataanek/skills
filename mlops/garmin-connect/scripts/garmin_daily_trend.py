#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime
import os

LAKE_PATH = "/home/mataanek/.hermes/data/garmin_lake/daily.parquet"
WIKI_PATH = "/home/mataanek/.hermes/wiki/personal/health.md"
TREND_SECTION_HEADER = "## Daily Resting HR vs High-Intensity Run Trend (Garmin)\n"

def load_lake():
    df = pd.read_parquet(LAKE_PATH)
    df['date'] = pd.to_datetime(df['date'])
    return df

def compute_daily_series(df):
    # Keep date, resting HR, high intensity minutes
    series = df[['date', 'resting_hr_bpm', 'high_intensity_run_min']].copy()
    # Sort by date
    series = series.sort_values('date')
    # Compute rolling correlation (30-day window)
    # Need at least 2 observations
    window = 30
    series['rolling_corr'] = series['resting_hr_bpm'].rolling(window).corr(series['high_intensity_run_min'])
    # For days where insufficient data, NaN
    return series

def format_trend_section(series):
    lines = []
    lines.append(TREND_SECTION_HEADER)
    lines.append(f"Analysis run at: {datetime.now().isoformat()}\n")
    lines.append(f"Total days: {len(series)}\n")
    lines.append("Showing last 14 days with rolling 30-day correlation between resting HR and high-intensity run minutes:\n")
    lines.append("Date | Resting HR (bpm) | High-Intensity Min | 30d Corr\n")
    lines.append("-----|------------------|--------------------|---------\n")
    # Get last 14 rows
    recent = series.tail(14)
    for _, row in recent.iterrows():
        date_str = row['date'].date().isoformat()
        hr = f"{row['resting_hr_bpm']:.1f}" if pd.notna(row['resting_hr_bpm']) else "N/A"
        intensity = f"{row['high_intensity_run_min']:.1f}" if pd.notna(row['high_intensity_run_min']) else "0"
        corr = f"{row['rolling_corr']:.3f}" if pd.notna(row['rolling_corr']) else "N/A"
        lines.append(f"{date_str} | {hr} | {intensity} | {corr}\n")
    # Overall interpretation based on latest correlation
    latest_corr = series['rolling_corr'].iloc[-1]
    lines.append("\nLatest 30-day correlation: ")
    if pd.isna(latest_corr):
        lines.append("Insufficient data\n")
    else:
        lines.append(f"{latest_corr:.3f}\n")
        lines.append("Interpretation: ")
        if abs(latest_corr) < 0.3:
            lines.append("weak\n")
        elif abs(latest_corr) < 0.7:
            lines.append("moderate\n")
        else:
            lines.append("strong\n")
        lines.append(f"(Negative correlation suggests higher running volume associated with lower resting HR, indicating improved fitness.)\n")
    return "".join(lines)

def update_wiki(new_section):
    if os.path.exists(WIKI_PATH):
        with open(WIKI_PATH, 'r') as f:
            content = f.read()
    else:
        content = ""
    # Remove any existing section with same header
    import re
    pattern = re.compile(r'\n## Daily Resting HR vs High-Intensity Run Trend \(Garmin\b.*?\n(?:(?!\n## ).)*', re.DOTALL)
    content = pattern.sub('', content)
    content = content.rstrip() + "\n"
    content += new_section
    with open(WIKI_PATH, 'w') as f:
        f.write(content)

def main():
    df = load_lake()
    series = compute_daily_series(df)
    section = format_trend_section(series)
    update_wiki(section)
    print("Daily trend section updated in health wiki.")

if __name__ == "__main__":
    main()