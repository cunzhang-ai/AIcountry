# Decision record: a countable Assembly election

3 October 2026 · integrated-design-15 · Research selection, not election law

## Baseline, authorship and bounded question

The pinned predecessor is [country design 14](COUNTRY-DESIGN-design-14.md)
(SHA-256 `afa669e1a5137eefdbdf0586fc4b48dfa82b5394433357538e9248799514d599`),
[status 14](DESIGN-STATUS-design-14.md)
(SHA-256 `b789269ea3bc6c31510c8c5a143665b76a9ea2ac467a14ea9f1de8b706e321cd`)
and [authority package before this change](AUTHORITY-AND-TRANSITION-before-election-rule.md)
(SHA-256 `69bbd8f019e0e0bc0a769c3186f022847d9951b9ab62096ee2547aec7c024f44`).
The [working framework](../FRAMEWORK.md), [decision template](../DECISION-TEMPLATE.md)
and earlier [candidate-gate review](../2026-10-democracy-and-time/candidate-gate.md)
were consulted. The author and controller are one AI-assisted project. No actual
voter, candidate, minority community, party, administrator, court or independent
reviewer took part. There is no jurisdiction or founding electorate.

The bounded problem is not whether this candidate *sounds* proportional. It is
whether two ballots produce a predictable finite Assembly when a list-backed
candidate wins a district without enough list votes, while a person can still
enter outside party leadership. Design 14 promised both territorial winners and
proportional list shares without deciding overhang, size, ties or shortages. Those
promises can conflict. This record selects a complete **reference count family**
conditional on pre-enacted N, D, a district map and electoral timetable. It does
not supply a first-election law or claim that an untested ballot has public consent.

Equal standing, effective opposition and peaceful replacement are design values
fixed by the user's direction, not empirical findings. The count's mathematical
behavior follows from its definition. Whether voters understand it, whether
districting and nomination are fair, and whether it improves representation are
empirical questions. N, D and the map require contextual and legitimate choice.

## Coherent alternatives

| Package | What it resolves | Cost and live objection |
|---|---|---|
| Retain the unspecified design-14 count | Leaves founding communities maximum flexibility. | The first legislature's composition would depend on later discretion; a promised plurality winner and promised proportionality could each be invoked against the other. |
| Keep every district plurality winner and add overhang plus leveling seats | Territorial first votes directly elect members and list disproportionality can be corrected. | Assembly size can become very large or fail to have a workable bound when a low-list-vote organization wins several districts; staffing, quorum, budget and coalition conditions then move with the result. |
| **Selected: fixed N, list-vote cover, bounded independent personal seats** | Second votes control list-backed seat shares, the Assembly has a known maximum, nonparty individuals retain a territorial route and preferences affect remaining candidates. | Some list-backed district plurality winners are not seated; independents have an asymmetric route and reduce the list seats available. Fixed size is not proof of fair representation. |
| One national or large-region open-list proportional ballot, including small civic lists | One vote, no overhang or conditional territorial winner; candidate choice and full chamber proportionality are easier to explain. | Weakens direct territorial candidate selection, may centralize campaigning and let list gatekeepers dominate without strong entry and candidate preference. Local councils mitigate but do not erase the loss. |
| Candidate-ranked multi-member districts (STV) | Voters rank people rather than accept a list-coverage condition; geographically grounded independent entry. | Transfer counts, district magnitude and local concentration can produce different national proportionality; ballot length and counting capacity need testing. |

