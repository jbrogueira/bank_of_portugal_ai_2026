# Inflation expectations — demo corpus

Six papers used in Session 2, §2.1 (literature triage). The set deliberately mixes three older scanned papers with three recent typeset working papers. The scanned/native distinction is the substance of the §2.1 failure-mode demonstration: identical prompt, divergent agent behavior depending on PDF extraction quality.

PDFs are not committed. Download each from the source URL below; rename to the filename listed.

## Bibliography

### Scanned classics

| Filename | Citation | Source |
|---|---|---|
| `cagan_1956_hyperinflation.pdf` | Cagan, P. (1956). "The Monetary Dynamics of Hyperinflation." In M. Friedman (ed.), *Studies in the Quantity Theory of Money*, University of Chicago Press, pp. 25–117. | Scanned copy hosted by R. King (BU): https://people.bu.edu/rking/SZGcourse/Cagan.pdf |
| `muth_1961_rational_expectations.pdf` | Muth, J. F. (1961). "Rational Expectations and the Theory of Price Movements." *Econometrica* 29(3), 315–335. DOI: 10.2307/1909635. | JSTOR: https://www.jstor.org/stable/1909635 — requires institutional access. |
| `friedman_1968_role_of_monetary_policy.pdf` | Friedman, M. (1968). "The Role of Monetary Policy." *American Economic Review* 58(1), 1–17. | AEA top-20 archive: https://www.aeaweb.org/aer/top20/58.1.1-17.pdf |

### Recent typeset

| Filename | Citation | Source |
|---|---|---|
| `coibion_gorodnichenko_2015_info_rigidity.pdf` | Coibion, O. & Gorodnichenko, Y. (2015). "Information Rigidity and the Expectations Formation Process: A Simple Framework and New Facts." *American Economic Review* 105(8), 2644–2678. DOI: 10.1257/aer.20110306. | NBER WP 16537: https://www.nber.org/papers/w16537 |
| `armantier_etal_2017_sce_overview.pdf` | Armantier, O., Topa, G., van der Klaauw, W., & Zafar, B. (2017). "An Overview of the Survey of Consumer Expectations." *FRBNY Economic Policy Review* 23(2), 51–72. | NY Fed Staff Report 800: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr800.pdf |
| `candia_coibion_gorodnichenko_2021_firms.pdf` | Candia, B., Coibion, O., & Gorodnichenko, Y. (2021). "The Inflation Expectations of U.S. Firms: Evidence from a New Survey." NBER Working Paper 28836. DOI: 10.3386/w28836. | NBER: https://www.nber.org/papers/w28836 |

## Use in the session

§2.1 prompts the agent to read the entire folder and produce a comparison table with quoted sentences and page numbers. Expected behavior:

- On the three typeset papers, extraction is clean and quotations are recoverable.
- On the three scanned papers, OCR errors appear in the quoted passages. The agent often fills the gaps confidently, producing fluent but unverifiable text.

The pedagogical purpose is to surface this asymmetry, not to discourage triage. Quoted passages from scanned PDFs require manual verification against the original.

## Reproduction

After downloading, the folder should contain exactly:

```
papers/inflation_expectations/
├── README.md
├── cagan_1956_hyperinflation.pdf
├── muth_1961_rational_expectations.pdf
├── friedman_1968_role_of_monetary_policy.pdf
├── coibion_gorodnichenko_2015_info_rigidity.pdf
├── armantier_etal_2017_sce_overview.pdf
└── candia_coibion_gorodnichenko_2021_firms.pdf
```
