---
type: Open Questions
title: Zipper Merge Lab Open Questions
description: Material unresolved modelling and tooling matters that affect later work.
tags: [zipper-merge, open-questions]
status: draft
generated:
  by: anthropic/claude-opus-5-5
  at: "2026-10-20T13:30:00-04:00"
sources:
  - id: model-log
    resource: ../docs/model-log.md
    title: Model Revision Log
---

# Open questions

1. **Freeway zipper capacity penalty (6–12%).**
   - *Why it matters:* the penalty runs against field evidence and drives the
     headline result.
   - *Evidence:* [model log §21](../docs/model-log.md). Through drivers reacting
     later (10 m + 1 s·v) restores about 1,494 veh/h at saturation, but brings
     back batching.
   - *Owner:* the repository owner.
   - *Hold:* treat any freeway throughput claim as provisional.
2. **No reproducible metrics harness in the repo.**
   - *Why it matters:* the headline numbers cannot be re-run after model changes.
   - *Evidence:* the [project state](project-state.md) verification boundary.
   - *Fix:* add a small Node script that runs the page's simulation headlessly.
   - *Owner:* the repository owner, if they want it.
3. **Unverified assumptions.**
   - *Why it matters:* they set the defaults people see.
   - *Assumptions:* the urban capacity target (1,400 pc/h/ln), the heavy-vehicle
     class split, and the exact HCM heavy-vehicle default table.
   - *Owner:* the repository owner, using local MTO or agency data.
