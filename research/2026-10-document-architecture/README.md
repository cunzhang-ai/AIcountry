# Design 27 document architecture

4 October 2026 · Structural change only; no design 28 selection

The country design already had fourteen C01–C14 chapter identities, but several
current supporting documents and three chapters still mixed many distinct jobs in
files of 281–572 lines. This made it hard to locate an authoritative paragraph,
review a focused change or tell current design from revision history.

The stable `research/` and `research/country/` paths now serve as short navigation
entries. The complete current text was relocated into:

| Stable entry | Current detail | Role |
|---|---|---|
| [Authority and transition](../AUTHORITY-AND-TRANSITION.md) | [authority/](../authority/) | Public powers, legacy migration, candidate clauses and continuity |
| [Founding and stress](../FOUNDING-AND-STRESS.md) | [founding/](../founding/) | Legitimate commencement, F1–F10 exercises and readiness limits |
| [C06](../country/C06-public-finance.md) | [country/C06/](../country/C06/) | Tax/budget, money/credit, shared commitments and shortfall |
| [C08](../country/C08-everyday-law-and-justice.md) | [country/C08/](../country/C08/) | Civil law, courts, criminal justice and official abuse |
| [C14](../country/C14-establishment-and-improvement.md) | [country/C14/](../country/C14/) | Founding/change, transition and learning |
| [Design history](../DESIGN-HISTORY.md) | [history/](../history/) | Research selections by period and remaining gates |

The [predecessor-design-27 snapshot](predecessor-design-27/README.md) retains all
six complete source files and their checksums. A reconstruction check confirmed
that the topic files contain the same substantive body text after reversing only
relative-link rebasing and added navigation headings. The introductions remain
at their established paths. Local links from the current research documents were
checked after relocation. This change does not adopt a new method, legal provision
or institutional arrangement. The current proposal remains integrated design 27.

Future changes should edit the relevant topic file and its chapter entry only when
navigation needs updating; a consequential selection also updates the integrated
country overview and status register. Do not rewrite the predecessor snapshot.
