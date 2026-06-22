# Bank of Portugal — AI Tools for Economics Research (2026)

12-hour course at Banco de Portugal. Four sessions × 3 hours in two 90-min blocks (10:30–12:00 and 14:30–16:00): Mon 25 May, Fri 29 May, Mon 22 June, Tue 23 June (2026). Audience: research economists.

## Structure

```
bank_of_portugal_ai_2026/
├── slides/
│   ├── decks/        # Marp source (.md), theme.css, rendered .pdf
│   └── assets/       # Figures and diagrams (.svg)
├── code/
│   └── scripts/      # Python scripts written during demos
├── data/
│   ├── raw/          # Original datasets (e.g. cpi.csv from FRED) — read-only
│   └── processed/    # Outputs from analysis scripts
└── docs/             # Syllabus (.md/.pdf) and TeX header
```

## Data handling — the one rule that does not bend

**Every step that touches data goes through a committed Python script under `code/scripts/`.** No inline snippets, no shell one-liners that transform data, no ad-hoc edits. If it isn't in a script that runs from a fresh clone, it didn't happen — that script is the only audit trail.

- `data/raw/` is **read-only**. Open it, never write it. Derived files go to `data/processed/`.
- A script may *read* `data/raw/` and *write* `data/processed/`. It must do its own checks (frequency, gaps, duplicate dates) and raise on a problem rather than silently fixing the data.
- Inspecting a raw file's header or comment lines to confirm a column is fine. Transforming data outside a script is not.
- If a data step won't fit in a script, stop and ask.

## Build

- **Syllabus**: `cd docs && pandoc syllabus.md -o syllabus.pdf --pdf-engine=pdflatex -V geometry:margin=1in -V fontsize=11pt -V documentclass=article --include-in-header=syllabus-header.tex`. Typography in `docs/syllabus-header.tex` (Palatino body, Helvetica accent headings, `#1F3A68` accent).
- **Slide deck**: `cd slides/decks && npx --yes @marp-team/marp-cli@latest --theme-set theme.css --html --allow-local-files sessionN.md -o sessionN.pdf`. `--html` is required because slides use inline HTML for layout classes (`title`, `divider`, `center`, `split`, `takeaways`).

## Slide conventions

- Decks use Marp + a shared CSS theme (editorial cream/ink with `#cc785c` accent). Do not switch to LaTeX/Beamer without asking.
- Each session is one `.md` file with a midpoint break: end-of-morning takeaways → break slide → an `AFTERNOON` suffix on the section divider that opens after lunch. Morning/afternoon split: §1.2 ↔ §1.3, §2.2 ↔ §2.3, §3.2 ↔ §3.3, §4.2 ↔ §4.3.
- Slide outline notes live in `slides/decks/outline.md`.

## Agent configuration

The repo doubles as the worked example for Session 4 — shared agent config lives in version control so a fresh clone inherits the setup:

- **`CLAUDE.md`** (this file) — standing conventions that hold every turn.
- **`.claude/skills/`** — named multi-step procedures invoked with `/name` (e.g. `clean-series`).
- **`.claude/settings.json`** — permissions and hooks (e.g. the audit-trail log).

## Other conventions

- Keep demo datasets small enough to commit (`data/raw/`).
- Code should be runnable end-to-end from a fresh clone.
