# One product test, two installation decisions

This constructed case tests [DMR01–DMR08](../../country/C04/01/03-domestic-recognition-and-local-protection.md).
Two public water sites need working pumps by the end of day 4. The common rule
covers a defined product configuration. Each site has its own authorized
inspector and installation slot. Assume no queue, no shared staff between sites,
and sequential work at each site. The original qualified product evidence takes
one day to authenticate. Repeating a full test takes three days including
authentication. The local inspection and installation each take one day.

| Path | Site A | Site B |
|---|---|---|
| Repeat the full test at both sites | Working on day 5 | Working on day 5 |
| Recognize the product claim and check both sites | Working on day 3 | Working on day 3 |
| Site B has a use outside the tested scope | Working on day 3 | Original installation blocked pending new evidence and site approval |
| Site B fails its installation inspection | Working on day 3 | Original installation blocked pending a safe site decision |
| Confirmed defect in Site B's batch only | Working on day 3 | Original installation blocked under a scoped hold |

In each blocked branch, Site B's existing approved supply remains in use
through day 3. An independently qualified and inspected backup can reach Site B
on day 4 if the named public payer settles 4 units by day 3 and the operator
confirms receipt on day 4. A branch with 3 units by day 3 and 1 on day 4 misses
the dispatch cutoff. A fully paid dispatch without usable receipt also misses
the deadline. Both failures leave a service gap visible to the duty holder and
reviewer. Neither converts the original evidence into approval for the blocked use.

The comparison assumes an authenticated unaffected batch at Site A. If that
separation cannot be established, the scoped decision must account for that
uncertainty. The two-day difference is a consequence of the assumed schedule.
Actual workload, costs, safety effects and independent remedies need separate
observation.

[Reproduction](verify-domestic-recognition.py).
