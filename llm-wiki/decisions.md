---
type: Decision Register
title: Zipper Merge Lab Decisions
description: Durable owner-directed choices that shape the simulation, with evidence locations.
tags: [zipper-merge, decisions]
status: draft
generated:
  by: anthropic/claude-opus-5-5
  at: "2026-10-20T13:30:00-04:00"
sources:
  - id: model-log
    resource: ../docs/model-log.md
    title: Model Revision Log
  - id: lab
    resource: ../zipper-merge-lab.html
    title: Zipper Merge Lab
---

# Decisions

Each entry was directed by the owner in the build conversation (2026-10-19) unless
it is marked *agent choice*. The evidence is the cited section of the
[model log](../docs/model-log.md) and the page's method text.

1. **Four panels, 2→1 lanes only:** freeway and urban, zipper and conventional. The
   funnel ("lanes merge") configuration was dropped. Evidence: log §9.
2. **A visual demo, not a calibrated microsim.** Keep the model simple. Demand is
   set in veh/h near capacity, not as a macro-style over-capacity scenario. Live
   metrics update as sliders change. Evidence: log §15–16.
3. **Driver behaviour comes from one bell-curve trait.** Assertiveness z ~ N(μ, σ)
   drives all IDM/MOBIL and yield parameters, with fun sliders. Evidence: log §9;
   page "Parameter mapping".
4. **Separate freeway and urban controls.** Freeway runs at 80–120 km/h and urban at
   40–70 km/h (default 50). The speed and taper sliders are combined because OTM
   Book 7 ties the taper to the posted speed. Evidence: log §13, §17.
5. **Heavy vehicles are to scale.** Car 4.8 m, single-unit truck 10 m and WB 21 m.
   Defaults are 12% freeway and 3% urban. The single-unit/WB split is an
   *agent choice*. Evidence: log §13; page "Heavy vehicles".
6. **Capacity is tuned to queue-discharge targets:** 1,600 pc/h/ln freeway (HCM
   short-term work zone) and 1,400 pc/h/ln urban (an assumption). Evidence: log §16.
7. **Compliance applies to both lanes, and its effect scales with aggression.**
   Strict 1-for-1 alternation is kept even though it costs freeway capacity. The
   owner accepted the trade-off ("Sounds good") rather than tuning for throughput.
   Evidence: log §21.
8. **The freeway result is framed as a modelling outcome,** with the industry
   conformance caveats stated on the page. Evidence: page "Capacity calibration"
   and "Limits".
