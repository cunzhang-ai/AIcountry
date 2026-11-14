# Design240 original sources and reproduction

Captured 9 November 2026 from the official Statistics Denmark
StatBank API. The [original responses, queries and metadata](original-sources/)
preserve the NABB69 and NABP69 release of 30 June 2026 at
08:00 Danish summer time. The dataset timestamp is 06:00 UTC.

- NABB69. Calendar 2025, 69-industry grouping, published total and
  general-government memo. Employee and total work are thousand
  worked hours. Employment measures are source-defined averages.
  [Official table](https://www.statbank.dk/NABB69)
- NABP69. Same release, year and grouping. Compensation, output
  and value added are in million DKK at current prices.
  [Official table](https://www.statbank.dk/NABP69)
- OFF3, OBESK1/2 and NAN1 retain the exact 2025 scopes pinned in
  [Design213](../2026-11-observed-government-baseline/sources.md).
  The statistical release and source families are identified
  separately. Matching one measure does not independently validate
  all dimensions.
- [Custody](../settlement/lawful-custody-capacity/01-danish-appropriations-and-capacity.md),
  [courts](../settlement/court-capacity-and-timely-remedy/01-danish-case-flow-and-source.md)
  and [adaptive care](../settlement/adaptive-home-support/01-denmark-and-copenhagen.md)
  supply qualified predecessor cases within their own scopes.

Run [reconcile-2025.py](../settlement/matched-national-work/reconcile-2025.py)
with Python 3. Its standard output reproduces [results.json](results.json).
The uniform change and alternative gain distributions are declared
calculations, not actual effects. No national conversion from FTE
to a qualified roster, price or free public cash is used.
