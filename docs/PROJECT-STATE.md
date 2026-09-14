# KIYA 360 — PROJECT STATE

## Current Phase

Phase 1 — Platform Architecture & System Design (Phase 1 Complete — Sealed Baseline)

## Status

PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2

## Current Source of Truth

`source/KIYA360_BRD.pdf` — KIYA 360 Business Requirements Document, version 2.0, prepared 13 September 2026.

## Completed

- Read and preserved the authoritative BRD.
- Catalogued all 28 BRD modules and 238 functional-requirement records.
- Documented scope, exclusions, flows, dependencies, conceptual data concepts, AI, NFRs, common features, assumptions, glossary, traceability, and open questions.
- Performed a formal Phase 0A review and corrected an unsupported Customer Service-to-flow mapping.
- Established the Phase 0B detailed-requirements strategy, canonical template, and status legend without expanding requirements.
- Mapped 15 shared-foundation capabilities and 11 critical/high BRD dependency records without expanding detailed requirements.
- Established a repository-based multi-agent continuity system for shared context, decisions, handoff, and changelog history.
- Analyzed and planned clarification for all 15 existing open questions without resolving them or expanding detailed requirements.
- Established the clarification-decision lifecycle, status controls, approval/evidence gates, change control, and AI-agent restrictions.
- Completed an assessment-only ERPNext/Frappe feasibility study, fit matrix, and PoC plan without selecting a technology, approving architecture, or changing requirements.
- Reverse-engineered ERPNext reference repository workflows and structural inventory (`21-erpnext-workflow-reverse-engineering.md`).
- Established comprehensive alignment between KIYA core business flows (C2C, P2P, A2S) and ERPNext (`22-erpnext-kiya-workflow-alignment-matrix.md`).
- Completed cross-module domain mapping covering 50 business entities, identifying exact equivalents, collisions, framework concepts, and missing entities (`23-erpnext-kiya-domain-mapping.md`).
- Executed rigorous 28-module gap analysis identifying ERPNext vs Frappe vs KIYA boundaries (`24-erpnext-kiya-gap-analysis.md`).
- Defined reuse vs build strategic boundaries across 30 capability areas and established 8 mandatory KIYA-owned seams (`25-erpnext-reuse-vs-build-boundary.md`).
- Cataloged 12 production transactional workflows detailing lifecycles, stock/accounting effects, and cancellation handling (`26-erpnext-workflow-reference-catalog.md`).
- Conducted formal quality-control analysis review resulting in PASS WITH CORRECTIONS (`27-erpnext-analysis-review.md`).
- Prepared Critical Clarification Group CG-01 stakeholder package for OQ-001 and OQ-002 (`28-cg01-stakeholder-clarification-package.md`).
- Formally processed and recorded approved stakeholder decisions for CG-01:
  - `CD-001` (OQ-001): Hybrid scope-expansion approach detailing core flows (C2C, P2P, A2S) and using traceable ERP-standard baselines for standard non-specified features (`29-cd001-scope-expansion-hybrid-model.md`).
  - `CD-002` (OQ-002): Operational Business Status model representing operational milestones, explicitly rejecting ERPNext's technical dual `docstatus` model (`30-cd002-transactional-lifecycle-business-status.md`).
