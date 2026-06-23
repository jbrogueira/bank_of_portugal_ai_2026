from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

cpi = pd.read_csv(ROOT / "data/raw/cpi.csv", comment="#",
                  parse_dates=["observation_date"])
cpi = cpi.sort_values("observation_date").reset_index(drop=True)

# Index by month so the 12-period lag is by calendar date, not row position.
# A missing month (e.g. 2025-10) then aligns to NaN instead of silently
# shifting every later observation's reference point.
s = cpi.set_index(
    pd.PeriodIndex(cpi["observation_date"], freq="M"))["CPIAUCSL"]
s = s.asfreq("M")  # make any gap explicit as NaN

# year-over-year inflation: 12 months for monthly data
yoy = 100 * (s / s.shift(12) - 1)

out = yoy.rename("value").reset_index()
out["date"] = out["observation_date"].dt.to_timestamp()
out["series"] = "cpi_yoy"
out = out.dropna(subset=["value"])

# long format: one row per (date, series, value)
long = out[["date", "series", "value"]]
long.to_csv(ROOT / "data/processed/inflation.csv", index=False)

# quick look at the most recent year
print(long.tail(12).to_string(index=False))
