# Zipper Merge Research Findings

_Impartial literature and agency-practice review behind the Zipper Merge Lab. Originally sections 1–6 of `FINDINGS.md` (2026-10-19); section numbers are kept so references elsewhere still resolve. Model-building history is in [the model log](model-log.md)._

## 1. Context
- Audience: friends (argument), but framed by a transportation engineer — must stay impartial and defensible.
- Key lenses (from discussion): driver behaviour (yielding vs. blocking), lane-ownership / "funnel" configs, freeway vs. urban geometry.

## 2. Evidence summary

Confidence key: **High** = multiple agency field studies agree · **Med** = some field data / mixed · **Low** = simulation, opinion, or no direct study found.

| Claim | Confidence | Notes |
|---|---|---|
| Zipper shortens queue length in congestion | **High** | CDOT ~50%; NC I-77 8 mi → 2 mi; MnDOT "much less"; MoDOT 40–50% (promo page) |
| Zipper reduces speed differential between lanes / safer merge | **Med–High** | MnDOT; Arrive Alive. Shorter queue also reduces spill-back into upstream ramps/intersections |
| Zipper improves throughput / travel time | **Low–Med** | MnDOT: no effect on travel time. SEH microsim: 16–42% reduction (modelled). Iowa TPF-5(438): "better use of available capacity." Bottleneck capacity is the hard limit |
| At low volume, early merge is fine | **Med** | Iowa TPF-5(438): drivers merge early at low volume "without any adverse impact on operations" |
| Signage drives compliance | **Med** | Iowa: PCMS raised compliance; text > graphic. FHWA-linked study: advance sign + "merge here / take turns" sign needed. CT alternating-merge sign: +10% desirable merges |
| No national consensus | **High** | FHWA: "no definitive guidance"; Iowa DOT: no consensus |

## 3. Driver behaviour (the real variable)
- **Mixed-strategy failure:** the worst case is half early / half late. Early mergers leave the closing lane empty → late mergers look like "cutters" → blockers (lane-straddlers, gap-closers) form → forced merges at the taper → stop-and-go and conflict.
- **Fairness perception** is a documented reason zipper underperforms in practice (Traffic Safety Store; ABC15 coverage).
- **Gap acceptance:** zipper relies on 1:1 alternation. Any refusal to yield turns a smooth alternation into a hard merge.
- Compliance is a design lever (signage, PCMS, public campaigns e.g. Saskatoon 2013 pilot), not a given.

## 4. Configurations
- **Lane drop ("Lane Ends" / right lane closed):** one lane "owns" the road; closing lane is subordinate. Invites early merging and gatekeeping.
- **Zipper (late merge w/ "Use Both Lanes / Take Turns / Merge Here"):** both lanes used to taper; alternation at a defined point.
- **Funnel / "Lanes Merge" (both lanes taper to one centred lane):** no lane ownership, so neither driver has priority.
  - ⚠️ **No direct study found** comparing funnel vs. lane-ends behaviour. What follows is engineering reasoning, not evidence:
  - Pro: removes the "cutter" narrative; forces alternation by geometry rather than courtesy.
  - Con: ambiguous priority → hesitation, side-by-side jockeying, possibly lower throughput at the taper.

## 5. Freeway vs. urban
- **Freeway work zone:** long advance warning, long storage in both lanes, long taper → proper zipper geometry possible. Most supporting studies are here.
- **Urban arterial:** short block lengths, driveways, intersections, signals upstream. Often no room for adequate storage or a defined merge point; queues spill back regardless. Signals meter flow in platoons, which changes merge dynamics. MoDOT notes irregular setups / speed variation make poor zipper candidates.
- Microsim (SEH) claims benefit on low-speed urban roads too, but that's modelled — treat as low confidence.

## 6. Bottom line from the research (impartial)
- In **congested freeway** conditions with **compliant drivers**, zipper is the better-supported practice: shorter queue, safer, fairer.
- "Everyone gets through faster" is **overstated**; the bottleneck sets capacity.
- At **low volume**, early merging is fine.
- **Behaviour and geometry decide outcomes** more than the method name. A zipper with non-compliant drivers or no room can be worse than a clean early merge.

## Sources
- [MnDOT – Late Merge / Zipper System](https://www.dot.state.mn.us/trafficeng/workzone/doc/When-latemerge-zipper.pdf)
- [Iowa DOT – TPF-5(438) Improving Effectiveness of Zipper Merge (2024)](https://publications.iowa.gov/52208) · [tech brief](https://publications.iowa.gov/52208/2/TPF-5_438__improving_effectiveness_zipper_merge_tech_brief.pdf) · [full report](https://swzdi.intrans.iastate.edu/wp-content/uploads/2025/01/improving_effectiveness_zipper_merge_w_cvr.pdf)
- [CDOT – Zipper Merge Guidelines (2025)](https://www.codot.gov/safety/traffic-safety/assets/documents/zipper-merge-guidelines_20250922.pdf)
- [MoDOT – Zipper Merge](https://www.modot.org/zipper-merge) · [MoDOT doc](https://www.modot.org/media/21649)
- [9News – FHWA tested zipper signs](https://9news.com/article/traffic/federal-highway-administration-tested-signs-zipper-merging/73-ca21cedd-97bd-423d-8658-abd8cdc8dcae)
- [TRB – CT alternating merge sign](https://onlinepubs.trb.org/onlinepubs/trispdfs/01011177.pdf)
- [ConstructConnect – Saskatoon pilot](https://canada.constructconnect.com/?p=67435)
- [Work Zone Safety – ODOT: zipper works, drivers annoyed](https://workzonesafety.org/publication/ohio-department-of-transportation-says-zipper-merge-works-drivers-annoyed/)
- [SEH – Zipper merging microsim](https://www.sehinc.com/news/zipper-merging-optimizing-traffic-flow-and-safety-at-lane-closures)
- [Texas Standard](https://texasstandard.org/stories/stay-in-your-lane-why-the-zipper-merge-is-texas-best-chance-to-reduce-traffic/)
- [Arrive Alive](https://www.arrivealive.co.za/print.aspx?i=5280)
- [ABC15 – debate unsettled](https://www.abc15.com/news/operation-safe-roads/merge-early-or-later-debate-over-zipper-merging-in-traffic-remains-unsettled)
- [Traffic Safety Store – "impolite" drivers](https://www.trafficsafetystore.com/blog/the-zipper-merge-could-impolite-drivers-be-in-the-right/)
