# Design517 sources and reproduction

- The official [Danish Health Authority publication for Q4 2025](https://www.sst.dk/udgivelser/2026/opgoerelse-over-udredning-og-behandlingsforloeb-paa-kraeftomraadet-maksimale-ventetider-4-kvartal-2025)
  links the [national report](https://www.sst.dk/media/3qupznt3/opgoerelse-over-udrednings-og-behandlingsforloeb-paa-kraeftomraadet-omfattet-af-reglerne-om-de-maksimale-ventetider-4-kvartal-2025.pdf),
  dated 23 February 2026. The national columns in Tables 1, 1a and 1b
  supply the [manually transcribed count extract](original-sources/table-1-extract.csv).
  The table totals reconcile across stages and categories. The figures
  rendered inside Figure 1 show a different arrangement of labels, and
  the prose states 94.56%, 95.53% and 90.53% against table-based
  94.52%, 95.50% and 90.49%. Preserve both vintages of presentation
  within the published document. This analysis uses only table counts.
  Local PDF retrieval returned HTTP 429; the counts were checked against
  the indexed primary report's structured table text.
- The [national monitoring explanation](https://www.sst.dk/vidensbase/sygdomme-og-behandling/kraeftsygdom/overvaagning-af-de-maksimale-ventetider-paa-kraeftomraadet)
  identifies the regulated maximum wait series. The [separate clinical
  pathway timing system](https://www.sst.dk/vidensbase/sygdomme-og-behandling/kraeftsygdom/pakkeforloeb-for-kraeft/standardforloebstider-og-monitorering-af-pakkeforloeb-for-kraeft)
  uses recommended times and differently defined events. Do not merge
  their denominators or import the thresholds into the country proposal.
- Run the [reconciliation](../settlement/clinical-pathway-bottlenecks/reconcile-starts.py)
  to reproduce [results.json](results.json). Counts are episodes among
  covered domestic public hospital starts, with initial and follow-up
  treatment, exclusions and separately reported interruptions. They do
  not track individual realized paths, people who had not started, or
  clinical outcomes.
- The [Health Data Authority workbook landing page](https://sundhedsdatabank.dk/sygdomme/kraeft-menu/kraeftmonitorering)
  supplies the September 2026 [counts workbook](original-sources/denmark-2026-q2-counts.xlsx)
  and [proportions workbook](original-sources/denmark-2026-q2-proportions.xlsx).
  The extractor uses sheets B12 and B26 and columns X and AB for Q2
  2025 and Q2 2026. Rows 11, 20, 42 and 75 are Region Zealand.
  The subsequent rows contain national values. Each row refers to a
  different indicator cohort with its own inclusion and timing rule.
  Retain published precision and do not infer exact numerators.
  [Indicator definitions](https://sundhedsdatastyrelsen.dk/media/16379/Monitoreringsmodel%20Organspecifik%20kraeft.pdf).
