# Zipper Merge Lab

An interactive, illustrative microsimulation of a 2→1 work-zone lane closure. Four
panels run side by side on the same stream of drivers:

- freeway zipper;
- freeway conventional (early) merge;
- urban zipper;
- urban conventional merge.

Sliders control:

- the driver mix (a bell curve from defensive to aggressive);
- how many drivers follow the zipper signs;
- demand;
- speed, which also sets the OTM Book 7 taper;
- heavy-vehicle share.

Live metrics show queue, throughput, delay and forced merges.

It is a fun demo of mechanism and direction, **not** a calibrated model. The page
explains its method, parameters and limits in full.

## Use it

- **Open:** double-click `zipper-merge-lab.html`, or run `make serve` and open
  <http://127.0.0.1:8000/zipper-merge-lab.html>.
- **Share:** send the single HTML file. It needs an internet connection only for
  Google Fonts.

## Repository layout

| Path | Contents |
|---|---|
| `zipper-merge-lab.html` | The simulation page: model, controls, method text |
| `docs/research.md` | Impartial evidence review on zipper vs. early merge |
| `docs/model-log.md` | Dated build and revision history of the model |
| `llm-wiki/` | Agent-maintained continuity: current state, decisions, open questions |
| `AGENTS.md` | Instructions and routing for coding agents |
| `scripts/check_repo_context.py` | Context and page-script validation |

## Validate

```sh
make test
```

This checks the agent-context structure. It also checks that the page's script
parses, when Node.js is installed.

## Model in brief

- **Car-following and lane changes:** the Intelligent Driver Model (IDM) and MOBIL,
  with cooperative and forced merging.
- **Driver behaviour:** one assertiveness trait per driver sets all of their
  parameters.
- **Vehicles:** cars, single-unit trucks and tractor-semitrailers, drawn to scale.
- **Capacity:** tuned to HCM-style queue-discharge targets.

Current results and caveats are summarized in
[`llm-wiki/project-state.md`](llm-wiki/project-state.md).
