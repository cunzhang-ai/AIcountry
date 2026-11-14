# Source boundaries and reproduction for Design213

Retrieved 9 November 2026. The original publisher responses, metadata
and exact API queries are in [original-sources](original-sources/).
Statistics Denmark is one source family. The court administration and
prison service replies in the Justice minister's letter are not
independent verification of completed correction.

| Reference | Release and scope |
|---|---|
| [OFF3](https://www.statbank.dk/OFF3) | 3 June 2026. Annual current-price expenditure, revenue, compensation, balances and current and capital internal transfers, million DKK, all sectors for 2025 |
| [OFF29](https://www.statbank.dk/OFF29) | 3 June 2026. Ten annual expenditure purposes and total, million DKK, 2025 |
| [OBESK1](https://www.statbank.dk/OBESK1) and [OBESK2](https://www.statbank.dk/OBESK2) | 24 September 2026. The four 2025 quarters by purpose and by sector, full-time equivalent employee jobs. Purpose attribution uses administrative and wage data, partly drawing on national accounts |
| [NAN1](https://www.statbank.dk/NAN1) | 30 June 2026. Selected 2025 whole-economy output, imports and final uses, current-price billion DKK |

The [employment definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/public-sector-employment--quarterly-/statistical-presentation)
describe the counting unit and quarterly means. The [processing notes](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/public-sector-employment--quarterly-/statistical-processing)
describe the estimated purpose allocation and the use of wage information
from national accounts. No joined purpose-by-subsector or occupation
roster was obtained. The 2025 year matches across the selected datasets.
The releases and definitions differ.

The [original Finance Act](https://fm.dk/media/o54afmlz/finansloven-for-2025-fuld-version.pdf)
was inspected at the publisher. Its main budget overview supplies
the original state-budget expense, revenue and balance. The captured
[central state accounts summary](original-sources/danish-state-accounts-summary-2025.pdf)
gives the later appropriations, outturn and annual net cash bridge
in tables 1 and 6. No complete transaction bridge to ESA accounts
or daily liquidity data is assumed.

The [financial audit summary](https://www.uk.rigsrevisionen.dk/audits-reports-archive/2026/aug/report-on-the-audit-of-the-danish-public-accounts-for-2025)
covers report 19/2025. The [operational audit](https://www.rigsrevisionen.dk/Media/639225602093624025/sr2025.pdf)
covers report 20/2025, especially sections 4.1 and 5.2. The [minister's reply](https://cdn.rigsrevisionen.dk/rigsrevisionen/Media/639286205594339469/20-2025-jm.pdf)
is dated 20 October 2026. These three documents are archived. The [state accounts status](https://oes.dk/statsregnskab/statens-regnskaber/statsregnskabet/statsregnskabet-2025/)
was inspected at the publisher. The findings qualify the tested
historical scope. Actual current delivery after the reported changes
requires newer evidence.

Run [compare.py](compare.py) with Python 3.10 or later. Its standard
output reproduces [results.json](results.json) from the preserved
responses. It compares transfer leaves in both directions and uses
source parents for consolidation. The accompanying comparison
retains the small fiscal, employment and final-use residuals without
creating an extra worker, invoice or funding line. No new model,
salary estimate or cross-vintage industry extrapolation is used.
