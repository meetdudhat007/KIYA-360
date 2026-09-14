# KIYA 360 — AI Handoff

## Current Phase

Phase 1 — Platform Architecture & System Design (Phase 1 Complete — Sealed Baseline)

## Current Status

PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2

## Current Objective

Handoff to Phase 2: Execute empirical technical Proofs-of-Concept (`PoC-01` through `PoC-04`), commission external corporate technology IP legal review for Frappe MIT vs ERPNext GPLv3 SaaS isolation (`Gate L-01`), execute Stakeholder Decision Gates `STK-01` through `STK-04` for open questions `OQ-003` through `OQ-015`, and begin detailed component design.

## Source of Truth

`source/KIYA360_BRD.pdf` — KIYA 360 BRD v2.0, prepared 13 September 2026. Follow the hierarchy in `AGENTS.md`.

## Completed Work

- Phase 0A: 28 modules, 238 functional-requirement records, scope/flows/NFRs/AI/common capabilities, 15 open questions, and formal review.
- Phase 0B-0: detailed-requirements strategy, template, and status legend.
- Phase 0B-1A: 15 shared-foundation records and 11 critical/high explicit dependency records.
- Phase 0B-1A.5: multi-agent continuity system created.
- Phase 0B-1B: analyzed all 15 open questions; created priority, blocking, grouping, stakeholder-type, flow/foundation/dependency, and clarification-session planning.
- Phase 0B-1C: created the `CD-###` lifecycle/register/template, approval and requirement-change gates, conflict/partial/deferred/supersession handling, and integrations with traceability, detailed-requirements governance, and session planning.
- Phase 0B-1D:
  - Document 21: Reverse-engineered ERPNext develop tree (v17.0.0-dev) workflows, doc lifecycles, and structural inventory.
  - Document 22: Mapped KIYA Customer-to-Cash, Procure-to-Pay, Asset-to-Service, and supporting flows against ERPNext reference mechanics.
  - Document 23: Mapped 50 domain entities across KIYA and ERPNext/Frappe; identified collisions, composite mappings, and missing concepts.
  - Document 24: Executed rigorous 28-module gap analysis detailing technical boundaries, consequences, and KIYA-owned build needs.
  - Document 25: Defined tactical reuse vs build boundaries across 30 capability areas; isolated 8 mandatory KIYA-owned seams and GPLv3 licensing constraints.
  - Document 26: Compiled an engineering reference catalog of 12 production transactional workflows with stock/accounting effects and cancellations.
  - Document 27: Completed formal quality-control review establishing status PASS WITH CORRECTIONS.
  - Document 28: Prepared Critical Clarification Group CG-01 stakeholder package.
  - Documents 29 & 30: Captured and formalized approved stakeholder decisions `CD-001` (scope expansion hybrid model) and `CD-002` (business status lifecycle model).
  - Document 31: Authored Phase 0B-2 Batch 1 Customer-to-Cash (C2C) detailed requirements expansion across all 18 stages (`DR-C2C-001` to `DR-C2C-018`) and completed strict quality-control anti-hallucination correction pass ensuring proper governance classifications (`BRD-REQUIRED`, `BRD-DERIVED`, `ERP-REFERENCE`, `PROPOSED`, `TBD`).
  - Document 32: Authored Phase 0B-2 Batch 2 Procure-to-Pay (P2P) detailed requirements expansion across all 12 stages (`DR-P2P-001` to `DR-P2P-012`), completed targeted quality-control correction pass neutralizing legal language and calibrating policies, and finalized targeted classification cleanup strictly separating confirmed BRD requirements (RFQ/RFP capabilities, physical warehouse/location/bin tracking) from proposed candidate mechanics/differentiators (multi-envelope RFP bidding, directed putaway, automated bin selection, barcode scanning), neutralizing liability wording, and aligning summary matrices across all 12 stages.
  - Document 33: Authored Phase 0B-2 Batch 3 Asset-to-Service (A2S) detailed requirements expansion across all 11 stages (`DR-A2S-001` to `DR-A2S-011`), establishing the Customer Installed Base vs Corporate Fixed Asset distinction, resolving the Field Service Work Order vs Discrete Manufacturing Work Order collision, integrating dynamic warranty entitlement with unified invoicing and tax engines, and connecting mobile spare parts truck stock without unsupported policy inventions.
  - Document 34: Authored Phase 0B-2 Shared Foundation Requirements Baseline (`34-shared-foundation-requirements-baseline.md`) covering all 15 platform foundations (`SF-001` through `SF-015`) mapped in `13-shared-foundation-requirements-map.md`. Enforces `CD-001` hybrid model, `CD-002` operational business status model, and `DEC-007` unified master data. Rigorously preserved technology neutrality (no database engines, queues, or frameworks selected), maintained open questions `OQ-003` through `OQ-015` as `TBD`, and verified full operational cross-flow support across C2C, P2P, and A2S.
  - Document 35: Authored Phase 0B-2 Compressed Remaining Module Requirements Baseline (`35-remaining-module-baselines.md`) covering Marketing, Customer Service, Supplier Management, Logistics, Projects, HR & Payroll, E-Commerce, and back-office Finance/Assets/Inventory/Mfg/Tax capabilities. Reconciled all 238 BRD functional requirements across 28 modules.
  - Document 36: Conducted the Final Phase 0 Requirements Traceability & Quality-Control Gate (`36-phase-0-completion-assessment.md`). Verified 100% coverage of all 28 modules and 238 BRD requirements, audited dependencies DEP-001..DEP-011 and foundations SF-001..SF-015, verified CD-001/CD-002 adherence, resolved the FR-AST-001..007 citation ambiguity with a minimal documentation correction in Document 35, calibrated DEP-005 to accurately distinguish sales dispatch and goods receipt receiving basis for supplier invoice matching, preserved technology neutrality and OQ-003..OQ-015 open status, and formally issued verdict PASS WITH CORRECTIONS.
