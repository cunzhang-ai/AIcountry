# Design516 original sources and reproduction

- [Eurostat hlth_silc_08](https://ec.europa.eu/eurostat/databrowser/view/hlth_silc_08/default/table)
  reports selected unmet need reasons as a proportion of the population group.
  The [retained API response](original-sources/hlth_silc_08.json) uses
  `lang=en`, `age=Y_GE16`, `sex=T`, and repeated `geo=DK`, `geo=FI`,
  `time=2024` and `time=2025`. The publisher version reports 20 October 2026.
- [Eurostat hlth_silc_08b](https://ec.europa.eu/eurostat/databrowser/view/HLTH_SILC_08B/default/table)
  gives a ratio conditional on reported need. The
  [retained API response](original-sources/hlth_silc_08b.json)
  uses the same query filters with that other dataset. It classifies the
  population relative to a national poverty threshold. That group is not
  the lowest income fifth. Neither series gives a jointly observed person
  link, actual appointment or administrative treatment confirmation.
- The [publisher metadata](https://ec.europa.eu/eurostat/cache/metadata/en/hlth_silc_01_esms.htm)
  describes EU-SILC health scope, main reason, the survey frame and group
  definitions. Use point estimates as reported and preserve flags. No test
  of statistical significance is supplied here.
- Run [the extractor](../settlement/comparative-country-validation/reproduce-survey.py)
  to reproduce [the comparison cells](results.json). No user records or
  synthesized 2025 health spending are used.
