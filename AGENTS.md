# KIYA 360 — Universal Agent Instructions

These instructions apply to Codex, Cursor, Antigravity, and other compatible agents working in this repository.

## Project Identity

KIYA 360 is a unified CRM + ERP business platform defined by the current 28-module Business Requirements Document (BRD). The repository, not any agent's internal memory, is the shared project record.

## Source-of-Truth Hierarchy

1. Current approved BRD: `source/KIYA360_BRD.pdf`
2. Approved requirements documentation under `docs/00-requirements/`
3. Approved project decisions in `.kiya/AI-DECISIONS.md`
4. Current-state snapshot: `docs/PROJECT-STATE.md`
5. Current phase specifications and handoff: `.kiya/AI-HANDOFF.md`
6. Implementation/code, when an authorized phase creates it
7. Agent suggestions

An agent suggestion must never silently override an authoritative requirement or decision.

## Required Working Discipline

- Inspect relevant repository files before changing anything.
- Start with the progressive context-loading order in `.kiya/AI-CONTEXT.md`; do not blindly read the entire repository.
- Never invent missing business requirements. Record missing material detail as TBD and link/raise an open question where appropriate.
- Use the established classifications exactly: BRD-REQUIRED, BRD-DERIVED, PROPOSED, TBD, OUT-OF-SCOPE.
- Do not classify unspecified functionality as OUT-OF-SCOPE.
- Do not make technology, architecture, database, API, UI, infrastructure, or AI-model decisions unless the current authorized phase explicitly permits them.
- Preserve traceability from any future work to approved requirements.
- Before adding a shared entity, workflow, dependency, or decision, check the existing shared-foundation, dependency, requirements, and decision records for consistency.
- Do not rewrite, delete, or reverse approved decisions or baseline requirements without explicit authorization and a recorded change decision.
- Validate completed work in proportion to its risk and report the evidence.
- After a meaningful task, update the relevant state, handoff, decision, and/or changelog record so another agent can safely continue.

## Cross-Agent Handoff

When taking over this repository: open the same workspace; read this file; read `docs/PROJECT-STATE.md`; read `.kiya/AI-HANDOFF.md` and relevant decisions; inspect actual files before editing; continue from the recorded state rather than restarting; and update the repository handoff/state when finished. Never assume another agent shares your internal memory.