- Phase 1A: Authored and approved Phase 1A Architecture Strategy, Principles & Decision Framework (`docs/02-architecture/01-architecture-strategy-and-decision-framework.md`), establishing 22 core architecture principles, quality-attribute governance (with unquantified NFRs linked to `OQ-015`), strict separation of Customer Installed Base vs Corporate Fixed Assets, explicit boundary enforcement for the 8 KIYA-owned strategic seams, 5 candidate architecture archetypes, 22 evaluation dimensions, and PoC / legal validation gates prior to platform selection. Completed targeted governance corrections to neutralize implementation mechanisms, calibrate licensing language, frame tenancy models as evaluation options, and adjust 1B entry criteria.
- Phase 1B: Authored and approved Phase 1B Candidate Architecture Evaluation & Trade-off Analysis (`docs/02-architecture/02-candidate-architecture-evaluation.md`, `docs/02-architecture/03-architecture-decision-readiness.md`, and `docs/02-architecture/adrs/ADR-001-provisional-platform-architecture.md`). Evaluated Candidates A through E across all 22 architecture dimensions; determined Candidate B (ERPNext-primary monolith) is materially mismatched with requirements due to `CD-002` conflict, 40%+ BRD gaps, and GPLv3 copyleft questions; determined Candidate E (Headless Microservices) is poorly suited for core transactional ERP due to distributed transaction/ledger consistency complexities; established Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation) as PROVISIONAL ARCHITECTURE RECOMMENDATION with Candidate D (Frappe + Mostly Custom KIYA Apps) as evaluated architectural fallback; established 4 mandatory empirical PoC gates (`PoC-01` to `PoC-04`) and mandatory Gate L-01 legal licensing review; recorded ADR-001 with status `PROPOSED / CONDITIONAL`.
- Phase 1C: Authored and approved Phase 1C Target Architecture Definition (`docs/02-architecture/04-target-architecture.md`), detailing the 14 conceptual layers, unified platform model, C2C/P2P/A2S cross-module flow architectures, master data architecture, operational business status model (`CD-002`), financial integrity boundary (`DEC-009`), Tax & Statutory Compliance architecture (`MOD-18` / Seam #8), shared workflows/notifications/DMS, tenancy evaluation, AI/BI boundaries, and mobile offline synchronization architecture.
- Phase 1D: Authored and approved Phase 1D Application, API & Integration Architecture (`docs/02-architecture/05-application-api-integration-architecture.md`), mapping all 28 BRD modules across 6 logical domain clusters, establishing the 28-Module Ownership Matrix, the API & Integration Responsibility Matrix, the 14-entity Master Data Ownership Matrix, the cross-module dependency graph, and the event/transaction propagation architecture.
- Phase 1E: Authored and approved Phase 1E Deployment & Operations Architecture (`docs/02-architecture/06-deployment-operations-architecture.md`), establishing four conceptual environments (DEV, TEST, STAGE, PROD), compute zoning and runtime topology, database-per-tenant isolation model, background task and distributed scheduler architecture, resilience and DR models, structured observability, and framework anti-corruption insulation seams.
- Phase 1 Governance: Authored Architecture Decision Register (`07`), Validation & PoC Register (`08`), Risk Register (`09`), Traceability & Complete Coverage Audit (`10`), and Final Architecture Completion Assessment (`11`). Formally issued verdict: PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2.

## Work In Progress

None.

## Files Created (Phase 1 Architecture Suite)

- `docs/02-architecture/01-architecture-strategy-and-decision-framework.md`
- `docs/02-architecture/02-candidate-architecture-evaluation.md`
- `docs/02-architecture/03-architecture-decision-readiness.md`
- `docs/02-architecture/04-target-architecture.md`
- `docs/02-architecture/05-application-api-integration-architecture.md`
- `docs/02-architecture/06-deployment-operations-architecture.md`
- `docs/02-architecture/07-phase-1-architecture-decision-register.md`
- `docs/02-architecture/08-phase-1-validation-and-poc-register.md`
- `docs/02-architecture/09-phase-1-architecture-risk-register.md`
- `docs/02-architecture/10-phase-1-traceability-and-coverage.md`
- `docs/02-architecture/11-phase-1-completion-assessment.md`
- `docs/02-architecture/adrs/ADR-001-provisional-platform-architecture.md`

## Files Modified

- `docs/PROJECT-STATE.md`
- `.kiya/AI-DECISIONS.md`
- `.kiya/AI-HANDOFF.md`
- `.kiya/AI-CHANGELOG.md`

## Important Findings

- Candidate B (ERPNext Primary Monolith) is materially mismatched with requirements due to `CD-002` conflict (hardcoded binary `docstatus`), 40%+ BRD gaps, and GPLv3 copyleft exposure across proprietary KIYA IP.
- Candidate E (Headless Microservices) is poorly suited for core transactional ledger/inventory due to substantial distributed transaction consistency complexities (sagas/2PC).
- Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation) is provisionally recommended for offering potential delivery acceleration and rock-solid ledger math while isolating proprietary IP into custom apps.
- Candidate D (Frappe Framework + Clean-Room Custom KIYA Apps) is the evaluated fallback if GPLv3 reuse fails legal review.
- Four empirical PoCs (`PoC-01` SaaS plane, `PoC-02` India tax, `PoC-03` concurrency benchmark, `PoC-04` mobile offline sync) and one legal review (`Gate L-01`) are mandatory prerequisites for final approval.
- 100% complete unbroken traceability is established across all 28 modules, 238 functional requirements, 15 shared foundations, 11 critical dependencies, and 8 strategic seams.