International IDEA's [mixed-system analysis](https://www.idea.int/publications/catalogue/mixed-electoral-systems-design-and-practice)
explains the overhang/leveling tradeoff and treats small design choices as
consequential; its [electoral-system database](https://www.idea.int/data-tools/data/electoral-system-design-database)
distinguishes list PR, MMP and STV. The [German Federal Returning Officer's
2025 explanation](https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/informationen-waehler/wahlsystem.html)
documents a real fixed-size, second-vote-backed territorial rule and an
independent-winner exception. These are primary descriptions of comparative
mechanisms, not evidence that Germany's threshold, district structure or ballot
would suit AIcountry. The numerical and candidate-ordering choices below are
AIcountry research hypotheses, not imported authority.

## Selected reference rule, stated as a count

1. Before the nomination period, legitimate law fixes a positive Assembly size
   **N**, a map of **D** single-member territories, and the franchise, with
   **D no greater than floor(N/3)** in this reference. It publishes all ballot,
   tie, recount, challenge, vacancy and certification dates. Equal-voter
   districting, geographic and community exceptions, independent mapmaking,
   public reasons and timely judicial challenge need pre-enacted standards.
   Incumbents cannot apply a materially self-benefiting map to their next contest.
2. Each eligible voter may cast one territorial first vote for a named candidate
   and one national list second vote for a party or objectively registered civic
   list. A second vote may indicate one nominee of the selected list; an absent
   preference does not diminish that list vote. Each district's candidate with
   the most valid first votes is its **plurality candidate**. A predeclared
   independent plurality candidate occupies one personal seat. No person may
   stand for more than one list or territory, and an independent is on no list.
   A list-backed plurality candidate is **not yet elected**. Personal-seat
   eligibility requires no accepted formal list endorsement, list direction
   or materially coordinated list campaign support under published,
   reviewable rules. A unilateral endorsement cannot sabotage an opponent's
   candidacy. A later coalition or similar policy position alone is not proof
   of hidden coordination. Objective pre-poll disclosure, a prompt independent
   appeal and a court remedy for proven concealment are needed; an ideological
   test would turn this safeguard into a veto.
3. Let **I** be the number of independent personal-seat winners. Rank every
   positive-vote eligible list's quotients **V/(2k+1)** for k from zero up to
   one less than its frozen eligible candidate-pool size, where **V** is its
   valid second-vote total. Award the highest **N-I** quotients. Thus a list
   receives no more seats than it has prepublished nominees. There is no legal
   percentage threshold: the finite N-I list seats still create an effective
   threshold. All valid list votes, including those cast in an independent
   winner's district and those without a candidate preference, count in V.
   Blank/invalid list votes do not transfer to another list.
4. Within each list's entitlement, seat its territorial plurality candidates
   first in descending order of each candidate's first votes divided by *all*
   valid first votes in that territory. If the list has fewer seats than such
   plurality candidates, the others are not seated by their first vote. Any
   remaining seats go to not-yet-elected nominees by their recorded second-ballot
   candidate-preference totals; a frozen, public fallback list order resolves
   equal totals, including zero totals. A territorial plurality candidate not
   seated at the first stage remains eligible for a preference-ordered list seat.
5. Quotient ties go first to the list with more total valid second votes;
   exact remaining ties use a public witnessed lot recorded with original
   evidence. Equal territorial first-vote totals require a recount opportunity
   and then the same kind of witnessed lot. Equal territorial vote *shares*
   across districts go first to more raw first votes, then a witnessed lot.
   These are prior rules, not a commission's political choice. A court may
   correct counting, eligibility or procedure under an enacted appeal; it does
   not award a favored person a seat from a missed deadline.
6. The election may not begin with fewer than N certified eligible list nominees
   in total, because an all-list outcome could otherwise leave seats unfillable.
   A list's own small pool caps its possible seats and that cap appears beside
   its ballot information. The nomination timetable must allow death, withdrawal
   or successful exclusion appeals before the freeze. If a post-poll court
   invalidation or catastrophe leaves no lawful nominee for an awarded seat,
   the seat remains vacant pending the enacted corrective election or appeal;
   an officer cannot invent a substitute or silently reallocate past ballots.
   If no valid list votes or lawful count remain, no Assembly result is certified:
   the prior lawful caretaker, court and repeat-poll rules govern, without
   converting failure or delay into an executive mandate.

This is a finite count: I is at most D, so no independent result adds seats
beyond N. The party/civic-list allocation is proportional **among N-I seats**,
subject to indivisible seats and published nominee caps, not exactly
proportional across the full chamber. No statement that every territory has a
seated first-place representative survives this choice. Lists, candidates and
ballot educators must explain that limitation before people vote. Public
ballot-level or equivalent auditable evidence, privacy protection, accessible
paper and assisted routes, independent recount and effective court orders are
part of the count's actual operating conditions.

For an arithmetic check, suppose N=12, D=4 and one independent wins a
territory. The three other territorial plurality candidates are backed by
list A, with first-vote shares 60%, 45% and 40%. List second votes are A=10,
B=50 and C=40, and all pools are large enough. The highest 11 Sainte-Laguë
quotients award **A=1, B=6, C=4**. Only A's 60% territorial plurality candidate
takes its seat by first vote; A's other two plurality candidates remain
unelected unless a subsequent lawful correction changes votes. The independent
holds the twelfth seat. Under an uncapped overhang promise, A would keep all
three despite only 10% of list votes, requiring substantial additional
leveling or accepting disproportionality. This arithmetic is a synthetic
edge case, not evidence about any population.

## Authority, continuity and failure of safeguards

The first N, D, map, candidate rules and exact count must be enacted by a
legitimate founding or predecessor route **before** the Assembly whose seats
they determine is elected. A later Assembly can change future election law
within the protected constitutional franchise, equal standing, opposition and
prospective-effect constraints. The electoral commission publishes the
pre-poll inputs and computes the count; local officers retain original poll
evidence; courts review exclusion, maps, counts and remedies; named officers
execute lawful certification and handover. Parties and civic lists choose
platforms and pools under published nondiscriminatory rules but cannot reorder
nominees after the freeze. No AI tool, archive vendor, publication clerk,
outgoing cabinet or missed deadline selects winners. The same-controller
audit in C03 still applies to mapmaking, nominations, finance, counting,
records, court access and transfer.

A list or list-backed territorial member's vacancy goes to the next eligible
unused nominee in that election's frozen preference/fallback order, after
judicially reviewable eligibility checks. If no nominee remains, the seat stays
vacant until a prior-law corrective election; no party inserts a new name.
An independent personal-seat vacancy triggers a prior-law territorial
by-election open to all qualified candidates. Its winner occupies that
personal seat for the unexpired term, without recalculating old list votes
even if the winner later affiliates with a list. That can temporarily alter
party balance and invite strategic resignation; it needs an observed risk
assessment and could justify a different public choice. Member party
expulsion alone creates no vacancy. A court's correction of the original
count is separate from an ordinary later vacancy.

This rule changes C03 and proposed A10, and it affects founding election law,
districting, campaign funding, ballot design, public media, legal aid, the
evidence archive, independent court capacity, party/civic-list law,
parliamentary quorum and the C06 budget. The cost account must include map
hearings, nomination appeals, paper and accessible ballots, preference
counting, independent auditing, recounts, by-elections and opposition access.
Prior lawful membership, terms, claims and service duties continue until
authorized change. The previous candidate study's assumption that
territorial winners fill seats unconditionally and the older
[democratic candidate's](../2026-09-democratic-control/democratic-constitution.md)
provisional 3% threshold are **displaced for this working design**, not erased
from history.
Their supporters need a fresh opportunity to object; earlier reviews cannot
be transferred to this materially changed proposal.

## Objections, qualification and next decision

The strongest objection is that a voter could see their local plurality
candidate lose despite a clear first-vote win. A one-ballot PR system avoids
that misleading expectation more cleanly; overhang-and-leveling keeps the
direct promise. Here the second vote is treated as the public's control over
the overall balance, while D is bounded and local councils supply local
government. That is an explicit normative choice, not proof that voters
prefer it. Independent personal seats create unequal routes into N. A party or
civic list may conceal support for nominal independents and gain personal
seats alongside its list entitlement. Disclosure and an effective court remedy
reduce but cannot eliminate that risk; an incumbent could weaponize a loose
proxy test against a lawful challenger. Optional preferences can let a small
motivated group reorder a large list or reward money and celebrity. A
no-threshold system may fragment parties, while a threshold can exclude lawful
minorities. Candidate-pool caps could waste list support. Fixed size and a
reproducible formula do not remedy a captured map, inaccessible ballot, hostile
employer, shared records controller or unfunded court. None of these objections
is averaged into a score.

**Evidence:** definitions and comparative primary analyses above plus the
synthetic arithmetic check; no AIcountry field observations. **Research
selection:** fixed N, list-vote cover, capped Sainte-Laguë, no legal percentage
threshold, limited independent personal seats and optional preference.
**Legal authorization:** none. **Operational readiness:** no jurisdiction,
N/D/map, franchise register, ballot, lawful founding rule, staffed commission,
funded court, records system or tested handover. **Observed outcomes:** none.
The selected rule cannot be called a proven democratic improvement.

The next bounded decision is whether the territorial first vote's conditional
effect is understandable and acceptable **compared with** open-list PR and
overhang-and-leveling under the same eligible population, district map,
nomination access and mock votes. A future competent electoral body would
deliver accessible ballot trials, candidate/seat tables for edge cases,
representation and money-power analysis, costed count/recount operations,
recorded objections from voters, parties, civic lists and independent
aspirants, and a proposed first-election statute if legitimately authorized.
The research budget for this desk record is only text and arithmetic; no
field trial is implied. Reopen the choice if conditional first votes are
materially misunderstood, if practical independent/list entry fails, if
uncovered districts or by-elections undermine replacement, if common
controllers can defeat the remedy chain, or if a rival performs better under
the public's stated values. An actual affected electorate must choose; an
AI-authored calculation cannot authorize its own election rule.
