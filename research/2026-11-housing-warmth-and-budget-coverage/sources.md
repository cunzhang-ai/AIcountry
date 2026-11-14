# Official observations for income, housing and warmth

The three [Eurostat EU-SILC data products](https://ec.europa.eu/eurostat/web/income-and-living-conditions/information-data)
use the published 2024 survey labels, annual frequency, percentage
unit, Denmark and EU-27. The selected totals use all ages and sexes
where those dimensions apply, and all private-household compositions
for warmth. The edition preserves the responses as returned in the
October 2026 source vintages. No cell used carries a published status
flag in those responses.

| Dataset and query | Local snapshot | Source vintage |
|---|---|---|
| [ilc_li02 at-risk-of-poverty rate](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_li02?lang=en&geo=DK&geo=EU27_2020&time=2024&freq=A&unit=PC&age=TOTAL&sex=T&statinfo=MED_EI&rskpovth=B_60) | [Response](ilc_li02.json) | 20 October 2026 |
| [ilc_lvho07a housing-cost overburden by poverty status](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho07a?lang=en&geo=DK&geo=EU27_2020&time=2024&freq=A&unit=PC&age=TOTAL&sex=T) | [Response](ilc_lvho07a.json) | 29 October 2026 |
| [sdg_07_60 inability to afford adequate warmth by poverty status](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_07_60?lang=en&geo=DK&geo=EU27_2020&time=2024&freq=A&unit=PC&hhcomp=TOTAL), derived from ilc_mdes01 | [Response](sdg_07_60.json) | 20 October 2026 |

The poverty selection is below 60% of median equivalised disposable
income. [Eurostat's housing indicator](https://ec.europa.eu/eurostat/databrowser/view/tessi163/default/table?lang=en)
uses a relative housing cost measure, with costs and income net of
housing allowances. [Its warmth indicator](https://ec.europa.eu/eurostat/databrowser/product/view/sdg_07_60)
is self-reported. [Survey methodology](https://ec.europa.eu/eurostat/web/income-and-living-conditions/methodology)
describes private households, income construction and imputation.
The statistical population excludes people outside private households,
and the aggregate results identify no individuals, buildings or cases.

The verifier parses the official dimension indexes, reconciles totals
against poverty strata within rounding and reproduces the saved
[results](results.json). It does not recreate survey weights, sampling
errors or a causal intervention. No assumptions about the source
population are copied into actual AIcountry benefit law.
