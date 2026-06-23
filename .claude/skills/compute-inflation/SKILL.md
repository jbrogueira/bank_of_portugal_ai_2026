---
name: compute-inflation
description: Compute year-over-year CPI inflation from data/raw/cpi.csv and write long-format results to data/processed/inflation.csv, via the committed script.
---

# compute-inflation

Compute year-over-year (YoY) inflation from the raw FRED CPI export and write
the result to `data/processed/inflation.csv` in long format.

## Rule

Per the project's data-handling rule, the transformation lives **only** in
`code/scripts/compute_inflation.py`. Do not transform the data inline or with
shell one-liners. This skill runs that committed script.

## Steps

1. Confirm `data/raw/cpi.csv` exists and is the monthly FRED `CPIAUCSL` series
   (header comment lines `#` describe units and frequency). `data/raw/` is
   read-only.
2. Run the script from the project root:

   ```bash
   python code/scripts/compute_inflation.py
   ```

3. The script:
   - reads `data/raw/cpi.csv` (skipping `#` comment lines),
   - sorts by date and reindexes on a monthly `PeriodIndex` so the 12-month
     lag is by calendar date and any missing month becomes an explicit NaN,
   - computes `100 * (p / p.shift(12) - 1)`,
   - drops NaN rows and writes **long format** to
     `data/processed/inflation.csv` with columns `date,series,value`
     (`series` = `cpi_yoy`),
   - prints the most recent 12 months as a sanity check.

4. Verify the printed tail looks plausible (single-digit percent for recent
   years) and that `data/processed/inflation.csv` was updated.

## Output schema

| column | meaning                          |
|--------|----------------------------------|
| date   | first day of the month (date)    |
| series | series id, `cpi_yoy`             |
| value  | YoY inflation, percent           |

## If something looks wrong

The script raises on data problems (gaps, frequency) rather than silently
fixing them. If it fails, inspect the raw file's cadence — do not patch the
data outside the script. If the fix won't fit the script, stop and ask.
