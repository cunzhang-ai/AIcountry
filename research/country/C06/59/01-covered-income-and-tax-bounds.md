# TN01–TN04: test a tax source without inventing a population

*Part of [TN](../59-tax-sources-and-country-operation.md); statistical proxy only.*

**TN01 — Match scope before deriving a source.** Fresh official INDKP1022023
reports4,938,895 full-year registered persons15+ and1,953.506389bnDKK pre-tax
income. The13 disjoint intervals reconcile exactly in count and differ by
2,000DKK in their published income sums from the total. Preserve that small
publication discrepancy; do not redistribute it or claim exact underlying
microdata. INDKP201's rounded mean×same count gives1,953.3329725bn, a distinct
rounded proxy. Neither source covers children under15, in-year migrants or
people who died during the year. These people keep candidate protection.

**TN02 — Bound the declared proxy, including the tails.** Apply the specified
SD05 tax directly to statistical pre-tax income X, before any Y deduction,
with authored M400,000/500,000/600,000DKK. These are sensitivities, not measured
W, selected legal M or a qualified range. For each finite interval with count n,
sum S and conservative endpoints a/b, convexity gives lower `n*f(S/n)` and
upper `n*f(a)+(S−n*a)*(f(b)−f(a))/(b−a)`. Below100,000, even negative incomes
produce zero tax for these scales. Above10million, f is affine: use S/n's
actual aggregate contribution, never a midpoint or income cap. Bounds treat
published cells as inputs, not confidence bounds on underlying observations.

| Authored M (DKK) | Proxy ordinary tax lower–upper (bnDKK) |
|---|---|
|400,000|391.320–400.096|
|500,000|325.616–331.343|
|600,000|273.780–284.154|

**TN03 — Preserve the definition gap.** Statistical pre-tax X is NOT TA Q.
TA05 ring-fences business losses rather than offsetting wages; TA06 inflation-
adjusted realized gains, PF private contribution/basis rules, noncash gross-up,
foreign relief and source periods differ. Exempt basic/I05/true reimbursements
and lawful Y reduce some candidate bases; removed relief or ring-fencing may
increase others. Published net sums do not identify positive worked receipts,
actual individual Y or joint gain/loss distributions. Therefore the table is
neither a proven upper bound nor a forecast of actual candidate receipts. Do
not apply rates to an average person or call all statistical pension cash Y/PF.

**TN04 — Expose the conflict without inventing a national deficit.** INDKP201's
108,600DKK income-tax mean×count is536.363997bnDKK; the separate21,200DKK
labor-market contribution mean×count is104.704574bn. These are rounded covered-
person products, not OFF3 cash collections. In a declared experiment replacing
only the first proxy and holding every other reference source fixed, ordinary
tax falls136.268–262.584bn across the three scales. Combining that experiment
with WF's70.713bn paid-time increment leaves partial annual balances below
zero even before other new costs. This defeats a source-neutral assumption
WITHIN THE EXPERIMENT; it proves no actual shortfall, balanced-budget law,
minimum tax increase or unaffordability of the whole country. A full actual
candidate balance remains unknown, including all unmatched cost/source bridges.
