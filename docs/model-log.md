# Model Revision Log

_Dated record of how the simulation was planned, built, and revised (revisions 1–8, 2026-10-19). Originally sections 7–21 of `FINDINGS.md`; section numbers are kept. Earlier results and open items here are superseded by later revisions. The current state lives in [`llm-wiki/project-state.md`](../llm-wiki/project-state.md); the research is in [research.md](research.md)._

## 7. Proposed animations (2–4 side by side) — DRAFT
Same demand, same single-lane bottleneck capacity in each panel. Live readouts: queue length, merges/min, # conflicts (hard brakes / forced merges).

1. **Early merge, everyone complies** — single long queue, closing lane empty.
2. **Zipper, everyone complies** — two short queues, smooth 1:1 alternation.
3. **Mixed behaviour (realistic)** — some early, some late, some blockers refusing gaps → forced merges, stop-and-go.
4. **Funnel ("Lanes Merge")** — both lanes taper; no priority; hesitation modelled.

Possible toggles: freeway vs. urban (short storage + upstream signal), demand level (low vs. high), % compliant drivers slider.

## 8. Open questions
- [ ] Which 4 panels? Or swap one for **urban short-storage** case?
- [ ] Should freeway/urban be a toggle or separate panels?
- [ ] Include a demand slider to show "low volume → early is fine"?
- [ ] Driver-behaviour parameters: % zipper-compliant, % blockers, gap-acceptance time — use rough defaults or values you have from practice?
- [ ] Funnel: how do you want priority resolved in the model (random, first-to-taper, hesitation delay)?
- [ ] Output: interactive web page (shareable link) vs. exported GIF for group chat?

---

## 9. Decisions (2026-10-19)
- Panels: **Freeway zipper · Freeway conventional · Urban zipper · Urban conventional** (2→1 lanes only). Funnel dropped.
- Driver behaviour: one assertiveness trait z ~ N(μ, σ) per driver drives all parameters (IDM T, s₀, a, v₀; MOBIL p, b_safe; yield probability). User-adjustable μ, σ, zipper compliance, demand.
- Yield vs. fight: P(yield) = 1/(1+e^(1.8(z−c))). c is higher when zipper signs set a turn-taking norm, and lower toward late "cutters" at a conventional closure. Non-yielders with z > 0.5 close the gap (headway × 0.55).
- Deliverable: self-contained `zipper-merge-lab.html` (no build, opens offline except Google Fonts).

## 10. Model sources added
- Treiber, Hennecke & Helbing (2000) IDM · Kesting, Treiber & Helbing (2007) MOBIL, TRR 1999
- Hidas (2005) forced/cooperative merging, Transp. Res. C 13(1)
- FHWA-HRT-07-030 NGSIM cooperative/forced merge · Lee (2006) MIT single critical-gap merge model · Kondyli & Elefteriadou ramp-merge behaviour
- WisDOT Vissim guidelines (CC1 0.9 s default, 0.7–3.0 s) · LaDOTD Vissim calibration

## 11. What the model showed at defaults in revision 1 (superseded; see Current state)
| Preset | Freeway queue Z / C | Freeway thru Z / C (veh/h) | Urban queue Z / C | Urban thru Z / C |
|---|---|---|---|---|
| Real world | 1.39 / 1.95 km | 1104 / 1188 | 510 / 557 m | 1116 / 1188 |
| Textbook | 1.40 / 2.24 km | 1056 / 1116 | 514 / 745 m | 1068 / 1056 |
| Friday 5 pm | 1.42 / 1.89 km | 1356 / 1428 | 387 / 379 m | 1380 / 1440 |
| Sunday drive | ~0 / ~0 | 996 / 972 | 13 / 13 m | 636 / 624 |

Read: zipper cuts the freeway queue by about 25–40%. Throughput is within a few percent either way. Urban shows little difference, because the queue overruns the short storage and the upstream signal in both setups. At low demand, the two are indistinguishable. Conflicts are mostly comparable, and they are higher wherever more drivers merge at a single point.

