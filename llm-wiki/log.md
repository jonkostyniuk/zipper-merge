# Maintenance log

## 2026-10-20

- Added the MIT licence and the not-engineering-advice disclaimer (page footer
  and README). Routed the owner's agent-setup guidelines reference copy
  (`docs/agents-setup-guidelines-2026-10-20v1.1.md`, CC BY 4.0). The context check now ignores links
  inside fenced code blocks.
- Established the model-neutral context architecture:
  - root `AGENTS.md` router;
  - lean OKF v0.2 bundle (state, decisions, open questions);
  - deterministic context validation via `make test`.
- Split the former `FINDINGS.md` into `docs/research.md` and `docs/model-log.md`,
  keeping the original section numbers. Moved its "Current state" summary into
  `project-state.md`.
