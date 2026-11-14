# Original observations, authored inputs and remaining limits

Retrieved3November2026 · Edition159 · Reference2023, not a selected jurisdiction

| Original source | What was actually inspected and used |
|---|---|
| [Statistics Denmark OFF10](https://www.statbank.dk/OFF10), metadata updated3June2026 | Captured English metadata/query/JSONSTAT for2023 total, civil-service, pension and old-age/early-retirement/supplement/other leaves. Only1.2.1 old-age150355mDKK enters hypothetical credit. Other captured categories are diagnostic exclusions, not extra offsets. |
| [Statistics Denmark FOLK1A](https://www.statbank.dk/FOLK1A), metadata updated10August2026 | Captured metadata/query/JSONSTAT, allDenmark000/allsex/allmarital, disjoint65–125 ages at2023K1–K4. Sum stock per quarter1213329/1217924/1223895/1228388; average1220884. No recipient history, survivor exposure, microdata or future forecast. |
| [Population definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/the-population/statistical-presentation) | Direct relevant definition, registration coverage, area and reference-date inspection: these are registered resident stocks; asylum/unregistered exclusions mean statistical scope cannot become a rights test. Denmark excludes Greenland/Faroes. No exclusion count used. |
| [Government finance definitions](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/government-finance-statistics/statistical-presentation) | Direct relevant sector/transaction definitions inspected: S.13 includes central/local/regions/social funds; compensation is wider than cash pay and includes pension/social components; pension transfer categories differ. An expense balance does not supply accepted borrowing or cash. |
| [151 original OFF3/NAN1 captures](../2026-11-country-source-and-capacity-frontier/original-sources/) | Reuse exact published2023 NL97.513, compensation396.633, revenue1418.780, expense1321.267bnDKK and GDP2781.3bnDKK within their original June3/June30 vintages. Actual entitlement/candidate source equivalence remains unqualified; no silent newest-vintage substitution. |

All fresh table requests use the official API endpoints
`https://api.statbank.dk/v1/tableinfo` and `https://api.statbank.dk/v1/data`;
exact submitted bodies and received JSON remain in `original-sources/`.
Selected definition inspection is recorded separately, not presented as archived
full webpage bytes. A guessed finance-document URL failed and contributes no
support; the corrected official government-finance entry above was inspected.
These observations share one statistical institution and often underlying
registers; they are not independent studies or independent reviewer judgments.
No new conflicting correction was found within this bounded inspection, which
is not a complete event/country-law search. No people were contacted.

## Explicit analytical choices

`inputs.json` defines17 named experiments, not a representative random sample or
probability distribution. Fixed reference economy/population; W400k/500k,
B96k/120k/200k, authored average earned pension0.25/0.375/0.5W; programme credit
0/0.5/1; net source0/3/5% referenceGDP; additional cost0/1%; partial floor0/−3%;
hours37/36/32 and a separate20% task-gain case. The same44 paid weeks,110 break
hours,64 learning hours and10% loss are authored inherited task assumptions,
not measured Danish staffing or a change to TW's actual legal proposal.

`H=C*p*(max(1,A37/(Ah*(1+g)))−1)`, `Ah=(44h−110−64)*0.9`.
All cases use p1; gain never creates a negative compensation bill or a source.
`Pnew=mean65stock*(B+aW)` is a scale illustration, not a reconstructed Y cohort.
`NLpartial=NLreference+ΔR−H−Pnew+k*Pold−O`; monetary outputs bnDKK.
Programme credit is hypothetical even at k1; new-service illustration never
cancels old rights, public/private capital, earlier earned units or survivors.
An actual transition may carry both systems. k0–1 is an authored sensitivity,
not a statistically established matching interval or bound on total costs.

All-net ΔR would need changed pension/pay taxes, existing/new contribution
receipts, tax interactions and behavior. We have not qualified it. TN155/156
fixed-income experiments cannot transfer to changed pension incomes. No extra
10% contribution, internal G-to-S credit, gross tax clawback, retained baseline
receipt or private balance enters as free new national revenue. ReferenceGDP
only scales authored inputs; it is not post-reform output. O0 does not mean no
other actual costs. Other-service/control/material/legacy/unfamiliar classes,
full cost, cash, FX, simultaneous qualified receiving and outcomes stay null.

## Bounded conclusion and reproducibility

Central authored source-neutral pension/time experiment fails its chosen partial
floor, including37hours; partial passes depend on assumed sources and omit
actual unqualified costs. No actual deficit, tax rate, minimum source, changed
benefit/hour date, accepted debt, whole-country feasibility or superiority
follows. Read [the decision](decision-record.md) and [current joined findings](../settlement/country-frontier/05-joined-public-offer-and-source.md).
`python3 model.py` reproduces `results.json`; `validate.py` checks arithmetic,
source/provenance, dependencies and unknown handling, not field outcomes.
