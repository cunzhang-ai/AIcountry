# AIcountry research map

AIcountry's current proposal is an English-language research design, not an
operating or legally adopted state. The files below have distinct jobs.

## Current file layout

```text
research/
  COUNTRY-DESIGN.md       whole-country summary (entry point)
  DESIGN-STATUS.md        chosen options, conflicts and priorities
  country/
    C01-...md to C14-...md  chapter entrances
    C01/ to C14/            canonical, short topic files
    systems/                four cross-chapter reading maps
    integration/            authority, shared duties and remedies
  coverage/                 four functional-audit tables
  status/current/          active choices, rivals, objections and owners
  status/selections/       original selection objects, retained with scope notices
  status/conflicts/        older-law and migration gaps by system
  authority/, settlement/, founding/, method/
                           supporting current research packages
  history/                 decision trail and real-world gates
  2026-*/                  dated studies and preserved predecessors
```

Read the short entry point, then open the one topic file that owns the
question. Current design choices are not maintained as one giant manuscript. Dated
directories remain at their established paths because prior records cite
them; moving them would break the evidence and predecessor trail.

| To do this | Start here |
|---|---|
| Use the frozen first edition | [Edition 1 release, archive and checksums](2026-11-first-edition/README.md) |
| Find questions for a later revision | [Next edition docket](2026-11-first-edition/NEXT-EDITION.md) |
| Understand the current national settlement | [National settlement](NATIONAL-SETTLEMENT.md) and [detailed country design](COUNTRY-DESIGN.md) |
| Validate the opening as one country | [Authority, resources and lived receipt](settlement/first-round-mandate/05-verify-the-first-mandate-as-one-country.md) |
| Trace a change of government and its next budget | [First-term operating exercise](settlement/first-round-mandate/04-government-change-and-the-next-budget.md) |
| Follow one whole-country system | [Four system maps](country/systems/README.md): democratic power, material life, shared limits, knowledge and change |
| Edit a specific institution | [C01–C14 chapter map](country/README.md) → the relevant numbered topic file |
| Check cross-chapter obligations | [Operating map](country/INTEGRATION.md), [current commitment inventory](settlement/commitments/README.md) and [social/fiscal settlement](SOCIAL-FISCAL-SETTLEMENT.md) |
| Find what is selected, disputed or unfinished | [Design status](DESIGN-STATUS.md), [four active decision registers](status/01-current-selections.md), [whole-objective completion](DESIGN-COMPLETENESS.md) and the [functional audit](COVERAGE-AUDIT.md) |
| Test legal founding and operation | [Authority and transition](AUTHORITY-AND-TRANSITION.md) and [founding and stress](FOUNDING-AND-STRESS.md) |
| Change the research method | [Framework](FRAMEWORK.md) and [decision template](DECISION-TEMPLATE.md) |
| Trace evidence and earlier choices | [Support map](SUPPORT-MAP.md), [design history](DESIGN-HISTORY.md) and [organization history](history/05-document-organization.md) |

The **current design** lives at the stable entries above and in their linked
short topic files under `country/`, including four cross-chapter system maps,
and under `authority/`, `settlement/`, `founding/`,
`status/`, `method/` and `history/`. Dated `2026-*` directories contain
comparisons, decision records and predecessor snapshots. They are retained
for traceability, not as competing current versions. Start with a current
chapter and consult a dated record only when it bears on that choice.

For an actual revision, change the owning numbered topic first. Update its
chapter entrance only when the topic list changes. Then update the relevant
system map, the integrated summary, the status register and a proportionate
decision record if the substantive country choice changes. Do not copy a
second full version of the topic into those indexes. Each audit finding belongs
to exactly one file under `coverage/`; the audit entrance is navigation only.

A consequential selection updates the affected topic, the [integrated
overview](COUNTRY-DESIGN.md) and [status](DESIGN-STATUS.md) together, with a
preserved predecessor and proportionate decision record. Reorganizing a file
or updating this index does not adopt a new rule, permit publication or create
legal authority.

Run `python3 scripts/check-research-structure.py` from the repository root
after an edit to catch broken local links, orphaned chapter topics, oversized
current files and duplicated functional-audit ownership. It leaves dated
research editions untouched.
