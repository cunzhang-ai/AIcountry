# Original2023 account and model sources inspected on4November2026

All original response/metadata/query bytes are retained in original-sources.
There is one shared Statistics Denmark national-accounts source family, not
nine independent experiments. Fiscal/production/use quantities are accounting
observations; published multipliers are model calculations; the5bn vector and
its programme interpretation are authored. No client testimony or microdata.

| Original primary table | Selected meaning | Published vintage |
|---|---|---|
| [OFF3](https://www.statbank.dk/OFF3) | General-government current/capital transactions, all leaves/parents retained, millionDKK |3June2026 |
| [NASL1](https://www.statbank.dk/NASL1) | S.13/S.1 output, intermediate consumption, value added, pay and depreciation, millionDKK |30June2026 |
| [NAIO1](https://www.statbank.dk/NAIO1) | Total allocated import layer and explicit D2121 duties, no industry parent summation |30June2026 |
| [NAIO2](https://www.statbank.dk/NAIO2) | Total unallocated imports; not a substitute for a duty decomposition |30June2026 |
| [NAIO4](https://www.statbank.dk/NAIO4) | Complete aggregate domestic/import/product-tax supply and seven disjoint final-use classes, current-price millionDKK |30June2026 |
| [NAN1](https://www.statbank.dk/NAN1) | GDP/imports/government consumption, displayed billionDKK at0.1bn precision |30June2026 |
| [INPMUL2N](https://www.statbank.dk/INPMUL2N) | Direct/simple income, imports and GVA per1m final-use change |7July2026 |
| [BESMUL2N](https://www.statbank.dk/BESMUL2N) | Direct/simple full-time employed wage-earner equivalents per1m final-use change |7July2026 |
| [PROMUL2N](https://www.statbank.dk/PROMUL2N) | Direct/simple domestic gross output per1m final-use change |7July2026 |

The three multiplier metadata footnotes explicitly describe a7July addition of
rows missing at30June. Preserve those corrected identities rather than relabel
all sources as a single vintage. The reference year is2023, not a2026 outcome.
Initial NAIO4 household-code selection ACP was rejected before data retrieval;
actual ACPT was verified and captured. No timeout restarted a live source job.

[Multiplier presentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/multiplier-tables/statistical-presentation)
distinguishes direct, simple and induced/normalized variants. We use simple,
including direct/upstream work, without induced consumption. Its unit is a
millionDKK final-use shock; employment counts are not occupational rosters.
The official method warns that induced consumption can wrongly treat people
as having had no prior work/consumption. Rounded three-decimal coefficients
limit precision; rounding propagation alone is about2.5 units on a5,000-unit
weighted total, not a statistical confidence interval or field calibration.

[Multiplier processing](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/multiplier-tables/statistical-processing)
identifies dependence on IO tables and matrix calculations. We reuse original
published coefficients rather than claim a newly estimated Leontief matrix or
independent confirmation from multiple tables. No causal public/private, AI,
job-creation, tax-yield or national-welfare inference follows.

[Supply-use presentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--input-output-and-supply-use/statistical-presentation)
explains basic versus purchaser prices and how customs duties can be included
in imports or separated. Actual NAIO1 D2121=3,612.439m; allocated import layer
1,330,332.762 plus NAIO2 unallocated354,877.916 equals NAIO4's1,685,210.678.
Subtracting the selected duty layer yields1,681,598.239, compatible with NAN1's
rounded1,681,600. GDP from GVA/net-product-tax plus selected duty is2,781,327.528,
compatible with rounded2,781,300. Do not silently force residuals to zero or
use allocated imports alone as the national total.

[Supply-use processing](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--input-output-and-supply-use/statistical-processing)
describes import allocation assumptions and addition of price layers to
purchaser-price column totals. We preserve the original final-use coefficient
boundary, not assume each unit is a cash appropriation or pure imported goods.
The0.266bn increment residual remains unallocated; neither its tax ownership,
refund/receipt nor the increment's import-duty/FX split was derived.

[General IO documentation](https://www.dst.dk/en/Statistik/dokumentation/documentationofstatistics/national-accounts--input-output-and-supply-use)
qualifies compilation/model assumptions and data reliability. These original
method pages were read and retained as HTML, not only search snippets. They
establish no actual country demand, prices, staff, safe receiving, source,
independent affected participation, legitimate adoption or better lives.
Current sector mappings are interpretation: hospital is not the complete HG
network, non-level education is not the complete AL offer, industry is not
institutional ownership, and software capital is not proven useful AI.

No UKGBP, fictionalCU/FU or actual Danish tax law is spliced into these DKK
calculations. No new foreign invoice, supply contract, voluntary buyer,
creditor, household spending response or external consent was obtained.
