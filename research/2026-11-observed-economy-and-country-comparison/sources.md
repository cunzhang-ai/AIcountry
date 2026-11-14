# Original published estimates, requests and interpretation

Accessed 3 November 2026. This is an external accounting comparator, not a tax,
investment or relocation recommendation, new law or participant consent.

## Original statistical sources

Statistics Denmark's original StatBank JSON-stat responses, metadata and requests
are frozen in [original-sources](original-sources/). Reference year 2023:

| Original table | Selection / declared unit / table vintage |
|---|---|
| [NAN1](https://www.statbank.dk/NAN1) | Current-price demand/supply; billion DKK; 30 June 2026 |
| [NASL1](https://www.statbank.dk/NASL1) | Production/income by S.1/S.13/S.1W/S.2; million DKK; 30 June 2026 |
| [NASL2](https://www.statbank.dk/NASL2) | Allocation/use/capital/net lending for the same sectors; million DKK; 30 June 2026 |
| [NAN3](https://www.statbank.dk/NAN3) | Households+NPISH consumption/income/saving, current-price billion DKK; 30 June 2026 |
| [OFF3](https://www.statbank.dk/OFF3) | General-government expenditure/revenue; million DKK; 3 June 2026 |
| [NASFK](https://www.statbank.dk/NASFK) | Seven sectors, assets/liabilities, opening/closing/transactions/revaluation/other volumes, all financial instruments/total counterparts; million DKK; 30 September 2026 |

API originals: `https://api.statbank.dk/v1/tableinfo/<TABLE>?lang=en&format=JSON`
and POST `https://api.statbank.dk/v1/data`, exact request bodies retained. The
VNASFK archived-June query returned HTTP500 SYSTEM-100; the original request
was retried once and a CSV-format diagnostic also failed. No CSV data were
received. Current NASFK2023 was then retrieved, keeping its different table
vintage rather than pretending the archive succeeded. The retrieved comparison
matches key net-lending totals; this does not establish every archived cell equal.
Unselected raw rows/categories, structural missing codes and definitions remain
in the sources; the model does not claim to inspect every underlying micro record.

## Primary explanatory scope actually read

[Statistics Denmark, Complete national accounts](https://www.dst.dk/en/Statistik/emner/oekonomi/nationalregnskab/samlet-nationalregnskab)
explains production/use and capital concepts. [Institutional-sector documentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--institutional-sectors)
explains source uncertainty and revisions: published accounts combine administrative,
survey and statistical estimates, not direct observations of every transaction.
[Sector accounts](https://www.dst.dk/en/Statistik/emner/oekonomi/nationalregnskab/sektorfordelt-nationalregnskab)
explains disposable income/net lending and the financial-source collaboration.
[Public economy](https://www.dst.dk/en/Statistik/emner/oekonomi/offentlig-oekonomi/offentlig-sektors-oekonomi)
distinguishes general-government fiscal activity and wider public corporations.
These shared original families do not constitute multiple independent reviews
of AIcountry or calibrate its unprovided workers/source/needs.

[Danmarks Nationalbank, Fixed exchange-rate questions](https://www.nationalbanken.dk/en/frequently-asked-questions/questions-regarding-fixed-exchange-rate-policy)
was read for its krone/euro ERM II framework and division of monetary/fiscal
responsibility. No current actual exchange-rate quote, foreign acceptance,
country monetary equivalence or superiority is inferred. Joint financial-account
compilation also involves this bank; source dependence remains visible.

The prior 133 bounded validator passed before 1,033 predecessor artifacts were
preserved. Its independent u/f examples remain hypothetical, not observations or
new sources for this comparison. Neither repeated AI descriptions nor matched
identities supply affected participation, independent qualification or actual
authority. New source revisions, events and objections require fresh final review.
