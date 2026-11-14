# Original evidence and scope

Design151 · Retrieved3November2026 · English source interpretation, not legal advice

## Direct official statistical responses

The [Statistics Denmark API](https://www.dst.dk/en/Statistik/hjaelp-til-statistikbanken/api)
provides original machine observations. `original-sources/` preserves exact
JSON metadata, submitted query and data for each table, not a secondary chart:

| Table and direct metadata | Query scope | Vintage and unit |
|---|---|---|
| [OFF3](https://api.statbank.dk/v1/tableinfo/OFF3?lang=en&format=JSON) | All UI categories, consolidated TOTAL sector,2023 | 3June2026; millionDKK converted once to billionDKK |
| [OFF29](https://api.statbank.dk/v1/tableinfo/OFF29?lang=en&format=JSON) | All purpose categories,2023 | 3June2026; millionDKK converted once to billionDKK |
| [NAN1](https://api.statbank.dk/v1/tableinfo/NAN1?lang=en&format=JSON) | All transaction categories, V_M current-price choice,2023 | 30June2026; selected money rows already billionDKK, actual hours million, employed persons thousand |

POST endpoint is `https://api.statbank.dk/v1/data`; exact request bodies are
`*-query.json`, responses `*-data.json` and metadata `*-metadata.json`.
The model checks dimensions, year, choices, revisions and units; missing or
status-marked required observations cannot silently become zero. Decimal
arithmetic retains published precision and negative transactions. OFF3's
disjoint leaves and OFF29's top purposes reconcile to the same1,321.267bn
expense; no new candidate budgets are allocated from either view.

Fresh selected2023 cells/statuses are compared with preserved134/139 originals.
Same vintage/data permits narrow source reuse, not transferred final approval
or a claim of independent confirmation. All three tables are one national
statistics evidence family, drawing on shared national/administrative accounts;
they are not three independent experiments. Rounded national demand components
can differ by0.1bn; no residual output or tax is invented to force exactness.

## Official context and event check

[Government finance statistical presentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/government-finance-statistics/statistical-presentation)
identifies S.13 central/local/regional/social-security scope, ESA/SNA and COFOG
purpose classification. Compensation includes cash/kind remuneration and
pension contributions; the source also describes imputed social contributions.
Consequently the396.633bn figure is an expense scale, not cash payroll or
net salaries. Definitions do not confer candidate fiscal or legal authority.

[Ministry working-hours guidance](https://lifeindenmark.borger.dk/working/work-rights/working-conditions/working-hours)
describes agreed37 normal hours in most areas and variable paid/unpaid lunch.
It is no actual public-sector roster or universal statutory37-hour rule. WF's
matched44-week,110-break,64-learning,10%-loss calendar is authored TW-like
comparison on both sides, not measured Danish leave/absence/availability.
The relative gain thresholds are calculations, not measured AI capability.

[26October2026 official EDP notice](https://www.dst.dk/da/Statistik/udgivelser/NytHtml?cid=54370)
reports rounded2025 EDP balance90.2bn and debt847.7bn. Its period, publication
and reporting scope differ from the pinned June2026/2023 model. It remains a
material event check, not a silently spliced replacement observation or proof
of a particular June table error. A future updated baseline needs a matched
bridge. The browser's original-page rendering is saved as
`original-sources/official-context-tool-render.json`; it is not raw HTML bytes,
inspection of every linked law or consent by Danish authorities.

## Claims this evidence cannot establish

No actual jurisdiction/population is selected. Candidate guarantees, tax bases,
behavioral yield, qualified worker supply, old claims, safe operating capacity,
owned FX, actual financing or improved lives are not inferred from aggregates.
No affected-party or independent field/legal review was obtained. Denmark's
wealth, treaties, personnel, assets and institutions cannot be appropriated by
this proposal. Positive productivity, affected shares, revenue/cost shocks and
annual-balance floors are explicit sensitivities, not original observations.
