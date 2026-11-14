# Sources actually inspected for design155

Retrieved3November2026. Primary statistics/definitions, one source family:
Statistics Denmark. Repeated tables and AI calculations are not independent
observations. Metadata and original JSONSTAT responses are retained in
`original-sources/`; exact request bodies accompany both used data responses.

1. [INDKP102](https://www.statbank.dk/INDKP102), metadata release2October2026:
   All Denmark, both sexes,2023, all13 disjoint pre-tax income intervals plus
   total; ENHED103 persons and110 income in thousands DKK. Count4,938,895;
   total1,953,506,389thousandDKK, interval sum2thousand higher. Data are actual
   published cells; their sums are not reconstructed from rounded means.
2. [INDKP201](https://www.statbank.dk/INDKP201), same release: nominal2023,
   full-year15+ population5000, both sexes, mean0050 and person count105,
   income types105/110/115/120/125/255/260/265. Means visibly in100DKK steps;
   products are rounded proxies, not exact tax collections or a qualified
   sampling/confidence interval.255 means total tax,260 income tax and265
   labor-market contribution. The published three means add exactly here;
   their correspondence to candidate G/S bases and fiscal cash is unproved.
3. [Income statistical presentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/income-statistics/statistical-presentation):
   directly read definitions/coverage. Pre-tax includes primary, transfers,
   private pensions, property and other income; imputed rent belongs in the
   separate disposable-income comparison. Persons must be15+ by year-end and
   registered all year; migrants/deaths in-year are omitted. Statistical private
   pensions include civil-service/ATP; no automatic candidate Y/PF classification.
4. [Accuracy/reliability](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/income-statistics/accuracy-and-reliability):
   directly read; register validation does not eliminate reporting/undeclared-
   income omissions. Certain one-time insurance/gambling receipts are absent;
   later tax corrections may not enter income extracts. No project error bound
   or flawless current-law/behavior match is inferred from register coverage.

The API catalog and INDKP221/222/105/106 metadata were inspected for discovery;
they are retained but do not provide the tax amounts used here. INDKP222 has
counts only and an open upper tail: not a sufficient income-sum substitute.
INDKP106 is disposable income, not the chosen pre-tax base. INDKP102 supplies
amounts and avoids an invented negative-income bound or upper-tail midpoint.

WF151's previously pinned OFF3/OFF29/NAN1 reference and calendar arithmetic
are reused ONLY for a separately declared partial conditional experiment:
net lending97.513bnDKK, compensation396.633bn, matched task hours1308.6/1110.6.
No fresh source qualification, actual roster, country task match or national-
accounts-to-person-tax bridge is claimed. All current obligations through PO
are considered as unpriced/included/new/control/transition dependencies.

Fresh API release dates/responses and current official definition/accuracy
pages were checked. No new conflicting correction was found in that bounded
inspection; no exhaustive news/law/revision search is claimed. Earlier search
snippets about earnings, OECD/Danish taxes and income processing are NOT used
to establish candidate W, actual foreign current law, policy effects or yield.
No affected testimony, original microdata, independent review, supplier offer,
foreign consent, lawful authority or observed country outcome was obtained.
