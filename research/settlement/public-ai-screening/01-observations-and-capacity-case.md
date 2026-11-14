# What changes when screening allocates scarce review

## Two observed limits

The UK Department for Work and Pensions reported that its model selected more
high-risk Universal Credit advance requests than a random comparison, by a factor
of 2.5, in its 2025–26 experimental analysis. The reviewing officer made the
decision and did not receive the model's risk rating. Among the specified
groups of paid advances, median time to payment was zero days when no fraud
control referred the request and one day after a high-risk model referral
followed by human approval. Advances subject to other fraud controls had the
same one-day median. These groups describe different routes. The difference
alone cannot isolate the model's causal effect or show whether late tails,
displacement, abandonment and missed useful times were acceptable. The agency's
conclusion about minimal effects is its assessment. A check against random
sampling also leaves open how the model compares with good ordinary triage.
[DWP assessment, paragraphs 10–11 and 31–32](https://www.gov.uk/government/publications/effectiveness-assessment-including-statistical-analysis-of-the-universal-credit-advances-machine-learning-model-1-april-2025-to-31-march-2026/effectiveness-assessment-of-universal-credit-advances-model)

Canadian Treasury Board guidance explicitly includes intermediate automation
and some machine-defined triage in the scope of its federal directive even
where an officer decides. It distinguishes some clerical work and simple
legislated triage. This is an institutional precedent for treating the route
as consequential. It supplies no observation about staffed alternatives or
remedy delivery for the proposed country.
[Treasury Board scope guide, decision processes and examples](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/automated-decision-making/guide-scope-directive-automated-decision-making.html)

## Constructed exercise with fixed capacity

Assume a benefit office has eight independent, qualified 15-minute work slots
before noon. Six admitted requests require a decision before noon. Two other
requests have original independently documented grounds for urgent review
before noon. None of these eight overlaps. The ordinary route uses all eight
slots. A new model also flags five distinct requests with uncorroborated
address mismatches. Their ordinary deadline is later. Assume each needs one
slot if checked. These are units of staff time. No one can be counted as working
in two of them at once.

| Routing choice | Before noon | Consequence |
|---|---|---|
| Ordinary priority | Eight due slots | Eight timely, no added review before noon |
| Put five flags at the head | Five flagged slots and three due slots | Five of eight due tasks miss noon, even if all final decisions are signed by humans |
| Protect the ordinary schedule | Eight due slots | Eight timely. Five leads can use paid qualified later capacity within the original deadlines or stay outside discretionary review |

Assume that at 10:00 an operator finds a credible error in the shared address
normalizer that also supplies a local housing office's queue. Its separate
staff have four slots before noon, three for due urgent cases and one genuine
spare. Three unsupported additional flags would require three slots if checked.
Head-of-queue handling would leave only one urgent slot and cause two misses.
The housing duty holder can restore its local priority and use its spare for
independent case evidence or ordinary work. Its slot does not count toward the
benefit queue. Each office can pause the affected referral and verify using
its lawful independent records. The coordinator warns both offices with
dependency and protective information. It cannot choose the payer or direct
either case. An unrelated, independently functioning appointment reminder
continues. If another request turns out to require urgent independent review
in the benefit office, or one of the five leads is corroborated and legally due
by noon, nine tasks compete for eight slots. The existing lawful priority and
scarcity process decides actual order, records the outstanding duty and sends
it to a competent receiving route if available. The model supplies no ninth slot.

Correction checks which person missed actual assistance, what can still be
delivered and which lawful remedy remains due. It cannot be marked complete
just because the address field was fixed or the original priority was restored.
No model precision, labour costs, operational capacity or national gain can be
inferred from these authored assumptions.
