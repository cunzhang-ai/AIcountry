# Original Eurostat sources and reproduction

The retained responses are for Denmark and Finland in 2024,
annual frequency, general government S13 and percent of national GDP.
The API snapshots retain their original metadata, values and missing
cells. The HTML extract preserves the original header and relevant
country rows from the published table.

| Source | Retained original | Used here |
| --- | --- | --- |
| [General government expenditure by function](https://ec.europa.eu/eurostat/databrowser/product/view/gov_10a_exp) | [gov_10a_exp](original-sources/gov_10a_exp.json) | TE, TOTAL and ten top-level COFOG headings. The response also contains lower-level headings. |
| [Government revenue, expenditure and main aggregates](https://ec.europa.eu/eurostat/databrowser/product/view/gov_10a_main) | [gov_10a_main](original-sources/gov_10a_main.json) | TE, TR and B9 cross-check. Preserve missing Danish TR and B9 cells in the snapshot. |
| [Government deficit, debt and associated data](https://ec.europa.eu/eurostat/databrowser/product/view/gov_10dd_edpt1) | [gov_10dd_edpt1](original-sources/gov_10dd_edpt1.json) | B9 and GD. |
| [October 2026 fiscal notification](https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-21102026-ap) | [Published table rows, compressed](original-sources/eurostat-edp-october-2026.html.gz) | Published 2024 expenditure and revenue rows. |

The three API responses use the Eurostat dissemination statistics
endpoint. The common filters are `lang=en`, `time=2024`, `sector=S13`,
`unit=PC_GDP`, and repeated `geo=DK` and `geo=FI`. For
`gov_10a_exp`, `na_item=TE`. For `gov_10a_main`, repeated
`na_item=TE`, `na_item=TR` and `na_item=B9`. The deficit and debt
response retains all its indicators under the common filters.

Run [the standard-library reconciliation](../settlement/matched-fiscal-baselines-and-budget-choice/reconcile-fiscal-baselines.py)
and compare its output to [results.json](results.json). The script
uses decimal arithmetic and locates the published 2024 column
from the year header. The source records report an October 2026
update. Use the frozen responses for this edition. A later dataset
revision needs a new comparison. All figures describe the reported
scope and supply no authorization, cash forecast or outcome measure.
