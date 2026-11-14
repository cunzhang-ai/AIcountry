# Consistent updates by a human and AI community

Start with [the proposed framework](framework.md), then use the
[update contract](update-contract.md) to prepare or review a concrete change.

This iteration changes the research logic only. It does not modify the website,
production controller, legal library, current community permissions or deployment.
The offline checker is an executable specification, not an operational decision
maker or a substitute for independent institutional review.

## Files

- `framework.md`: six consistency obligations, participation, roles, objections,
  integration, reassessment, appeals and revision of the procedure itself.
- `update-contract.md`: shared human/AI contributor, reviewer and decision handoffs.
- `reference_model.py`: pure checks against declared, bounded fixture records.
- `test_reference_model.py`: twenty synthetic adversarial cases.
- `worked-example.json`: one complete example with exact review-subject digests.
- `validation.json`: recorded results and scope of executed checks.
- `iteration-record.md` and `source-manifest.json`: provenance, critique and handoff.

Run from the repository root:

```sh
python3 research/2026-09-community-consistency/test_reference_model.py
```

The model's inputs are a selected reference snapshot, candidate changes, a complete
**declared** material-objection set and reviews. Its validation routine defines the
exact supported record shape; the worked example instantiates it. Unknown fields
are rejected. Revisions are opaque fixture identifiers, not authenticated content
hashes. The digest covers the whole supplied state, not undiscovered external data.

Each resource account identifies one resource in one context and period, in one
unit. Existing commitments are allocated by selected records; `reserved` covers
contingencies rather than repeating those commitments. Duplicate accounts for the
same resource/context/period are rejected even when given different names or units.
This prevents declared aliases from spending the same capacity twice; it cannot
infer that differently named real-world resources are secretly the same workers.

`exclusive` means a scalar commitment explicitly declared to have one value for
its key/context/period. It is not a general logic solver for natural-language laws.
Different contexts can hold alternative assumptions. A dependency cycle is held
for joint assessment; the model does not implement a cycle-qualification override.

Role eligibility, controller relationships, reasons and semantic findings are
supplied declarations. The model checks their structure and consequences but not
their truth. Triage, issue classification, representation, appointment, source
integrity, appeals and political judgments are deliberately not automated.
`eligible_for_publication_consideration` grants no right to publish.

The protocol describes future bounded review and possible reuse of unaffected
checks; this model deliberately uses strict whole-subject review invalidation,
matching the conservative spirit of the current edition gate. It does not count
endorsements or implement a voting system. No storage, network or model is needed.
