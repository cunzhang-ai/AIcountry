# Primary source meaning and the same-year join

Accessed 5 November 2026 · One Statistics Denmark national-accounts family

[Metadata captures](original-sources/metadata-capture-status.json), [data
captures](original-sources/data-capture-status.json), [detailed-use captures](original-sources/programme-capture-status.json)
and [method captures](original-sources/definition-capture-status.json) retain exact
response bodies, queries, status, bytes and hashes. All five table metadata
vintages are 30 June 2026; the reference year is 2023. No changed-vintage numeric
substitution, fabricated failed body or supposed independent confirmation.

| Primary table | Actual scope used |
|---|---|
| [NAIO1](https://www.statbank.dk/NAIO1) | Domestic/import/duty layers,117 six-digit industry leaves plus separate source totals,117 receiving industries, seven final uses and four additional detailed uses |
| [NAIO2](https://www.statbank.dk/NAIO2) | Unallocated imports and component labels by the same uses; use total once, do not add parents/children |
| [NAIO4](https://www.statbank.dk/NAIO4) | Actual industry output and final-use purchaser/import/product-tax layers, including aggregate checks |
| [NABB117](https://www.statbank.dk/NABB117) | All/employee source-defined worked hours, separate total and included G memo; employment counts retained but not turned into available hires |
| [NABP117](https://www.statbank.dk/NABP117) | Companion output/D1 and remaining original transactions; rounded industry output checked, not used to degrade IO precision |

Read [IO presentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--input-output-and-supply-use/statistical-presentation)
and [IO processing](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--input-output-and-supply-use/statistical-processing):
Denmark publishes an industry-by-industry model based on fixed sales structures;
import allocation and price layers have explicit compilation assumptions. Basic
and purchaser values, import duties, inventories and ownership cannot be merged.
We build our own fixed-coefficient allocation, not a newly observed technology.
Detailed product-use relations are not all publicly supplied; this117-industry
view cannot identify a particular nurse, medicine, power shift or delivery site.

Read [NA labor definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--employment-and-compensation-of-employees/statistical-presentation):
source hours include unpaid overtime and shadow adjustments and exclude paid
absence; employment is not a roster; D1 includes actual/imputed employer social
contributions. No legitimization of unlawful/unpaid work, no cash-tax-base
inference. Much ordinary unpaid domestic care/relationships is outside measured
production. Positive output with zero reported hours does not establish no
household burden; its particular source treatment was not investigated further.

## Precision, model and interpretation

Domestic Z/F contain no imported basic supply or net product taxes. L times F
allocates domestic output; hours/output weights allocate source-defined labor.
Direct final imports plus intermediate import coefficients times modeled output
retain allocated and unallocated layers once; selected duty layers are separately
identified and subtracted only for that named import lens. This is no actual
invoice, currency/title/settlement source or foreign worker-footprint estimate.

Fresh IO output has 0.001 m precision; rounded companion output differs by at
most0.5m. Industry source employee/all hours sum respectively0.006m/0.004 m above
published totals. Baseline domestic row imbalance is at most0.008 m DKK; inverse
reconstruction at most0.008687m. Whole import/duty allocations retain their own
small residuals. Ancillary NULL cross-cells, such as output by household final use, remain
NULL; required numeric cells are checked rather than zero-filled.
No source row is rescaled or given a fictitious balancing
worker. The change model uses actual output plus solved change; full baseline
reconstruction and source totals stay separately inspectable.

The added hospital/early-care/non-level-education/software vector is authored,
not a quoted public programme or a new demand observation. Non-level education
extrapolates+160.697%; the aggregate-closing household/export contraction is
26.727768%. Neither is a calibrated marginal response. The household counterpart
includes imputed housing: it is not literally withdrawn cash or collected tax.
Fixed-price demand, actual prices under retained pay, behavior, skills/training,
sector entry, household work, foreign payment, capital and protection need
independent qualification. Negative inventory attribution is net production
accounting displacement, not physically negative labor.

Old177 source/coefficients and185 total-based scalar remain unchanged. Their
original vectors/concepts informed this comparison; no FTE coefficient is
subtracted from national-account hours. A search rediscovered the previously
noted Fan2025 study; its full body was not inspected or adopted here, and it
supplies no extra empirical family or automatic next-study queue. No worker
microdata, sensitive testimony, actual contracts, independent reviewers, paid
capacity or causal country/welfare comparison was obtained.
