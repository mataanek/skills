---
name: garmin-data-lake
description: Build a daily-level Parquet data lake from Garmin Connect export for health and workout trend analysis.
category: mlops
---

**Description:** Build a daily-level Parquet data lake from Garmin Connect export (wellness, sleep, summarized activities) for health and workout trend analysis. Includes token verification, lake creation, trend scripts, and optional plotting.

**Prerequisites:**
- Garmin export JSON files under `/home/mataanek/.hermes/wiki/raw/garmin/`.
- Valid Garmin Connect tokens in `/home/mataanek/.hermes/.garminconnect/` (oauth1_token.json with non-empty csrf_token, oauth2_token.json with future expires_at).
- Python 3.8+ with pandas, pyarrow, matplotlib installed.

**Workflow:**
1. **Verify Tokens** – run `python3 scripts/verify_garmin_tokens.py` (or manually check files).
2. **Build Lake** – execute `scripts/build_lake.py` to produce `/home/mataanek/.hermes/data/garmin_lake/daily.parquet`.
3. **Update Trends** – run `scripts/garmin_trend.py` for weekly correlation or `scripts/garmin_daily_trend.py` for daily rolling correlation to update `/home/mataanek/.hermes/wiki/personal/health.md`.
4. **Optional Plots** – use `scripts/plot_resting_hr.py` or `scripts/plot_resting_hr_v2.py` for visualizations.

**Key Files:**
- `scripts/build_lake.py` – extracts and aggregates JSON into daily Parquet.
- `scripts/garmin_trend.py` – computes correlation and updates wiki.
- `scripts/plot_resting_hr.py` – generates resting HR time‑series plot.
- `scripts/verify_garmin_tokens.py` – validates token freshness and correctness.
- `references/token_verification.md` – details on token checks and common pitfalls.

**Pitfalls:**
- Empty `csrf_token` or `expires_at: 0` → token refresh fails → 403 Forbidden on HR endpoints.
- Missing wellness/sleep entries for certain dates → NaN in lake (expected; handled by trend scripts). This can cause gaps in plots (e.g., missing resting HR in May 2024) which reflect missing source data, not logging errors.
- Ensure activity files are labeled with correct `activityType` (e.g., "running") for intensity detection.

## Notes:
- The lake is updated incrementally; re‑run the build script when new JSON files appear.
- Trend analysis uses rolling windows; adjust window size in the script if needed.
- All outputs are stored under the user's wiki and data lake for reproducibility.
- For live API polling, see the `garmin-connect` skill; for historical analysis, use this lake.
