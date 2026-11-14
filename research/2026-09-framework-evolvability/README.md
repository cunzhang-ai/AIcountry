# Framework evolvability proposal 2.0

Read [the framework](framework-v2.md) and use the
[future-compatible worksheet](update-contract-v2.md). Start from the shared
[research index](../FRAMEWORK.md) when continuing this work later.

This proposal extends the community-consistency framework with module contracts,
capability-aware representations, explicit compatibility and migration, selective
reuse of supporting checks, and evaluation of the improvement process itself.
Previous artifacts are preserved byte-for-byte. There is no website or runtime edit.

## Concrete artifacts

- `framework-v2.md`: the proposed logical design and boundaries.
- `update-contract-v2.md`: practical human/AI handoff, building on the v1 contract.
- `evolution_planner.py`: pure offline planning and exact dependency fingerprints.
- `test_evolution_planner.py`: twenty synthetic adversarial regression cases.
- `worked-examples.json`: reproducible unrelated-update and workforce-correction examples.
- `transition-map.json`: what v2 changes and what remains governed by v1 or current authority.
- `open-questions.json`: bounded next investigations, with unknown ownership explicit.
- `iteration-record.md`, `source-manifest.json`, `validation.json`: provenance and results.

Run from the repository root:

```sh
python3 research/2026-09-framework-evolvability/test_evolution_planner.py
python3 research/2026-09-community-consistency/test_reference_model.py
```

## What the planner means

`ready_for_migration_review` only means the supported structural planning checks
found no declared gap. It can coexist with `rerun_required` supporting checks.
Neither status permits publication, waives further checks or certifies the design.
The output always requires fresh final review; the earlier consistency gates remain
applicable, including rights, resources, independence and objection closure.

Snapshots contain exact module revisions and dependency pins, plus a context and
procedure. The planner computes check scope transitively, compares both original
and candidate fingerprints, and checks declared method revisions, coverage, status
and date validity. Expiry dates are inclusive UTC calendar dates in these fixtures;
production would need a specified clock and more precise time semantics.

Method and module revision identifiers are declared, not authenticated. The planner
rejects a changed module reusing its revision within the supplied pair, but cannot
verify a global registry or hidden changes outside the export. Fingerprints are
canonical only under this local Python serialization; cross-language signatures
would need a separately specified canonical encoding and verification protocol.

Unknown annotations survive unchanged. Unknown semantic extensions, module kinds
or schemas produce planning gaps; unsupported semantics in a check's dependency
scope also prevent reuse. Annotation classification is a declaration subject to
review, not a permission to hide behavior in metadata. No payload is executed.

Migration covers declared transitive consumers for one-to-one changes and retirement.
It requires ownership, explicit obligation and loss assessments, validation status
and recovery. “Passed” is supplied testimony, not independently verified completion.
Many-to-many splits/merges, real consultation, automatic investigation, role
appointments and appeals are described in the framework but not implemented here.

The planner cannot infer hidden dependencies, semantic equivalence, actual rights
or resource safety. Cycles are held for joint assessment; the model does not offer
an override. It conservatively invalidates a supporting check if any included
module changes, including annotations. Selective annotation-level reuse is deferred.

These modules are research artifacts. No attempt was made to load them as a live
API, migrate a database, execute an AI review or amend a national edition.
