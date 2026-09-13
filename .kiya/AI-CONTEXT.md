# KIYA 360 — AI Context

## Identity and Source

KIYA 360 is a unified CRM + ERP platform. The current source of truth is `source/KIYA360_BRD.pdf`, **version 2.0**, prepared **13 September 2026**. It supersedes the earlier 12-module BRD; no older BRD is present in this repository.

## Scope at a Glance

The BRD defines 28 modules: Platform & Administration; CRM; Sales; Marketing; Customer Service; Procurement; Supplier Management; Inventory; Warehouse; Manufacturing; MRP & Planning; Quality; Asset Management; Maintenance & Field Service; Logistics & Transportation; Projects; Finance & Accounting; Tax & Statutory Compliance; HR & Payroll; E-Commerce; Document Management; Business Intelligence; EPM / Budget / Forecast; Workflow & Approvals; AI & Automation; Integration & API; Mobile Application; Audit, Security & Compliance.

Core BRD flows are Customer-to-Cash, Procure-to-Pay, and Asset-to-Service. Shared platform capabilities include enterprise context, master data/unified data model, access/security, workflow/approvals, notifications, documents, audit, mobile/offline synchronization, AI/automation, BI/EPM, integration, numbering, and common platform actions. Global capabilities include multi-company/country/currency/language, real-time insights, security, scalability, and 24/7 operations.

AI scope is limited to BRD-level AI Insights, Predictive Analytics, Process Automation/RPA, AI Chat Assistant, Anomaly Detection, and Machine Learning Models. No model, provider, algorithm, or architecture is selected.

## Current State

Current phase: **Phase 0B-1C — Clarification Decision & Approval Framework**. Phases 0A, 0B-0, 0B-1A, 0B-1A.5, 0B-1B, and 0B-1C are complete. The next action is stakeholder clarification and controlled decision approval, beginning with CG-01; detailed requirements expansion remains blocked until applicable decisions are approved.

The project is requirements-first, evidence-based, traceable, cross-module aware, technology-neutral, and explicit about uncertainty. No application implementation exists.

## Non-Negotiable Rules

- BRD v2.0 and approved documentation outrank suggestions and conventions.
- Never invent business rules, fields, statuses, approvals, tax/payroll rules, notifications, integrations, APIs, UI, data design, technologies, or AI design.
- Mark uncertainty TBD; use BRD-DERIVED only for a necessary, explained consequence of explicit BRD evidence.
- Do not modify the BRD or silently alter approved baselines/decisions.

## Documentation Map

- `docs/PROJECT-STATE.md`: authoritative current-state snapshot.
- `docs/00-requirements/01`–`09`: Phase 0A baseline and review.
- `docs/00-requirements/10`–`12`: detailed-requirements governance, template, and status legend.
- `docs/00-requirements/13`–`14`: shared-foundation and critical-dependency maps.
- `docs/00-requirements/15`: critical clarification plan and session template.
- `docs/00-requirements/16`–`17`: clarification-decision approval framework, initial register, and reusable decision template.
- `docs/00-requirements/18`–`20`: assessment-only ERPNext/Frappe feasibility report, fit matrix, and PoC plan; no platform selection.
- `.kiya/AI-DECISIONS.md`: decision register.
- `.kiya/AI-HANDOFF.md`: current task continuation record.
- `.kiya/AI-CHANGELOG.md`: concise project history.

## Source Hierarchy and Reading Order

Use the hierarchy in `AGENTS.md`. For a new task, load progressively:

1. `AGENTS.md`
2. `docs/PROJECT-STATE.md`
3. `.kiya/AI-CONTEXT.md`
4. `.kiya/AI-DECISIONS.md`
5. `.kiya/AI-HANDOFF.md`
6. Current phase documentation
7. Relevant requirement documents
8. Source code, if any and relevant
9. Relevant BRD sections

Do not read the entire repository by default; load only what the task needs.

## Git Compatibility

Git is not initialized in this workspace. Do not initialize, commit, or tag unless explicitly instructed. If Git is later used, suggested milestone names are `phase-0a-complete`, `phase-0b-0-complete`, `phase-0b-1a-complete`, and `phase-0b-1a5-complete`; these are recommendations only, not existing tags.