- Authored and completed strict quality-control anti-hallucination correction pass on Phase 0B-2 Batch 1: Customer-to-Cash (C2C) Detailed Requirements Expansion covering all 18 stages from Lead to Customer History (`DR-C2C-001` through `DR-C2C-018` in `31-customer-to-cash-detailed-requirements.md`), rigorously classifying `BRD-REQUIRED`, `BRD-DERIVED`, `ERP-REFERENCE`, `PROPOSED`, and `TBD` elements, and ensuring exact status enumerations and automated QI-rejection-to-NCR mappings are treated as candidate/proposed rather than rigid confirmed baselines.
- Authored and completed targeted quality-control anti-hallucination correction pass on Phase 0B-2 Batch 2: Procure-to-Pay (P2P) Detailed Requirements Expansion covering all 12 stages from Supplier Master to Supplier Performance (`DR-P2P-001` through `DR-P2P-012` in `32-procure-to-pay-detailed-requirements.md`) under `CD-001` hybrid model and `CD-002` operational business status model, rigorously neutralizing legal wording, calibrating tax statutory treatments and 3-way matching tolerances, setting policy controls to proposed/TBD, and auditing all acceptance criteria against hidden assumptions.
- Completed final classification cleanup pass on `32-procure-to-pay-detailed-requirements.md` strictly separating confirmed BRD requirements (RFQ capability, RFP capability, physical warehouse/location/bin coordinate tracking) from candidate mechanics and differentiators (multi-envelope technical-vs-commercial RFP evaluation, directed putaway optimization, automated bin selection, and barcode scanning mechanics as `PROPOSED / Reference Baseline`), removing legal terminology from AP liability settlements, and aligning summary matrices and differentiator overviews across all 12 stages.
- Authored Phase 0B-2 Batch 3: Asset-to-Service (A2S) Detailed Requirements Expansion covering all 11 stages from Asset/Machine (Installed Base) through Asset History (`DR-A2S-001` through `DR-A2S-011` in `33-asset-to-service-detailed-requirements.md`) under `CD-001` hybrid model and `CD-002` operational business status model, rigorously enforcing the architectural distinction between Customer Installed Base and Corporate Capital Assets, preventing Work Order schema collisions between Field Service and Discrete Manufacturing, integrating dynamic warranty entitlement with unified invoicing and tax engines, and linking spare parts truck-stock execution directly to mobile field technicians without inventing unsupported SLAs, pricing rules, or dispatch algorithms.
- Authored Phase 0B-2 Shared Foundation Requirements Baseline covering all 15 platform foundations (`SF-001` through `SF-015` in `34-shared-foundation-requirements-baseline.md`) under `CD-001` hybrid model, `CD-002` operational business status model, and `DEC-007` unified master data. Rigorously preserved technology neutrality (no database engines, queues, or frameworks selected), classified all statements according to approved discipline, maintained open questions `OQ-003` through `OQ-015` as `TBD`, and verified full operational support for C2C, P2P, and A2S core business flows.
- Authored Phase 0B-2 Compressed Remaining Module Requirements Baseline (`35-remaining-module-baselines.md`) covering Marketing, Customer Service, Supplier Management, Logistics, Projects, HR & Payroll, E-Commerce, and back-office Finance/Assets/Inventory/Mfg/Tax capabilities. Completed comprehensive 238-Requirement Coverage Reconciliation accounting for every single BRD functional requirement across all 28 modules without gaps or contradictions.
- Conducted and completed the formal Phase 0 Final Requirements Traceability & Quality-Control Gate (`36-phase-0-completion-assessment.md`), auditing all 28 BRD modules, all 238 functional requirements, core flows, shared foundations, dependencies (`DEP-001`..`011`), and governance decisions. Applied minimal documentation calibrations resolving the Asset requirement citation (`FR-AST-001`..`007` in Document 35) and refining `DEP-005` in Document 36 to accurately distinguish sales dispatches from goods receipt receiving basis for supplier invoice matching. Verified zero requirement contradictions, confirmed technology neutrality, verified preservation of `OQ-003`..`OQ-015`, and granted final quality-control sign-off.
- Authored and approved Phase 1A Architecture Strategy, Principles & Decision Framework (`docs/02-architecture/01-architecture-strategy-and-decision-framework.md`), establishing 22 core architecture principles, quality-attribute governance (with unquantified NFRs linked to `OQ-015`), strict separation of Customer Installed Base vs Corporate Fixed Assets, explicit boundary enforcement for the 8 KIYA-owned strategic seams, 5 candidate architecture archetypes, 22 evaluation dimensions, and PoC / legal validation gates prior to platform selection. Completed targeted governance corrections to neutralize implementation mechanisms, calibrate licensing language, frame tenancy models as evaluation options, and adjust 1B entry criteria.
- Authored and completed Phase 1B Candidate Architecture Evaluation & Trade-off Analysis (`docs/02-architecture/02-candidate-architecture-evaluation.md`, `docs/02-architecture/03-architecture-decision-readiness.md`, and `docs/02-architecture/adrs/ADR-001-provisional-platform-architecture.md`). Evaluated Candidates A through E across all 22 architecture dimensions; determined Candidate B (ERPNext-primary monolith) is materially mismatched with requirements due to `CD-002` conflict, 40%+ BRD gaps, and GPLv3 copyleft questions; determined Candidate E (Headless Microservices) is poorly suited for core transactional ERP due to distributed transaction/ledger consistency complexities; established Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation) as PROVISIONAL ARCHITECTURE RECOMMENDATION with Candidate D (Frappe + Mostly Custom KIYA Apps) as evaluated architectural fallback; established 4 mandatory empirical PoC gates (`PoC-01` to `PoC-04`) and mandatory Gate L-01 legal licensing review; recorded ADR-001 with status `PROPOSED / CONDITIONAL`.
- Authored and completed Phase 1C Target Architecture Definition (`docs/02-architecture/04-target-architecture.md`), defining the 14 conceptual layers, unified platform model, C2C/P2P/A2S cross-module flow architectures, master data architecture, operational business status model (`CD-002`), financial integrity boundary (`DEC-009`), Tax & Statutory Compliance architecture (`MOD-18` / Seam #8), shared workflows/notifications/DMS, tenancy evaluation, AI/BI boundaries, and mobile offline synchronization architecture.
- Authored and completed Phase 1D Application, API & Integration Architecture (`docs/02-architecture/05-application-api-integration-architecture.md`), mapping all 28 BRD modules across 6 logical domain clusters (`MOD-01` to `MOD-28`), establishing the 28-Module Ownership Matrix, the API & Integration Responsibility Matrix, the 14-entity Master Data Ownership Matrix, the cross-module dependency graph, and the event/transaction propagation architecture.
- Authored and completed Phase 1E Deployment & Operations Architecture (`docs/02-architecture/06-deployment-operations-architecture.md`), establishing the four conceptual environments (DEV, TEST, STAGE, PROD), compute zoning and runtime topology, provisional database-per-tenant isolation model, background task and distributed scheduler architecture, resilience and DR models, structured observability, and framework anti-corruption insulation seams.
- Authored Phase 1 Architecture Decision Register (`docs/02-architecture/07-phase-1-architecture-decision-register.md`), consolidating ADR-001 through ADR-006 with confidence ratings and validation gates.
- Authored Phase 1 Validation & PoC Register (`docs/02-architecture/08-phase-1-validation-and-poc-register.md`), defining capability-based criteria for PoC-01 through PoC-04, Legal Gate L-01, and Stakeholder Gates STK-01 through STK-04.
- Authored Phase 1 Architecture Risk Register (`docs/02-architecture/09-phase-1-architecture-risk-register.md`), classifying 14 core technical, legal, and operational risks with mitigations and ownership.
- Authored Phase 1 Traceability & Complete Coverage Audit (`docs/02-architecture/10-phase-1-traceability-and-coverage.md`), certifying 100% complete unbroken traceability across all 28 modules, 238 functional requirements, 15 shared foundations, 11 dependencies, and 8 strategic seams.
- Authored and completed Phase 1 Final Architecture Completion Assessment (`docs/02-architecture/11-phase-1-completion-assessment.md`), auditing Questions A through N, anti-patterns, single source of truth, and issuing the formal gate verdict: PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2.
- Compiled, audited, and sealed the self-contained external architecture review dossier: `docs/PHASE-1-COMPLETE-REVIEW-PACKAGE.md`.

## Documents

- `docs/00-requirements/01-master-requirements.md`
- `docs/00-requirements/02-module-inventory.md`
- `docs/00-requirements/03-scope-boundaries.md`
- `docs/00-requirements/04-business-flows.md`
- `docs/00-requirements/05-requirement-traceability.md`
- `docs/00-requirements/06-open-questions.md`
- `docs/00-requirements/07-glossary.md`
- `docs/00-requirements/08-assumptions.md`
- `docs/00-requirements/09-phase-0a-review.md`
- `docs/00-requirements/10-detailed-requirements-strategy.md`
- `docs/00-requirements/11-detailed-requirement-template.md`
- `docs/00-requirements/12-requirement-status-legend.md`
- `docs/00-requirements/13-shared-foundation-requirements-map.md`
- `docs/00-requirements/14-critical-requirement-dependencies.md`
- `AGENTS.md`
- `.kiya/AI-CONTEXT.md`
- `.kiya/AI-DECISIONS.md`
- `.kiya/AI-HANDOFF.md`
- `.kiya/AI-CHANGELOG.md`
- `docs/00-requirements/15-critical-clarification-plan.md`
- `docs/00-requirements/16-clarification-decision-register.md`
- `docs/00-requirements/17-clarification-decision-template.md`
- `docs/00-requirements/18-erpnext-frappe-feasibility-assessment.md`
- `docs/00-requirements/19-erpnext-frappe-feasibility-matrix.md`
- `docs/00-requirements/20-erpnext-poc-plan.md`
- `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`
- `docs/00-requirements/22-erpnext-kiya-workflow-alignment-matrix.md`
- `docs/00-requirements/23-erpnext-kiya-domain-mapping.md`
- `docs/00-requirements/24-erpnext-kiya-gap-analysis.md`
- `docs/00-requirements/25-erpnext-reuse-vs-build-boundary.md`
- `docs/00-requirements/26-erpnext-workflow-reference-catalog.md`
- `docs/00-requirements/27-erpnext-analysis-review.md`
- `docs/00-requirements/28-cg01-stakeholder-clarification-package.md`
- `docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md`
- `docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md`
- `docs/00-requirements/31-customer-to-cash-detailed-requirements.md`
- `docs/00-requirements/32-procure-to-pay-detailed-requirements.md`
- `docs/00-requirements/33-asset-to-service-detailed-requirements.md`
- `docs/00-requirements/34-shared-foundation-requirements-baseline.md`
- `docs/00-requirements/35-remaining-module-baselines.md`
- `docs/00-requirements/36-phase-0-completion-assessment.md`
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

## Important Decisions

- BRD version 2.0 is the Phase 0A source of truth.
- Phase 0 remains documentation-only and technology-neutral.
- No direct Customer Service-to-end-to-end-flow mapping is asserted because the BRD does not state one.
- Phase 0B detailed requirements must remain BRD-first, evidence-based, technology-neutral, traceable, and explicit about uncertainty.
- Shared foundation analysis identifies 15 foundation records; 11 explicit critical/high dependency records require coordinated specification.
- `AGENTS.md` and `.kiya/` form the persistent project-context bridge between AI agents; `PROJECT-STATE.md` remains the authoritative current-state snapshot.
- The clarification plan assigns 9 Critical and 6 High questions, with 6 Blocking and 9 Partially Blocking.
- `DEC-012` / `CD-001`: Adopt a HYBRID scope-expansion approach for Phase 0B-2 detailed requirements: fully detail core business flows (C2C, P2P, A2S) while using proven ERP-standard behavior as a reference baseline for non-specified standard features without automatic ERPNext coupling.
- `DEC-013` / `CD-002`: Use BUSINESS STATUS as the primary transactional lifecycle and status model representing operational progression; explicitly reject ERPNext's dual `docstatus` (Draft/Submitted/Cancelled) model.
- ERPNext/Frappe assessment and reverse engineering are reference material only, NOT an approved platform selection or architecture decision.
- ERPNext v17 develop tree is GPLv3; Frappe Framework is MIT. Direct core modification is strictly prohibited; legal licensing review is mandatory.
- KIYA must strictly own 8 strategic seams: Product/Domain Boundaries, SaaS Control Plane, API Gateway, AI Governance, BI/EPM, UX/Mobile, Security/Audit, and Tax Compliance.
- `ADR-001` (`DEC-014`): Formally adopted Candidate C (Frappe Framework + Selective ERPNext Core Reuse Under Evaluation) as PROVISIONAL ARCHITECTURE RECOMMENDATION with Candidate D (Frappe Framework + Mostly Custom KIYA Apps) as evaluated fallback / contingency option; status is `PROPOSED / CONDITIONAL` pending successful clearance of `PoC-01`..`PoC-04` and Gate L-01 legal licensing review.
- `ADR-002` (`DEC-015`): Authoritative Single-Source Master Data Registry Model (`PROPOSED / ALIGNED WITH DEC-007`).
- `ADR-003` (`DEC-016`): Decoupled Operational Business Status Lifecycle Architecture (`PROPOSED / ALIGNED WITH CD-002`).
- `ADR-004` (`DEC-017`): Anti-Corruption Framework Insulation & Strategic Seams (`PROPOSED`).
- `ADR-005` (`DEC-018`): Multi-Tenant Operational Isolation Topology (`PROVISIONAL / SUBJECT TO BENCHMARKING`).
- `ADR-006` (`DEC-019`): Asynchronous Decoupling of Intelligence, Analytics & Background Workloads (`PROPOSED`).

## Open Issues

- OQ-001 and OQ-002 are formally resolved via approved decisions `CD-001` and `CD-002`.
- Questions OQ-003 through OQ-015 remain open and unresolved, governed by Stakeholder Gates `STK-01` through `STK-04` and technical PoCs in `ARCH-08`.
- Platform architecture baseline is complete; implementation commitments remain deferred to Phase 2.

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

## Next Phase

**Phase 2 — Technical PoC Validation, Component Architecture & Detailed Design:**
1. Execute `PoC-01` (SaaS Control Plane & Multi-Tenant Data Isolation).
2. Execute `PoC-02` (India Statutory Tax & NIC E-Invoicing Integration).
3. Execute `PoC-03` (High-Concurrency Transaction & Read-Replica Load Benchmark).
4. Execute `PoC-04` (Mobile Offline Synchronization & Conflict Resolution).
5. Obtain corporate legal licensing opinion on Frappe MIT vs ERPNext GPLv3 (`Gate L-01`).
6. Conduct Stakeholder Clarification Sessions for `STK-01` through `STK-04` (`OQ-003` to `OQ-015`).

## Last Validation

14 September 2026 — Phase 1 Final Seal Gate PASSED (`docs/02-architecture/01` through `11` and `docs/PHASE-1-COMPLETE-REVIEW-PACKAGE.md`). Customer Service Enquiry separation verified; exact Phase 0 OQ-003..OQ-015 mappings restored; 238 functional requirement baseline coverage verified without conflation of subordinate flow records; Candidate C provisional status and Candidate D evaluated fallback confirmed; Candidate E fairly evaluated; 28/28 modules and 15/15 SFs verified; formal gate verdict confirmed: PHASE 1 COMPLETE WITH CONTROLLED OPEN ITEMS — READY FOR PHASE 2.

## Last Reviewed By

Antigravity


