# Original data, scope and reproduction

- The retained [EU-SILC API response](original-sources/hlth_silc_08.json)
  uses `hlth_silc_08`, `time=2024`, `sex=T`, `age=Y_GE16`,
  `lang=en`, and repeated `geo=DK` and `geo=FI`. The original
  response includes all reason and income-group cells available for
  the filter. Extract `TOTAL`, `QU1` and `QU5` for cost, waiting,
  distance and the published combined measure. Preserve flags and
  missing values. [Eurostat EU-SILC health metadata](https://ec.europa.eu/eurostat/cache/metadata/EN/hlth_silc_01_esms.htm).
- The survey percentage is for the relevant population group aged
  16 or over, with usual private-household coverage. A separate
  Eurostat dataset reports percentages conditional on people who
  needed care. Its denominator differs and its values do not enter
  this comparison. [Eurostat 2024 analysis using hlth_silc_08](https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/37395.pdf).
- The [Design428 result](../2026-11-matched-fiscal-baselines-and-budget-choice/results.json)
  supplies the reproduced 2024 general-government COFOG health
  function, `GF07`, in percent of GDP. The earlier source record
  preserves the original response and cross-table residuals.
  [Eurostat COFOG table](https://ec.europa.eu/eurostat/databrowser/product/view/gov_10a_exp).
- Run the [reconciliation](../settlement/health-access-bottlenecks-and-first-budget/reconcile-health-access.py)
  and compare with [results.json](results.json). The constructed
  assessment and treatment choices use separate stated assumptions
  and supply no observed cost or effect.

The sources do not establish actual unmet need outside survey scope,
a causal relationship, an individual care entitlement or a funding
amount for AIcountry.