## 12. Open items (revision 1; resolved: trucks added in rev 2, capacity recalibrated in rev 3)
- [ ] Single-lane throughput (~1100–1400 veh/h) sits at the low end of work-zone capacity. Lower base T if you want 1500+.
- [ ] No trucks. Adding ~10% heavy vehicles would sharpen the urban case.
- [ ] Should the zipper signs be dynamic (active only when congested, like MnDOT's)?

---

## 13. Revision 2 (2026-10-19)
**Per-scenario road sliders**
- Freeway: work zone speed 80–120 km/h (default 80). Taper 220–300 m (default 300). Heavy vehicles 0–30% (default 12%; split 35% single-unit / 65% tractor-semitrailer).
- Urban: work zone speed 40–70 km/h (default 50). Taper 60–200 m (default 60). Heavy vehicles 0–15% (default 3%; split 70/30).

**OTM Book 7 (Apr 2022 Field Edition) taper length for full lane closure, by normal posted regulatory speed (NPRS)**
| | 50 | 60 | 70 | 80 | 90 | 100 | 110 |
|---|---|---|---|---|---|---|---|
| Non-freeway (short/long duration layouts) | 60 | 85 | 155 | 180 | 200 | – | – |
| Freeway | – | – | – | 220 | 250 | 300 | 300 |
- Freeway LBA: 60 / 75 / 95 / 110 m (80–110 km/h). Freeway max marker spacing is 12 m at 80 km/h and 24 m at 90–110; non-freeway is 6–12 m.
- OTM sizes tapers on the normal posted speed, not the reduced work zone speed, so taper and speed are separate sliders.

**Vehicles (drawn to scale; lane width 3.75 m freeway / 3.5 m urban)**
- Car / light-duty: 4.8 × 1.9 m. Single-unit truck: 10 × 2.6 m (AASHTO SU-30 9.1 m, SU-40 12.0 m). Tractor-semitrailer: 21 × 2.6 m (AASHTO WB-62 21.0 m; TAC WB-20 ≈ 22 m).
- Trucks: headway +0.3/+0.5 s, s₀ +0.5 m, a ≈ 0.8/0.5 m/s², v₀ capped at 110/105 km/h (Ontario 105 km/h limiter), and they accept 30% less braking imposed on others.

**Heavy-vehicle defaults:** 12% freeway and 3% urban are HCM/NCHRP 599-style defaults. I could not open the NCHRP 599 tables to confirm them. Ontario 400-series corridors often run well above 12%, so use MTO counts for a real site.

**Taper behaviour:** the closing lane may roll into the first ⅓ of the taper while shifting left along the cone line. It never enters the coned area. Throughput is counted at that point.

## 14. Open issue: zipper throughput penalty
With trucks, the zipper panels show 5–25% lower throughput than conventional. The cause is stop-start merges at the lane end, and trucks needing long gaps from rest. That is more pessimistic than the field evidence. Candidate fixes:
- Anticipatory gap creation: through-lane drivers adjust speed earlier, like Vissim's cooperative lane change.
- Let mergers in the zone accept gaps while rolling at matched speed.
- Calibrate against a target work-zone capacity (~1,500–1,700 veh/h).

---

## 15. Microsim review (2026-10-19)
**Vehicle mix: confirmed.** Each arrival is a per-vehicle random draw. In a 10-min run the arriving mix came out at freeway 87.7% car / 5.0% SU / 7.3% WB (12.3% HV vs. 12% set) and urban 96.2 / 2.6 / 1.3 (3.8% vs. 3%). That's within sampling noise. Demand is in veh/h with trucks taking real space, so no PCE conversion is needed, which is correct for micro. The SU/WB split is still an assumption to check against local classification counts.

**Demand: needs correcting.** The slider is a % of a nominal 1800 (fwy) / 1300 (urb) veh/h, but the model's *saturated discharge* (its actual capacity) is lower:
| | 0% HV | 12% / 3% HV |
|---|---|---|
| Freeway zipper / conv | 1128 / 1284 veh/h | 960 / 1116 veh/h |
| Urban zipper / conv | 1104 / 1080 veh/h | 1080 / 1080 veh/h |
So the default 115% is about 165–215% of model capacity on the freeway (and the 150% max is up to ~280%), and about 140% urban. Under sustained oversaturation the queue grows as (demand − capacity) × time, so queue results mostly reflect run length and small capacity differences.

**Proposed fix**
- Separate demand sliders in veh/h per context (e.g. freeway 600–1,800, urban 300–1,400), with a live v/c readout against the model's measured capacity.
- Calibrate the model's work zone capacity to a target first, then express demand as v/c of about 0.6–1.15.
- Time-varying demand profile (15-min steps: ramp up → peak slightly over capacity → ramp down) after a warm-up. Report max queue, total delay, time to clear, and unserved (latent) demand. Use multiple seeds per FHWA Traffic Analysis Toolbox Vol. III.

---

## 16. Revision 3 (2026-10-19): capacity calibration + demand in veh/h
- **Capacity definition used:** the queue discharge rate, i.e. the maximum sustained flow through the single open lane once a queue exists. It is lower than the pre-breakdown flow at speed.
- **Targets:** freeway 2→1 work zone 1,600 pc/h/ln (common HCM short-term work zone base). Urban 1,400 pc/h/ln (assumption; replace with a local value).
- **Calibrated parameters:** mean headway T 1.5 → 1.2 s, standstill gap s₀ 2.0 → 1.5 m, acceleration a 1.2 → 1.4 m/s². Cooperative yielding limited to the through-lane vehicle directly behind a merger (30 m freeway / 20 m urban), as in Vissim cooperative braking.
- **Measured saturated discharge (5 seeds):**
  - Freeway, car only: ≈1,600 avg (zipper 1,470 / conventional 1,730). With 12% trucks: ≈1,320 (HCM E_T = 2.0 estimate 1,430; model behaves like E_T ≈ 2.7).
  - Urban, car only: ≈1,420 (zipper 1,435 / conventional 1,400). With 3% trucks: ≈1,350 (estimate 1,360).
- **Demand:** separate veh/h sliders. Freeway 400–2,000 (default 1,500, v/c 1.05). Urban 200–1,600 (default 1,450, v/c 1.07). The v/c readout uses the target capacity adjusted for trucks. Presets set v/c (1.05 / 1.05 / 1.15 / 0.55).
- **Live metrics:** a rolling 5-simulated-minute window that updates continuously as sliders change. Slider changes apply to new arrivals.
- Tried and rejected: a Vissim-style safety distance reduction factor of 0.6 on merges (made the zipper worse).

**Still open:** on the freeway, the zipper's saturated discharge is 8–15% below conventional because its merges sit at the head of the bottleneck. That's a real mechanism, but the size of the penalty is larger than field studies report. Near v/c ≈ 1, this can flip the queue comparison in favour of conventional.

---

## 17. Revision 4 (2026-10-19): rolling zipper + combined speed/taper
- **Speed and taper are one slider per context.** Taper follows OTM Book 7 for the selected speed.
  - Freeway 80/90/100/110/120 → 220/250/300/300/300 m (120 uses the 110 value).
  - Urban 40/50/60/70 → 60/60/85/155 m (40 uses the 50 value).
- **Rolling merge (gap seeking):** closing-lane drivers in the merge zone match the through-lane speed. If there's no room ahead, they ease back into the next gap, so they merge while rolling instead of driving to the lane end and stopping.
- **Truck interactions:**
  - Drivers give way to merging trucks more readily (yield curve shifted by 0.8).
  - Mergers won't cut in if it makes a truck brake harder than 1.5 m/s².
  - Trucks no longer get a reduced braking-acceptance factor.
  - These match the cooperative/forced merge findings (Kondyli & Elefteriadou).
- **Recalibrated:** mean headway T̄ 1.35 s freeway / 1.3 s urban (separate behaviour sets per link type, as in Vissim).

**Saturated discharge, 8 seeds**
| | Car only (zipper / conventional) | Default trucks (zipper / conventional) |
|---|---|---|
| Freeway | 1,485 / 1,560 (−5%) | 1,365 / 1,385 (−1.6%) |
| Urban | 1,435 / 1,350 (+6%) | 1,385 / 1,335 (+4%) |
The freeway zipper penalty was −15% in revision 3.

**Presets, 8 seeds (queue, zipper vs. conventional)**
| Preset | Freeway | Urban |
|---|---|---|
| Real world (v/c 1.05) | 277 vs 178 m | 132 vs 267 m |
| Textbook (polite, 95% comply) | 529 vs 66 m | 187 vs 416 m |
| Friday 5 pm (pushy, v/c 1.15) | about equal (52 vs 60 m) | about equal (47 vs 62 m) |
| Sunday (v/c 0.55) | no queues | no queues |
Pushy drivers raise effective capacity, which is why Friday barely queues.

**Remaining caveat:** near capacity on the freeway, the zipper can still queue more than conventional, most of all with very polite, very compliant drivers who wait for big gaps. Under heavy saturation, queues and delay come out about equal.

---

## 18. Revision 5 (2026-10-19): stuck trucks + zipper compliance bugs
**Diagnosis (instrumented runs, 80% compliance)**
- **Trucks stuck:** tractor-trailers waited up to 393–559 s at the lane end. The through-lane driver only yielded if a gap ahead of the merger already existed, and a 21 m truck in a queue almost never had one.
- **Zipper not followed:** the median zipper merge was 196 m before the taper, at the start of a 200 m merge zone. Drivers took the first gap instead of merging at the merge point.
- **Lanes unbalanced:** the closing lane held about 2× the through lane (92 vs 50), because late-planning drivers could move into the closing lane but never back.

**Fixes**
- **Long-wait courtesy:** a merger stopped for more than 20 s gets room from the driver behind, even if no gap ahead exists yet. Max truck wait is now about 80–150 s in a crawling queue.
- **Merge zone shortened** to 60 m freeway / 25 m urban before the taper start. Median zipper merge is now −24 to +5 m from the taper start.
- **Two-way MOBIL lane choice upstream** for late-planning drivers. Lanes are now balanced (≈43/43 to 57/54).
- **Rejected:** a looser yield rule that yields with no room ahead. It cost about 11% throughput in both layouts.

**Saturated discharge, 8 seeds (zipper / conventional, veh/h)**
| | Car only | Default trucks |
|---|---|---|
| Freeway | 1,516 / 1,554 | 1,419 / 1,462 |
| Urban | 1,435 / 1,393 | 1,432 / 1,359 |

**Presets, queue m (zipper vs. conventional)**
| Preset | Freeway | Urban |
|---|---|---|
| Real world 60% compliance | 335 vs 213 | 109 vs 224 |
| Real world 80% compliance | 294 vs 213 | 95 vs 224 |
| Textbook | 381 vs 57 | 200 vs 421 |
| Friday | 160 vs 133 | 49 vs 67 |
| Sunday | 0 vs 0 | 3 vs 3 |

---

## 19. Revision 6 (2026-10-19): actual zipper turn-taking
**Diagnosis:** the order of vehicles passing the taper showed batches of about 4–20 closing-lane merges in a row, then 5–20 through cars (e.g. `TTTTTTTTTTZZZZZZZZZZZZZZ`), instead of 1:1. Causes:
1. Nobody gave the lead closing-lane car its turn. A through driver only yielded if a gap ahead already existed.
2. Closing-lane cars rolled alongside through cars, up to about 70 m into the taper, instead of tucking in behind them.
3. A car that had just merged acted as a fresh through driver and let the next closing-lane car in, so the whole closing-lane queue chained in.
4. A 20 s "long wait" bypass let almost everyone skip their turn in stop-and-go traffic.
5. Upstream early merges set the "already let one in" flag on drivers, who then reached the taper marked as having had their turn.

**Fixes (zipper panels only)**
- **Lead merger gets a turn:** the through driver behind the lead closing-lane car re-decides at the zipper-norm rate, and holds back even before the gap ahead has opened.
- **One car each:** each through driver lets in one car. A just-merged car has also had its turn, so the next merger waits for the next through car. Exceptions: a clear gap, z > 1.3, or a wait over 60 s.
- **Tuck in:** a closing-lane car with a through car alongside eases back and tucks in behind it.
- **Flag scope:** the "let one in" flag is now only set by merge-zone merges.
- **Queue metric:** gap tolerance 150 → 400 m freeway (40 → 80 m urban). It was truncating stop-and-go queues.
- **Defaults:** zipper compliance 80% (presets: Textbook 95, Real world 80, Friday 50, Sunday 80).

**Result:** crossing runs dropped from about 6 through : 4 merges to about 4 : 2. Bursts now only occur on clear gaps or long waits.

**Presets, 8 seeds: zipper vs. conventional**
| Preset | Freeway queue | Freeway delay | Urban queue | Urban delay |
|---|---|---|---|---|
| Real world 80% | 266 vs 135 m | 110 vs 53 s | 105 vs 283 m | 75 vs 162 s |
| Textbook 95% | 406 vs 53 m | 132 vs 60 s | 177 vs 442 m | 120 vs 265 s |
| Friday 50% | 129 vs 131 m | 72 vs 66 s | 51 vs 67 m | 45 vs 48 s |
| Saturated, car only | 1,673 vs 1,905 m | 344 vs 381 s | 532 vs 730 m | 246 vs 343 s |
| Saturated, trucks | 2,192 vs 1,748 m | 476 vs 479 s | 602 vs 814 m | 284 vs 380 s |

**Saturated throughput (veh/h, zipper vs. conventional):** freeway car-only 1,710 vs 1,660; freeway trucks 1,455 vs 1,509; urban 1,467 vs 1,281 (car) and 1,434 vs 1,237 (trucks).

**Still open:**
- Near capacity on the freeway (v/c ≈ 1.05), the zipper discharges about 7% below conventional and queues longer.
- Capacity shifted with these changes (freeway conventional ~1,660 car-only, urban conventional ~1,280). This needs a recalibration pass.

---

## 20. Revision 7 (2026-10-19): stopped lead car gets let in
**Request:** a lead car stopped at the lane end should be let in in some manner. Not every driver complies, but drivers should visibly slow.

**Changes (built on revision 6)**
- **Escalating pressure:** if the lead closing-lane car is stopped (v < 2 m/s) within 20 m of the lane end, the through driver behind it re-decides every 6 s. The yield curve shifts by up to 2 units of z (wait/10 s). Applies in both modes.
- **Persistent yield:** once a driver starts making room (`yTo`), they keep holding back (up to 3 m/s²) instead of abandoning the yield when the gap tightens.
- **Firmer braking to let in:** a merger may cut in ahead of a driver who is letting it in if that driver brakes up to 4 m/s² (vs the normal b_safe).

**Rejected along the way**
- **Forcing the driver behind the lead car to consider it at all times:** gave a perfect 1:1 zipper, but the freeway lost ~19% throughput because merges moved to the lane end.
- **Shorter hold-back headways (×0.5, ×0.3):** no gain.
- **A 2.5 m cushion with yields persisting while overlapped:** deadlock. A stopped yielder sat alongside the lead car forever.

**Results, 6–8 seeds (zipper vs. conventional)**
| | Freeway thru | Freeway queue | Freeway delay | Urban queue | Urban delay |
|---|---|---|---|---|---|
| Real world (v/c 1.05, 80%) | 1,412 vs 1,392 | 264 vs 298 m | 104 vs 71 s | 83 vs 214 m | 62 vs 129 s |
| Textbook (95%) | 1,402 vs 1,453 | 392 vs 152 m | 129 vs 84 s | 190 vs 393 m | 120 vs 231 s |
| Friday 5 pm (50%) | 1,635 vs 1,543 | 128 vs 189 m | 73 vs 84 s | 46 vs 67 m | 47 vs 50 s |
| Sunday | 793 vs 799 | 0 vs 0 | 8 vs 9 s | 4 vs 3 m | 22 vs 20 s |
| Saturated, trucks | 1,502 vs 1,446 | 2,185 vs 1,861 m | 428 vs 487 s | 557 vs 720 m | 269 vs 347 s |
| Saturated, car only | 1,642 vs 1,706 | 1,671 vs 2,170 m | 362 vs 391 s | 555 vs 632 m | 238 vs 296 s |

- Merges happen at the taper start (median −11 to −2 m). Turn-taking is about 4 through : 2 merges, not a strict 1:1.
- The freeway zipper now matches or beats conventional on throughput in most cases. Near capacity its delay is still higher. Under the Textbook preset it still queues longer.

## 21. Revision 8: compliance drives the zipper turn-taking

**User feedback:** at 80% compliance, that 80% should actually produce zipper behaviour, with the chance of letting someone in depending on how aggressive the driver is.

**Diagnosis:**
- The compliance slider only controlled closing-lane lane use. Through-lane drivers ignored it.
- A sequence log at the taper showed batching (ZZZZZZZZ / TTTTTTTTTT), not alternation. Only 16–36% of merges came from a follower choosing to yield.
- Bug 1: a through driver decided "yes" too late. By then, opening a gap took more than 3 m/s², so they rolled past. One lead car waited 113 s while about 20 willing drivers passed.
- Bug 2: through drivers checked the nearest closing-lane car (the second car in the queue), not the lead car. They only noticed the lead car once they were alongside it.
- The 60 s skip-the-turn bypass caused reverse-order chain merges.

**Changes:**
- Every driver has a `comply` flag drawn from the slider.
- In the zipper panels, sign followers yield with c = 1.5: 94% at z = 0, 71% at z = 1, 29% at z = 2. Non-followers use the cutter curve, c = −0.3, which gives 37% at z = 0.
- Explicit, stateless turn rule. If the open-lane car just ahead of the lead merger is a car that merged at the taper, it is the through lane's turn. Otherwise it is the closing lane's turn.
- The through driver directly behind the lead car decides, and holds back from 12 m + 1.5 s·v. Hold-back braking is up to 4 m/s², and also applies below 5 m/s.
- A merger being let in accepts tighter gaps. A merger with a through car alongside drops back more firmly, to that car's speed minus 3 m/s.
- The conventional panels are unchanged from revision 7.

**Results** (freeway, default demand, seed 1):

| Compliance | Follower chose to yield | Avg merge run |
|---|---|---|
| 0% | 26% | |
| 50% | 45% | |
| 80% | 75% | 1.01 |
| 100% | 81% | 1.01 |

- Turn-taking is now visibly 1-for-1, with about 2 through cars per merge on the freeway and about 1.6–2.2 on urban.

**Trade-off (6 seeds, throughput/queue/delay, zipper vs. conventional):**

| Preset | Freeway zipper | Freeway conventional |
|---|---|---|
| Real world | 1332 / 462 m / 177 s | 1416 / 273 m / 80 s |
| Saturated | 1390 | 1564 |

- Urban zipper is still better than conventional: Real world 1382 / 149 / 95 vs. 1302 / 252 / 147.
- Strict courtesy at crawl speed slows the open lane at the taper. Lane-end crossing speed is about 7–8 m/s vs. about 11 m/s under conventional, so freeway capacity drops about 6–11%.
- Reacting later to the lead car restores capacity (1,494 at saturation), but alternation collapses back to batching.
- Field evidence on zipper throughput is mixed, so this is a model trade-off, not a finding.

**Rejected:**
- A token handed back when a through car crossed the taper start. It wasted one through car per cycle (−13%).
- A "one each" flag on followers who gave way. Saturated freeway capacity fell to 910.
