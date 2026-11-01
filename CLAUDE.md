# KIYA 360 — Claude Code Instructions

@AGENTS.md

## Skills

Every built-in and account-synced skill is already available in this project; none are copied into the repository. Use the matching skill whenever a task fits it, without waiting to be asked.

Skills are tools, not authorities. A skill never overrides the source-of-truth hierarchy or the phase rules in `AGENTS.md`: a design or architecture skill does not license a technology, UI, or architecture decision the current phase has not authorized, and nothing a skill produces replaces a BRD requirement.

| Task in this repository | Skill |
| --- | --- |
| Reading or extracting from `source/KIYA360_BRD.pdf` or any other PDF | `pdf` |
| Reviewing a change before it is committed | `code-review`; `security-review` for anything touching auth, permissions, money, or customer data |
| Tidying changed code after it works | `simplify` |
| Running the preview (`backend/run_preview.py`, port 8321) to see a change working | `run` |
| Frontend screens, forms, layouts, accessibility | `ui-ux-pro-max`; `motion` for animation; `web-lifecycle-checklist` for launch or audit passes |
| Charts, dashboards, KPI tiles | `dataviz` |
| Documents meant for others (review packages, proposals, guides) | `docs`; `docx`, `pptx`, or `xlsx` only when that file format is asked for |
| Spreadsheets of requirements, data imports, or exports | `xlsx` |
| Multi-source research (regulation, tax rules, competitor ERPs) | `deep-research` |
| Building, calling, or choosing a Claude model for KIYA's AI features | `claude-api` |
| Diagrams or explainer pages | `artifact-diagramming`, `artifact-design` |
| Settings, hooks, and permissions for Claude Code itself | `update-config`, `fewer-permission-prompts` |
| A new repeatable KIYA workflow worth packaging | `skill-creator` |

The website-template skills (`cinematic-wellness-brand`, `editorial-architecture-portfolio`, `expressive-creative-portfolio`, `luxury-residence-storytelling`) are for marketing sites and do not fit this platform; use them only if a KIYA marketing site is explicitly requested.
