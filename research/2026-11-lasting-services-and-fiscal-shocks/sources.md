# Source archive and reproduction

## Original observations

The English-language Statistics Denmark Statbank API responses and their
exact request bodies are stored under [original-sources](original-sources).
The API endpoints are `https://api.statbank.dk/v1/tableinfo` for definitions
and `https://api.statbank.dk/v1/data` for observations. Each series uses
2015–2025 and the original release units.

| Table and publisher update | Scope and units | Local material |
|---|---|---|
| OFF3, 3 June 2026 | General government TOTAL. 1.1 employee compensation, 1.17 current and capital expense, 2.17 current and capital revenue, 2.19 released net lending/borrowing. Million DKK. | [Definitions](original-sources/OFF3-metadata.json) · [Data](original-sources/OFF3-data.json) |
| SKAT, 3 June 2026 | Central 1.1.01 and municipal 1.1.03 income tax. Separate 1.3 tax on yields of certain pension scheme assets. Thousand DKK. | [Definitions](original-sources/SKAT-metadata.json) · [Data](original-sources/SKAT-data.json) |
| NAN1, 30 June 2026 | B1GQK GDP, V_M current prices. The generic unit field is a dash and the price axis states billion DKK. GDP is used only to scale the observed balance. | [Definitions](original-sources/NAN1-metadata.json) · [Data](original-sources/NAN1-data.json) |

The publisher's interactive tables identify the series. The archived
machine-readable responses and definitions provide the observed values
used here. The responses were captured for this edition. The archive
makes no assumption that later revisions retain these values.
[OFF3](https://www.statbank.dk/OFF3) · [SKAT](https://www.statbank.dk/SKAT) · [NAN1](https://www.statbank.dk/NAN1)

## Scoped calculation

Run `python3 research/2026-11-lasting-services-and-fiscal-shocks/compare.py`
from the project directory. It reads the archived original responses and
writes [results.json](results.json). The script has no third-party dependency.
OFF3 values divide by 1,000, SKAT values by 1,000,000, and NAN1 values use
their V_M unit. The published balance stays authoritative for this comparison
and the script records its difference from published revenue minus expense.
Unrounded values drive the arithmetic and displayed money amounts round to
three decimal places.

Reuse of the earlier WF case is limited to the matched-calendar factor and
its unchanged-pay/output, full-compensation and no-gain assumptions. The
2015–2025 comparison reapplies the factor to released same-year compensation.
The new 10% benchmark scales a hypothetical net receipt against observed
central plus municipal income tax. It does not apply a percentage rate to
taxable income, add observed taxes twice or join SKAT cash to OFF3 accruals.
The evidence is from one publisher family and is not independent replication.
These are historical contexts for a design comparison, with no projection of
cost, behavioral response or readiness. [Calculation](compare.py)