## Important Decisions

- `DEC-012` / `CD-001`: Approved hybrid scope-expansion approach for Phase 0B-2.
- `DEC-013` / `CD-002`: Approved operational business status lifecycle model.
- `ADR-001` (`DEC-014`): Formally adopted Candidate C (Frappe Framework + Selective ERPNext Core Reuse Under Evaluation) as PROVISIONAL ARCHITECTURE RECOMMENDATION with Candidate D (Frappe Framework + Mostly Custom KIYA Apps) as evaluated fallback / contingency option; status is `PROPOSED / CONDITIONAL` pending successful clearance of `PoC-01`..`PoC-04` and Gate L-01 legal licensing review.
- `ADR-002` (`DEC-015`): Authoritative Single-Source Master Data Registry Model (`PROPOSED`).
- `ADR-003` (`DEC-016`): Decoupled Operational Business Status Lifecycle Architecture (`PROPOSED`).
- `ADR-004` (`DEC-017`): Anti-Corruption Framework Insulation & Strategic Seams (`PROPOSED`).
- `ADR-005` (`DEC-018`): Multi-Tenant Operational Isolation Topology (`PROVISIONAL`).
- `ADR-006` (`DEC-019`): Asynchronous Decoupling of Intelligence, Analytics & Background Workloads (`PROPOSED`).

