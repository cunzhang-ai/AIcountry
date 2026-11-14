# Original population, personal-income and public-employment evidence

3November2026 · Design152 · Reference Denmark2023, not a selected candidate territory

Original English StatBank JSON metadata, exact submitted query and raw data
are retained in `original-sources/`. POST data endpoint is
`https://api.statbank.dk/v1/data`; [official API guide](https://www.dst.dk/en/Statistik/hjaelp-til-statistikbanken/api).

| Table | Frozen selected scope | Retrieved metadata vintage / units |
|---|---|---|
| [FOLK1A metadata](https://api.statbank.dk/v1/tableinfo/FOLK1A?lang=en&format=JSON) | All Denmark, total sex/marital status, all single ages, first day of each2023 quarter |10August2026; persons, not annual recipient-years |
| [INDKP201 metadata](https://api.statbank.dk/v1/tableinfo/INDKP201?lang=en&format=JSON) | All income types/ages, total sex, population5000 including those without the income, nominal006, mean0050 DKK and persons105,2023 |2October2026; separate source-defined mean/counted-person units, not a fiscal-total table |
| [OBESK1 metadata](https://api.statbank.dk/v1/tableinfo/OBESK1?lang=en&format=JSON) | All general-government COFOG purposes, four2023 quarters, unadjusted |24September2026; full-time-equivalent jobs, not unique professionals |

These later source vintages remain separate from WF151's June2026 fiscal/
national accounts. Shared tax/register origins are one evidence family, not
independent causal confirmation. No source is spliced into frozen151 outputs.
Exploratory metadata for OBESK2/OBESK4/PEN113 is retained for transparency:
their data were not used. PEN113 is disability, not an old-age basic table;
OBESK4 is seasonally adjusted, not OBESK1's raw series. Their labels grant
no matched pension-cost or staffing estimate.

[Official income definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/income-statistics/statistical-presentation)
identify annual full-year registered persons15+ and exclusion of in-year
migration/deaths. They distinguish income sources, computed owner rent and
family-equivalised indicators. In the source classification, private pensions
also include civil-service pensions/ATP; public pension includes disability/
old age and early retirement. Candidate source/ownership cannot follow labels.
The documentation's general unit wording does not override this table's
explicit ENHED mean(DKK)/persons choice. Rounded means multiplied by counts
are approximate proxies, not inspected unrounded fiscal totals. No precision
interval or exact net taxable/usable-resource base is inferred.

[Official income accuracy](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/income-statistics/accuracy-and-reliability)
retains omitted/misreported income, theoretical housing values and extraction/
revision limitations. Full register coverage does not mean all candidate
people/needs are covered or that every observation is error-free. New2025
release coverage does not supply a2023 cash/needs/tax-base bridge.

[Official public-employment definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/public-sector-employment--quarterly-/statistical-presentation)
use quarterly average full-time jobs within S.13 by COFOG. Four-quarter mean
is an explicit summary, not annual unique employees, paid overtime available
for new services, occupation/skill mix, actual task hours or complete private/
contracted care. Tool-rendered definitions/accuracy are saved separately from
raw API bytes; an inaccessible population-documentation URL is not claimed
as inspected evidence. No linked legislation or actual worker contract was reviewed.

## Country rules and separate authored calculations

Canonical I04–I20, SD05, PA10–PA12, Y01–Y07, PF and WF151 retain their exact
source semantics. Seven authored person/distribution cases use annual
B120,000/M500,000 and housing60,000 solely as arithmetic scales, not adequate
Danish baskets, median FTE earnings, source-law tax/benefit simulation, service
prices or observed people. Tax, Y, actual pension receipt and I05 match once.
Due basic before correction is separate from paid basic and no automatic
arrears cancellation/recovery is modeled. Ordinary-service credit remains
conditional on applicable law/actual voluntary receipt and costs no free provider.

The gross pension snapshot uses actual January age counts with a unit
1,000DKK monthly B sensitivity; it is not annual entitlement incidence or net
replacement cost. The FTE illustration uses the explicitly authored151
matched-calendar ratio; it is not a recruitment, wage or productivity forecast.
No source establishes a complete candidate budget, real authority, actual
independent affected judgment, safe qualified capacity or improved lives.
