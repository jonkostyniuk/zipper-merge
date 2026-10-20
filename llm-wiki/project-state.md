---
type: Project State
title: Current Zipper Merge Lab State
description: Resumable state, headline results, and verification boundary for the zipper merge demo.
tags: [zipper-merge, microsimulation, work-zone, current-state]
status: draft
generated:
  by: anthropic/claude-opus-5-5
  at: "2026-10-20T13:30:00-04:00"
sources:
  - id: lab
    resource: ../zipper-merge-lab.html
    title: Zipper Merge Lab (simulation, method text, and parameter tables)
  - id: research
    resource: ../docs/research.md
    title: Zipper Merge Research Findings
  - id: model-log
    resource: ../docs/model-log.md
    title: Model Revision Log
---

# Current handoff

Revision 8 of `zipper-merge-lab.html` is current. The owner reviewed it and judged
it ready to share as a fun, illustrative demo. It is not a design or
calibrated-analysis tool.

## What exists

- **One self-contained HTML page** with four panels, all 2→1 lanes: freeway zipper,
  freeway conventional, urban zipper and urban conventional. Each zipper/conventional
  pair gets the same seeded arrivals and drivers.
- **Model:**
  - IDM car-following and MOBIL lane changes, with forced and cooperative merging.
  - One assertiveness trait z ~ N(μ, σ) per driver sets all of their parameters.
  - Three vehicle classes: car, single-unit truck and tractor-semitrailer.
  - The OTM Book 7 taper is tied to each speed slider.
- **Compliance (zipper panels):** applies to drivers in both lanes.
  - Sign followers use both lanes to the taper and take turns. In the open lane they
    yield with c = 1.5, which gives 94% / 71% / 29% at z = 0 / 1 / 2.
  - Non-followers merge early, or treat a late merger as a cutter (c = −0.3).
  - Merging alternates 1-for-1. A stopped lead car gets let in, with pressure rising
    every 6 s.
- **The conventional panels** have been unchanged since revision 7.

## Headline results (headless runs, 6–8 seeds)

Saturated throughput in veh/h, zipper vs. conventional:

| Vehicle mix | Freeway | Urban |
|---|---|---|
| Car only | 1,588 vs 1,707 | 1,497 vs 1,372 |
| Default trucks | 1,374 vs 1,561 | 1,435 vs 1,282 |

- **Urban:** the zipper is better on queue, delay and throughput. This has held in
  every revision.
- **Freeway:** the zipper shows a longer queue and 6–12% less throughput near
  capacity. The result is sensitive to the courtesy-rule tuning: a later reaction
  gives about −4% but loses the alternation.
  - This is less favourable to the zipper than the field evidence
    ([research §2](../docs/research.md)), so present it as a modelling outcome,
    not a finding.
  - It is tracked in [open questions](open-questions.md).
- **Low demand (Sunday preset):** the two layouts are indistinguishable.

## Industry-conformance position

- **Structure:** the same as commercial microsimulation (car-following, mandatory
  lane change, cooperative yielding, driver-type spread). Vissim uses Wiedemann
  and Aimsun uses Gipps, not IDM/MOBIL.
- **Assumptions:** driver types are one linked trait, and the yield curve is a
  behavioural assumption.
- **Calibration:** capacity is tuned to HCM-style targets. It is not calibrated or
  validated against field data.

## Verification boundary

- The page script parses with `node --check`.
- On 2026-10-19 the page loaded in Chrome without console errors, and the freeway
  zipper panel showed both lanes queued to the taper.
- All results above come from headless Node harnesses. Those harnesses were
  session scratch files and are **not** in this repository, so the numbers cannot
  be reproduced from the repo alone.
- No validation against field counts has been done.

## Next step

None is pending. The owner intends to commit and share the page. Durable choices
are in [decisions](decisions.md); the build history is in the
[model log](../docs/model-log.md).