## Open Questions

- `OQ-001` and `OQ-002` are **APPROVED / FORMALLY RESOLVED** via `CD-001` and `CD-002`.
- Questions `OQ-003` through `OQ-015` remain **OPEN / TBD** in `docs/00-requirements/06-open-questions.md`, governed by Stakeholder Gates `STK-01` through `STK-04` and technical PoCs in `ARCH-08`.

## Known TBDs

- Technical PoC execution harnesses for `PoC-01` through `PoC-04`.
- Legal licensing opinion from qualified counsel for `Gate L-01`.
- Formal non-functional performance and sizing targets (`OQ-015` / `STK-04`).

## Known Risks

- Reusing ERPNext core modules (Candidate C) creates potential GPLv3 copyleft contamination of proprietary KIYA IP if architectural and legal isolation boundaries fail (`RSK-03`). Mitigated by `Gate L-01` and Candidate D fallback.
- Upstream Frappe/ERPNext `docstatus` engine enforces binary submission, requiring an explicit state-machine adapter layer to support KIYA's 8-state operational `business_status` (`RSK-02`).
- India statutory tax engine changes and NIC portal updates (`RSK-04`). Mitigated by pluggable tax adapter and `PoC-02`.
- Mobile offline synchronization and state collisions in intermittent connectivity (`RSK-05`). Mitigated by client-generated UUIDs, outbox sync, and `PoC-04`.

## Do Not Change

- Do not alter the BRD source document.
- Do not introduce implementation, production code, database DDL, concrete API endpoints, or UI designs into architecture documents.
- Do not classify unspecified functionality as OUT-OF-SCOPE.
- Do not assume agent memory is shared; use the repository context system and inspect actual files before changing them.
- Do not mark platform architecture as final approved without satisfying all PoC and legal gates in ADR-001.

## Next Exact Action

**Phase 2 — Technical PoC Validation, Component Architecture & Detailed Design:**
1. Execute `PoC-01` (SaaS Control Plane & Multi-Tenant Data Isolation).
2. Execute `PoC-02` (India Statutory Tax & NIC E-Invoicing Integration).
3. Execute `PoC-03` (High-Concurrency Transaction & Read-Replica Load Benchmark).
4. Execute `PoC-04` (Mobile Offline Synchronization & Conflict Resolution).
5. Obtain corporate legal licensing opinion on Frappe MIT vs ERPNext GPLv3 (`Gate L-01`).
6. Conduct Stakeholder Clarification Sessions for `STK-01` through `STK-04` (`OQ-003` to `OQ-015`).

## Required Validation

Before starting Phase 2 tasks: read `AGENTS.md`, `docs/PROJECT-STATE.md`, this handoff record, `.kiya/AI-DECISIONS.md`, and `docs/02-architecture/01-architecture-strategy-and-decision-framework.md` through `11-phase-1-completion-assessment.md`. Confirm BRD v2.0 remains the primary business authority, Phase 1 architecture is sealed with controlled open items, ADR-001 is recorded as PROPOSED/CONDITIONAL, the 8 strategic seams are enforced, open questions OQ-003 through OQ-015 remain open, and no production code or database schemas have been created.

## Last Updated

14 September 2026 — Phase 1 Final Identifier Conformance Audit PASSED. Critical correction: DEP-006 through DEP-011 in `docs/02-architecture/10-phase-1-traceability-and-coverage.md` restored to their exact Phase 0 authoritative meanings (Procurement → Supplier Management, Asset Management → Maintenance & Field Service, Projects → Finance, All → BI/EPM, All → Workflow & Approvals, All → Audit/Security/Compliance). DEP-001 corrected to CRM → Sales only (no MOD-05). OQ-005 mislabel in ADR-005 corrected. FR prefixes aligned (FR-CSVC, FR-WH). All 11 DEP IDs, 28 MOD IDs, 15 SF IDs, 15 OQ IDs, 6 ADR IDs, 4 PoC IDs, 4 STK IDs, and 2 CD IDs verified conformant. Formal gate verdict confirmed: PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2.

