"""US vs Portugal year-over-year inflation, monthly, common sample.

Inputs:
  data/raw/cpi.csv      US CPI (FRED CPIAUCSL, index 1982-84=100, seasonally adjusted)
  data/raw/hicp_pt.csv  Portugal HICP (Eurostat prc_hicp_midx, CP00, index 2015=100, NOT seasonally adjusted)

Outputs:
  data/processed/inflation_us_pt.csv          long format (date, country, yoy)
  data/processed/inflation_us_pt_by_decade.md markdown table: mean/sd/min/max by decade and country
  slides/assets/inflation_us_pt.png           two-line plot

Caveat: the US series is seasonally adjusted and the PT series is not. Year-over-year
differencing removes most seasonality, so the effect on the comparison is minor.
"""

import matplotlib.pyplot as plt
import pandas as pd

US_CSV = "data/raw/cpi.csv"
PT_CSV = "data/raw/hicp_pt.csv"


def yoy(index: pd.Series) -> pd.Series:
    """Year-over-year inflation in percent: 100 * (P_t / P_{t-12} - 1)."""
    return 100 * (index / index.shift(12) - 1)


def load(path: str, value_col: str) -> pd.Series:
    df = pd.read_csv(path, comment="#", parse_dates=["observation_date"])
    return df.sort_values("observation_date").set_index("observation_date")[value_col]


us = load(US_CSV, "CPIAUCSL")
pt = load(PT_CSV, "HICP_PT")

infl = pd.DataFrame({"US": yoy(us), "PT": yoy(pt)})

# Common sample: months where both series have a YoY value.
infl = infl.dropna(how="any")
print(f"Common sample: {infl.index.min():%Y-%m} to {infl.index.max():%Y-%m} "
      f"({len(infl)} months)")

# --- long format ---
long = (infl.rename_axis("date").reset_index()
        .melt(id_vars="date", var_name="country", value_name="yoy")
        .sort_values(["country", "date"]))
long.to_csv("data/processed/inflation_us_pt.csv", index=False)

# --- by-decade summary table ---
long["decade"] = (long["date"].dt.year // 10 * 10).astype(str) + "s"
summary = (long.groupby(["decade", "country"])["yoy"]
           .agg(mean="mean", sd="std", min="min", max="max")
           .round(2).reset_index())

header = "| Decade | Country | Mean | SD | Min | Max |\n|---|---|---|---|---|---|\n"
rows = "".join(
    f"| {r.decade} | {r.country} | {r.mean:.2f} | {r.sd:.2f} | "
    f"{r.min:.2f} | {r.max:.2f} |\n"
    for r in summary.itertuples()
)
md = (f"# US vs Portugal YoY inflation by decade\n\n"
      f"Common sample: {infl.index.min():%Y-%m} to {infl.index.max():%Y-%m}. "
      f"US = FRED CPIAUCSL (SA); PT = Eurostat HICP CP00 (NSA). Percent per year.\n\n"
      f"{header}{rows}")
with open("data/processed/inflation_us_pt_by_decade.md", "w") as f:
    f.write(md)
print(md)

# --- plot ---
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(infl.index, infl["US"], color="#1F3A68", lw=1.4, label="United States (CPI)")
ax.plot(infl.index, infl["PT"], color="#cc785c", lw=1.4, label="Portugal (HICP)")
ax.axhline(0, color="0.6", lw=0.6)
ax.set_ylabel("YoY inflation (%)")
ax.set_xlabel("")
ax.set_title("Year-over-year inflation: US vs Portugal")
ax.legend(frameon=False)
ax.margins(x=0.01)
fig.tight_layout()
fig.savefig("slides/assets/inflation_us_pt.png", dpi=150)
print("wrote slides/assets/inflation_us_pt.png")
