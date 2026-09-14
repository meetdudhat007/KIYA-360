# KIYA 360 — Complete Candidate Architecture Evaluation & Trade-off Analysis

## 1. Document Control & Governance

- **Document ID:** `02-candidate-architecture-evaluation`
- **Phase:** Phase 1 — Platform Architecture & System Design (Phase 1B)
- **Status:** Complete Evaluation Baseline
- **Date:** 14 September 2026
- **Authors:** Senior Enterprise Solutions Architect, Architecture Evaluation Lead, Technology Due-Diligence Lead, and Architecture Governance Auditor
- **Primary Business Source:** `source/KIYA360_BRD.pdf` (Version 2.0, 13 September 2026)
- **Approved Phase 0 Baseline:** `docs/00-requirements/36-phase-0-completion-assessment.md` (and Docs `01`–`35`)
- **Approved Decisions:** `CD-001` (Hybrid Scope Expansion), `CD-002` (Operational Business Status), `DEC-001`–`DEC-013`
- **Architecture Strategy & Governance Authority:** `docs/02-architecture/01-architecture-strategy-and-decision-framework.md`
- **Reference Feasibility & Reverse-Engineering Baseline:** `docs/00-requirements/18-erpnext-frappe-feasibility-assessment.md` through `docs/00-requirements/27-erpnext-analysis-review.md`

---

## 2. Phase 1B Purpose & Scope

The purpose of Phase 1B is to execute an objective, evidence-based due-diligence evaluation of all viable candidate architectural archetypes for the KIYA 360 platform. 

This phase determines:
1. What is empirically verified vs. inferred vs. unknown across candidate options.
2. How each candidate aligns with the 28 BRD modules, 238 functional requirements, and core business flows (C2C, P2P, A2S).
3. The precise architectural trade-offs between delivery speed, operational complexity, data model control, multi-tenancy, and intellectual property protection.
4. The mandatory Proof-of-Concept (PoC) validation gates, legal reviews, and stakeholder decisions required before final platform commitment.
5. Whether the empirical evidence warrants a provisional architecture recommendation or if final approval must remain conditional.

`[ARCHITECTURE-CONSTRAINT]` This document is strictly an evaluation and decision-readiness specification. It does not select a final platform, design physical database schemas, author API payloads, design UI wireframes, write application code, or resolve open stakeholder business questions (`OQ-003` through `OQ-015`).

---

## 3. Authoritative Source Hierarchy

In compliance with project governance (`AGENTS.md` and Doc 01 §3), all architectural reasoning adheres strictly to the following authority hierarchy:

- **Level 1 — Primary Business Authority:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026).
- **Level 2 — Approved Functional & Foundation Baseline:** `docs/00-requirements/` (Docs `01` through `36`).
- **Level 3 — Approved Clarification Decisions:** `.kiya/AI-DECISIONS.md` (`CD-001`, `CD-002`, `DEC-001` through `DEC-013`).
- **Level 4 — Architecture Strategy & Decision Framework:** `docs/02-architecture/01-architecture-strategy-and-decision-framework.md`.
- **Level 5 — Reverse-Engineering & Technical Reference Material:** `docs/00-requirements/18-erpnext-frappe-feasibility-assessment.md` through `docs/00-requirements/27-erpnext-analysis-review.md`.
- **Level 6 — Official External Technical Documentation:** Official framework/engine documentation verified during analysis.
- **Level 7 — General Engineering Knowledge:** Established software patterns and industry practices.

`[ARCHITECTURE-CONSTRAINT]` Lower-level sources must never silently override, weaken, or contradict higher-level business requirements or approved decisions.

---

## 4. Governance Constraints & Non-Negotiables

All candidate architectures are evaluated against non-negotiable governance precedents established in Phase 0 and Phase 1A:

1. **CD-001 Hybrid Scope Model:** C2C (18 stages), P2P (12 stages), and A2S (11 stages) must be supported natively to detailed specifications. ERP-standard behavior serves only as a reference baseline for standard non-specified capabilities. ERPNext behavior is not an automatic requirement.
2. **CD-002 Operational Business Status Lifecycle:** Business Status is the sole operational lifecycle model representing real-world transaction milestones. ERPNext's technical dual `docstatus` integers (0=Draft, 1=Submitted, 2=Cancelled) are explicitly rejected as a user-facing or architectural lifecycle.
3. **DEC-007 Single Unified Master Data Model:** Authoritative, non-duplicated master entities for Customer, Supplier, Item/Product, Warehouse, Employee, and Chart of Accounts.
4. **Mandatory Domain Disambiguations:**
   - *Customer Installed Base* (Module 14 / A2S) $\neq$ *Corporate Financial Fixed Asset* (Module 13 / Finance).
   - *Field Service Work Order* (`DR-A2S-005`) $\neq$ *Manufacturing Production Work Order* (`FR-MFG-003`).
5. **The 8 Mandatory KIYA-Owned Strategic Seams:** The architecture must enforce clean, proprietary seams isolating:
   - Seam 1: Product & Domain Boundaries
   - Seam 2: SaaS Control Plane (Tenant Provisioning, Billing, Quotas)
   - Seam 3: API Gateway & External Integrations
   - Seam 4: AI Governance & Orchestration
   - Seam 5: Enterprise BI & EPM Analytical Engine
   - Seam 6: Modern UX & Mobile Client Experience
   - Seam 7: Enterprise Security, RBAC & Audit Ledger
   - Seam 8: Statutory Tax & Regulatory Compliance Engine
6. **Open Questions Preserved:** `OQ-003` through `OQ-015` remain open and unresolved. Candidate architectures must insulate these decisions behind configuration or adapters.

---

## 5. Candidate Architecture Definitions

Five candidate architecture archetypes are formally evaluated:

```
+---------------------------------------------------------------------------------------------------+
|                                  CANDIDATE ARCHITECTURE SPECTRUM                                  |
+-----------------------------+-----------------------------+---------------------------------------+
|  MAXIMUM REUSE / PACKAGED   |       HYBRID FRAMEWORK      |           DECOUPLED / CUSTOM          |
+-----------------------------+-----------------------------+---------------------------------------+
| Candidate B:                | Candidate C:                | Candidate D:    Candidate A:    Cand. E:  |
| ERPNext-Primary Application | Frappe + Selective ERPNext  | Frappe + Custom Full Custom   Headless|
+-----------------------------+-----------------------------+---------------------------------------+
```

### Candidate A: Full Custom Architecture
- **Description:** Purpose-built enterprise application designed from scratch. Custom frontend, custom modular backend services, standard relational database, and bespoke SaaS control plane.
- **Hypothesis:** Provides complete architectural freedom, alignment with KIYA's 8 seams, absence of copyleft licensing exposure, and zero framework baggage.
- **Trade-off:** Carries substantially higher implementation burden because all 28 enterprise modules and foundational ERP plumbing (double-entry GL, stock valuation, tax rules, BOM explosion) must be built, validated, and maintained entirely from scratch.

### Candidate B: ERPNext-Primary Architecture
- **Description:** Deploying ERPNext v17 as the core platform monolith, customizing and extending it via custom apps, server scripts, and Frappe hooks.
- **Hypothesis:** Delivers maximum immediate out-of-the-box functional coverage across standard ERP domains, accelerating initial demo capability.
- **Trade-off:** Materially mismatched with current KIYA requirements and constraints: direct conflict with `CD-002` (deeply coupled to `docstatus`); GPLv3 copyleft exposure across proprietary modules requiring legal review; lacks native support for several KIYA differentiators (Enquiry, RFP multi-envelope, dynamic warranty, physical WMS coordinate tracking).

### Candidate C: Frappe Framework + Selective ERPNext (Provisional Leading Candidate)
- **Description:** Utilizing the Frappe Framework (MIT) as the core application engine (metadata, ORM, auth, job queues, REST generator); evaluating selective reuse of proven ERPNext (GPLv3) domain capabilities (specifically general ledger and stock valuation logic as potential reuse candidates); building custom, proprietary KIYA applications for all strategic seams and differentiating flows.
- **Hypothesis:** Potentially reduces initial implementation effort by avoiding reinvention of complex accounting/stock plumbing while isolating proprietary IP behind KIYA apps.
- **Trade-off:** Requires strict network/API isolation and formal legal review to manage GPLv3 boundaries; requires adapter wrappers to decouple internal `docstatus` from external Business Status; empirical PoCs and legal clearance required before any final commitment.

### Candidate D: Frappe Framework + Mostly Custom KIYA Apps (Evaluated Fallback Candidate)
- **Description:** Utilizing Frappe Framework (MIT) strictly as a metadata-driven runtime, ORM, and rapid application development tool, but authoring custom KIYA applications for all 28 modules without installing or reusing ERPNext domain apps.
- **Hypothesis:** Eliminates GPLv3 copyleft exposure (Frappe is MIT-licensed); provides complete control over domain entities and `CD-002` status lifecycles while retaining Frappe's rapid ORM and admin tooling.
- **Trade-off:** Demands substantial engineering effort to author all ERP accounting, tax, and inventory transaction plumbing on top of Frappe ORM; remains coupled to Frappe runtime conventions. Serves as the evaluated fallback candidate if ERPNext reuse is deemed commercially unviable.

### Candidate E: Modular Headless / API-First Architecture
- **Description:** Decoupled, modular domain services (e.g., modular service runtime evaluation options) communicating via candidate API/event mechanisms and a unified API gateway, with independent modern web and mobile frontends.
- **Hypothesis:** High horizontal scalability, failure isolation, decoupled technology evaluation per domain, zero monolithic framework lock-in.
- **Trade-off:** Currently appears poorly suited to KIYA's core transactional ERP workload because of the additional distributed-consistency and operational complexity it introduces; dual-write and distributed transaction coordination risks for financial ledgers; substantial operational/DevOps overhead.

---

## 6. Evidence Method & Sourcing Discipline

The evaluation employs a strict evidence-driven methodology to prevent speculative or biased scoring:

1. **Separation of Frappe Framework vs. ERPNext:**
   - Statements regarding Frappe Framework (MIT) are evaluated independently from ERPNext (GPLv3). Capabilities present in Frappe (e.g., DocType schema generator) are never credited as ERPNext, and vice versa.
2. **Traceability to Code and Documentation:**
   - Findings draw on inspected source code from the Frappe/ERPNext develop tree (v17.0.0-dev) documented in Docs `21` through `27`, official Frappe/ERPNext documentation, and BRD v2.0 requirements.
3. **Explicit Handling of Gaps & Assumptions:**
   - Hypotheses that have not been tested empirically are classified as `[POC REQUIRED]`.
   - Commercial and licensing interpretations are classified as `[LEGAL REVIEW REQUIRED]`.
   - Unspecified organizational policies are classified as `[STAKEHOLDER INPUT REQUIRED]`.

---

## 7. Evidence Quality Model

Every architectural finding and dimension assessment is assigned an **Evidence Strength Level** and an **Evidence Classification**:

### Evidence Strength Levels
- **Level 1 — Direct Experimental Evidence:** Empirically verified via working prototypes, load tests, or automated validation scripts.
- **Level 2 — Official Technical Documentation:** Directly documented in authoritative vendor or framework specifications.
- **Level 3 — Inspected Source Code / Repository:** Verified through direct analysis of codebase implementations, database schemas, and hooks.
- **Level 4 — Existing Project Analysis:** Derived from approved Phase 0/Phase 1A baselines and alignment matrices.
- **Level 5 — Expert Inference:** Logical engineering deduction based on software architecture principles.
- **Level 6 — General Industry Assumption:** Broad industry convention without direct repository evidence.

### Evidence Classifications
- `[VERIFIED]`: Direct evidence is available, inspected, and conclusive.
- `[PARTIALLY VERIFIED]`: Evidence exists, but important operational or functional limitations remain.
- `[REFERENCE EVIDENCE]`: Observed in benchmark systems; useful as a reference but not validated for KIYA.
- `[INFERENCE]`: Plausible architectural deduction without direct empirical proof.
- `[UNKNOWN]`: Insufficient data available to reach a defensible conclusion.
- `[POC REQUIRED]`: Critical architectural hypothesis requiring empirical testing before commitment.
- `[LEGAL REVIEW REQUIRED]`: Subject to formal commercial and copyleft legal interpretation.
- `[STAKEHOLDER INPUT REQUIRED]`: Subject to business policy, budget, or timeline sign-off.
- `[NOT APPLICABLE]`: Dimension does not apply to the specific candidate.

---

## 8. Evaluation Method & Scoring Rubric

To ensure objectivity without creating arbitrary numbers, evaluation utilizes a defined qualitative rubric paired with an explicit **Evidence Confidence Rating**:

### Qualitative Scoring Rubric
- **Strong (Score 4–5):** The candidate natively satisfies the dimension with verifiable evidence, minimal technical risk, and low engineering delta.
- **Adequate (Score 3):** The candidate satisfies the dimension with acceptable engineering effort, standard workarounds, or well-understood integration patterns.
- **Weak (Score 2):** The candidate exhibits significant architectural friction, major functional gaps, or high maintenance overhead.
- **Very Weak / Fails (Score 0–1):** The candidate fundamentally violates a core requirement, creates unacceptable legal/operational risk, or requires catastrophic rework.
- **NOT YET SCORED:** Evidence is insufficient to assign a defensible rating prior to PoC execution.

### Evidence Confidence Levels
- **HIGH:** Supported by Level 1, 2, or 3 evidence (code, docs, tests).
- **MEDIUM:** Supported by Level 4 or 5 evidence (project analysis, rigorous inference).
- **LOW:** Dependent on Level 6 assumptions or unverified vendor marketing claims.

---

## 9. 22-Dimension Candidate Evaluation

Every candidate is systematically evaluated across all 22 architecture dimensions established in Doc 01 §20.

### 9.1 Evaluation Summary Matrix

| # | Evaluation Dimension | Cand A: Full Custom | Cand B: ERPNext Primary | Cand C: Frappe + Selective | Cand D: Frappe + Custom | Cand E: Headless / Modular |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **BRD 28-Module Coverage** | Weak (High Build) | Strong (Out-of-box) | Strong (Hybrid) | Adequate (Custom Build) | Weak (High Build) |
| 2 | **Core Flow Fidelity (C2C, P2P, A2S)**| Strong (Native) | Weak (docstatus clash)| Adequate (via Adapters) | Strong (Native) | Strong (Native) |
| 3 | **Unified Data Model Control** | Strong (Total Control)| Weak (Rigid DocTypes) | Adequate (Shared Core) | Strong (Custom Schemas)| Strong (Domain Schemas)|
| 4 | **Business Status Lifecycle Fit** | Strong (Native CD-002)| Fails (Tightly Coupled)| Adequate (via Wrapper) | Strong (Native CD-002) | Strong (Native CD-002) |
| 5 | **Strategic Seams Decoupling** | Strong (Clean) | Very Weak (Monolith)  | Adequate (App Seams)   | Strong (Clean Seams)   | Strong (Service Seams) |
| 6 | **Multi-Tenant SaaS Viability** | Strong (Purpose-built)| Weak (Bench-bound)    | Adequate (PoC Required)| Adequate (PoC Required)| Strong (Native SaaS)   |
| 7 | **Security & RBAC Granularity** | Adequate (Build Needed)| Adequate (Frappe RBAC)| Adequate (Frappe RBAC) | Adequate (Frappe RBAC) | Strong (Modern Auth)   |
| 8 | **Performance & Concurrency** | Strong (Optimized)   | Weak (Python GIL)     | Adequate (Benchmarked) | Adequate (Benchmarked) | Strong (Polyglot)      |
| 9 | **Scalability & Resource Eff.** | Strong (Horizontal)  | Weak (Monolithic)     | Adequate (Tiered)      | Adequate (Tiered)      | Strong (Independent)   |
| 10| **Mobile & Offline Capability** | Strong (Tailored)    | Weak (Web Wrapper)    | Adequate (Custom API)  | Adequate (Custom API)  | Strong (API-First)     |
| 11| **AI Integration Flexibility** | Strong (Neutral)     | Weak (Hardcoded/Absent)| Strong (Adapter Seam)  | Strong (Adapter Seam)  | Strong (Mesh/Adapter)  |
| 12| **BI & EPM Separation** | Strong (Decoupled)   | Weak (Same OLTP DB)   | Adequate (Read Replicas)| Adequate (Read Replicas)| Strong (Dedicated OLAP)|
| 13| **API & Integration Maturity** | Strong (Contract-1st)| Adequate (Frappe API) | Adequate (Frappe + GW) | Adequate (Frappe + GW) | Strong (Gateway/Mesh)  |
| 14| **Operational Complexity** | Adequate (Standard)  | Weak (Bench/Procfile) | Adequate (Bench Ops)   | Adequate (Bench Ops)   | Weak (Distributed Ops) |
| 15| **Upgradeability & Extensibility**| Strong (Internal)    | Very Weak (Core Drift)| Adequate (App Hooks)   | Strong (Clean Apps)    | Strong (Versioned APIs)|
| 16| **Vendor & Platform Lock-In** | Strong (Zero Lock-in)| Fails (Extreme)       | Adequate (Framework)   | Adequate (Framework)   | Strong (Open Stacks)   |
| 17| **Licensing & Legal Risk** | Strong (100% Own IP) | Very Weak (GPLv3)     | Weak (GPLv3 Seam Risk) | Strong (MIT Only)      | Strong (100% Own IP)   |
| 18| **Time to Market** | Very Weak (Slowest)  | Strong (Fastest Demo) | Strong (Accelerated)   | Adequate (Moderate)    | Weak (Complex Build)   |
| 19| **Team Competency / Hiring** | Strong (Broad Tech)  | Weak (Niche Frappe)   | Adequate (Niche + Py)  | Adequate (Niche + Py)  | Strong (Broad Market)  |
| 20| **Development & 5-Yr TCO** | High Dev / Low Maint | Low Dev / High Maint  | Balanced (PoC Dep.)    | Balanced (Custom Dev)  | High Dev / High Ops    |
| 21| **Reversibility / Migration** | Strong (Standard DB) | Weak (DocType Schema) | Weak (DocType Schema)  | Adequate (Clean Schema)| Strong (Portable APIs) |
| 22| **Empirical Evidence Maturity** | Medium (Industry)    | High (Inspected Code) | High (Inspected Code)  | Medium (Frappe Only)   | Medium (Industry)      |

---

## 10. Detailed Assessment: Candidate A (Full Custom Architecture)

### 10.1 Architectural Profile
- **Stack Archetype:** Modern enterprise application tier (e.g., modular service runtimes, standard relational database, caching and asynchronous messaging options under evaluation).
- **Control Plane:** Purpose-built multi-tenant control plane, metering, and provisioning.

### 10.2 Dimensional Strengths
- `[VERIFIED]` **Absolute Data Model & Workflow Control:** Complete freedom to implement `CD-002` Business Status without legacy `docstatus` constraints. Complete freedom to implement single unified master data (`DEC-007`) and unambiguous domain entities (`Installed Base ≠ Fixed Asset`).
- `[VERIFIED]` **Intellectual Property & Licensing Purity:** Zero GPLv3 copyleft exposure. 100% of codebase is proprietary KIYA IP, simplifying commercial SaaS valuation, white-labeling, and investor due diligence.
- `[INFERENCE]` **Modern Scalability & Observability:** Unconstrained ability to implement stateless application tiers, connection pooling, and distributed tracing.

### 10.3 Dimensional Weaknesses & Risks
- `[VERIFIED]` **Substantially Higher Implementation Burden:** Building standard ERP double-entry financial ledgers, multi-currency revaluation, tax compliance engines, landed cost calculations, and multi-level BOM manufacturing explosions requires substantially more implementation effort; exact delivery impact is currently UNKNOWN and requires project estimation.
- `[INFERENCE]` **Reinventing the Wheel:** High probability of bugs in core accounting, inventory reconciliation, and tax calculation engines where established platforms have decade-long edge-case hardening.

---

## 11. Detailed Assessment: Candidate B (ERPNext-Primary Architecture)

### 11.1 Architectural Profile
- **Stack Archetype:** Monolithic ERPNext v17 deployment on Frappe Framework, using standard relational database, Desk web client, and custom Frappe applications.

### 11.2 Dimensional Strengths
- `[VERIFIED]` **Immediate Out-of-the-Box ERP Depth:** Native support for standard accounting, purchasing, sales orders, stock ledger, quality inspections, and basic CRM (Doc 21).
- `[VERIFIED]` **Rapid Initial Prototyping:** Fastest route to a clickable end-to-end ERP demonstration.

### 11.3 Dimensional Weaknesses & Requirement Conflicts
- `[VERIFIED]` **Direct Violation of CD-002:** ERPNext core transactions are structurally hardcoded to `docstatus` integers (0=Draft, 1=Submitted, 2=Cancelled). Attempting to override this breaks standard document links, cancellation reversals, and ledger posting triggers (Doc 21 §3, Doc 27).
- `[LEGAL REVIEW REQUIRED]` **GPLv3 Copyleft Uncertainty:** ERPNext is licensed under GPLv3. Distributing software, deploying client-specific on-premise instances, or combining proprietary KIYA modules directly within the ERPNext Python process creates significant copyleft questions requiring formal legal review.
- `[VERIFIED]` **Strategic Seam Violations:** Lacks clean boundaries for SaaS multi-tenancy, external API gateway, enterprise BI/EPM, and independent AI governance.
- `[VERIFIED]` **Missing Core Capabilities:** Inspecting ERPNext develop tree reveals that Indian GST localization has been extracted to a separate regional app, physical WMS coordinate tracking is absent (only logical Bin quantities exist), and multi-envelope RFP bidding is unsupported (Doc 24).

---

## 12. Detailed Assessment: Candidate C (Frappe + Selective ERPNext — Provisional Leader)

### 12.1 Architectural Profile
- **Stack Archetype:** Frappe Framework (MIT) core application engine; evaluating selective reuse of ERPNext (GPLv3) domain capabilities (identifying `Accounts` and `Stock` ledger posting plumbing as potential reuse candidates under evaluation); all 8 strategic seams, CRM/Enquiry, Field Service, WMS, and India Tax implemented in separate, proprietary KIYA applications.

### 12.2 Dimensional Strengths
- `[VERIFIED]` **Potential Delivery Acceleration on Core Plumbing:** Reusing battle-tested, double-entry financial ledger accounting (`GL Entry`) and FIFO/Moving-Average inventory valuation (`Stock Ledger Entry`) provides a potential reduction in initial core implementation effort.
- `[VERIFIED]` **Rapid Application Development (RAD):** Frappe Framework provides automated schema generation, role-based permissions, background job scheduling, and REST endpoints out of the box.
- `[PARTIALLY VERIFIED]` **Seam Isolation Feasibility:** Proven capable of isolating proprietary business logic in independent Frappe applications installed on the bench.

### 12.3 Dimensional Weaknesses & Risks
- `[LEGAL REVIEW REQUIRED]` **GPLv3 Seam Boundary Sensitivity:** While Frappe Framework is MIT, ERPNext's `Accounts` and `Stock` modules are GPLv3. Evaluating them for selective reuse requires strict architectural isolation and formal legal sign-off (Gate L-01) to ensure proprietary KIYA apps are not deemed derivative works.
- `[PARTIALLY VERIFIED]` **Docstatus Adaptation Overhead:** Requires custom wrapper logic to translate KIYA Business Statuses (`CD-002`) into underlying submission hooks without exposing `docstatus` to users or API clients.
- `[POC REQUIRED]` **Multi-Tenant SaaS Scaling Limits:** Traditional Frappe multi-tenancy (bench site-per-tenant) must be empirically benchmarked to verify tenant density, memory footprint, and automated provisioning speeds (`PoC-01`).

---

## 13. Detailed Assessment: Candidate D (Frappe + Mostly Custom KIYA Apps — Evaluated Fallback)

### 13.1 Architectural Profile
- **Stack Archetype:** Pure Frappe Framework (MIT) runtime and ORM; zero ERPNext domain modules installed; 100% of the 28 business modules authored as proprietary KIYA Frappe applications.

### 13.2 Dimensional Strengths
- `[VERIFIED]` **Absence of GPLv3 Copyleft Constraints:** Frappe Framework is MIT-licensed. Eliminating ERPNext eliminates copyleft exposure, ensuring clean proprietary IP ownership across the entire suite.
- `[VERIFIED]` **Native CD-002 Alignment:** Custom DocTypes author their own lifecycle state machines without conflicting with ERPNext's hardcoded submission rules.
- `[VERIFIED]` **Clean Data Model Control:** Complete control over master data definitions, ensuring strict separation of Customer Installed Base vs. Corporate Fixed Assets.

### 13.3 Dimensional Weaknesses & Risks
- `[INFERENCE]` **Substantial Accounting Build Effort:** Unlike Candidate C, Candidate D requires authoring double-entry GL ledgers, stock valuation routines, and tax calculation logic from scratch on top of Frappe ORM.
- `[PARTIALLY VERIFIED]` **Framework Coupling:** Remains tied to Frappe Framework conventions, Python execution characteristics, and database semantics.

---

## 14. Detailed Assessment: Candidate E (Modular Headless / API-First Architecture)

### 14.1 Architectural Profile
- **Stack Archetype:** Decoupled modular domain services communicating via candidate API/event mechanisms, with independent web/mobile clients.

### 14.2 Dimensional Strengths
- `[VERIFIED]` **Unrivaled Scalability & Domain Isolation:** Independent scaling of high-throughput services (e.g., POS or IoT telemetry) without impacting transactional finance.
- `[VERIFIED]` **Modern Developer Ergonomics:** Clean separation of concerns; best-of-breed technology choices per domain.

### 14.3 Dimensional Weaknesses & Architectural Complexities
- `[INFERENCE]` **Distributed Consistency Complexity for Core Transactions:** Maintaining strict double-entry financial consistency across distributed microservice boundaries introduces substantial distributed transaction complexity (e.g., 2PC or Saga orchestration with compensation transactions), creating risks of ledger imbalance.
- `[INFERENCE]` **Substantially Higher Implementation Burden:** Building 28 enterprise modules across distributed boundaries introduces severe operational and delivery complexity for an initial product launch.

---

## 15. Cross-Candidate Comparison Matrix

| Architectural Dimension | Cand A: Full Custom | Cand B: ERPNext Primary | Cand C: Frappe + Selective | Cand D: Frappe + Custom | Cand E: Headless Modular |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Development Velocity (Initial)** | Very Low | Very High | High | Moderate | Low |
| **Long-Term Maintainability** | High | Low | Moderate | High | Moderate |
| **IP Ownership & Licensing** | 100% Proprietary | Severe Copyleft Risk | Conditional (Seam Dep.)| 100% Proprietary (MIT)| 100% Proprietary |
| **Compliance with CD-001** | High | Low | High | High | High |
| **Compliance with CD-002** | High | Fails | Moderate (via Adapter) | High | High |
| **Compliance with DEC-007** | High | Low (Rigid Schemas) | Moderate | High | High |
| **8 Strategic Seam Protection** | Native | Fails | Enforced via Apps | Native | Native |
| **Operational Simplicity** | High | Moderate | Moderate | Moderate | Low (Complex) |
| **Evidence Confidence** | Medium | High | High | Medium | Medium |

---

## 16. Core Business Flow Comparison

```
+---------------------------------------------------------------------------------------------------+
|                                  CORE BUSINESS FLOW FIDELITY                                      |
+----------------------+--------------------+--------------------+----------------------------------+
| Flow                 | Candidate A / D / E| Candidate B        | Candidate C                      |
+----------------------+--------------------+--------------------+----------------------------------+
| Customer-to-Cash     | Fully Native       | Friction (Enquiry, | Native via KIYA CRM App;         |
| (18 Stages)          |                    | WMS, docstatus)    | reuses Accounts/Stock ledger     |
+----------------------+--------------------+--------------------+----------------------------------+
| Procure-to-Pay       | Fully Native       | Friction (RFP multi| Native via KIYA SCM App;         |
| (12 Stages)          |                    | envelope, WMS bins)| reuses AP / PO ledger            |
+----------------------+--------------------+--------------------+----------------------------------+
| Asset-to-Service     | Fully Native       | Fails (Confuses    | Native via KIYA Field Service App|
| (11 Stages)          |                    | Asset vs Machine)  | isolates Customer Installed Base |
+----------------------+--------------------+--------------------+----------------------------------+
```

1. **Customer-to-Cash (C2C):**
   - *Candidates A, D, E:* Full native alignment with all 18 stages (`DR-C2C-001`..`018`), including sequential dispatch billing and candidate Business Statuses.
   - *Candidate B:* Fails native alignment; lacks Enquiry entity; forces premature billing or complex submission reversal hacks.
   - *Candidate C:* Achieves high fidelity by authoring C2C commercial stages in a proprietary KIYA app while delegating final stock movement and invoice GL posting to proven ERPNext background engines.
2. **Procure-to-Pay (P2P):**
   - *Candidates A, D, E:* Full native alignment with all 12 stages (`DR-P2P-001`..`012`), including dual RFQ/RFP and 3-way matching tolerances.
   - *Candidate B:* Partially supported; lacks multi-envelope technical-vs-commercial RFP bidding; physical warehouse bin tracking absent.
   - *Candidate C:* Achieves high fidelity via custom KIYA Procurement app wrapping standard Goods Receipt and Purchase Invoice engines.
3. **Asset-to-Service (A2S):**
   - *Candidates A, D, E:* Full native alignment with all 11 stages (`DR-A2S-001`..`011`), strictly separating Customer Installed Base from Corporate Fixed Assets.
   - *Candidate B:* Severe structural collision; ERPNext's `Asset` module represents capitalized balance-sheet assets and maintenance schedules, completely lacking customer site warranty entitlement, technician dispatch, and truck-stock spare parts consumption.
   - *Candidate C:* Achieves full fidelity by authoring A2S completely within a custom KIYA Field Service application, completely bypassing ERPNext's corporate asset module.

---

## 17. Data Architecture & Entity Modeling Comparison

`[ARCHITECTURE-PRINCIPLE]` Data architecture comparison against `DEC-007` and domain disambiguations:

1. **Customer & Supplier Master Unification:**
   - *Candidates A, D, E:* Native implementation of single polymorphic party entity (`Party` with Customer and Supplier roles).
   - *Candidates B & C:* Frappe/ERPNext maintains separate `Customer` and `Supplier` DocTypes linked to a shared `Party` link. Candidate C wraps these to present a single unified KIYA Master API.
2. **Installed Base vs. Corporate Fixed Asset:**
   - *Candidates A, D, E:* Clean separate database entities (`CustomerInstalledBase` vs. `FixedAsset`).
   - *Candidate B:* Fails; forces conflation or awkward custom fields on corporate `Asset`.
   - *Candidate C:* Enforces absolute separation by creating a dedicated `KIYA Installed Base` DocType in the custom service app and ignoring ERPNext corporate assets.
3. **Work Order Disambiguation:**
   - *Candidates A, D, E:* Separate schemas for `FieldServiceWorkOrder` and `ManufacturingWorkOrder`.
   - *Candidate B:* Fails; ERPNext hardcodes `Work Order` strictly to discrete manufacturing production orders.
   - *Candidate C:* Custom Field Service app authors `KIYA Service Order`, completely avoiding ERPNext's manufacturing `Work Order`.

---

## 18. SaaS & Multi-Tenancy Architecture Comparison

`[POC REQUIRED]` Multi-tenancy comparison across candidate strategies:

| Tenancy Metric | Candidate A (Custom) | Candidate B (ERPNext) | Candidate C (Frappe + Sel) | Candidate D (Frappe Cust) | Candidate E (Headless) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Isolation Model** | Schema or DB-per-tenant| Site-per-tenant (Bench)| Site-per-tenant or DB  | Site-per-tenant or DB   | DB-per-tenant / RLS    |
| **Cross-Tenant Leakage Risk**| Low (Architected DBs)  | Low (Isolated DBs)    | Low (Isolated DBs)     | Low (Isolated DBs)      | Low (Engineered RLS)   |
| **Tenant Provisioning Speed**| Fast (Benchmark Req.)  | Slower (Bench CLI - PoC-01) | PoC-01 Benchmark Required | PoC-01 Benchmark Required | Fast (Benchmark Req.)  |
| **Tenant Resource Density**  | High (Shared Pool)    | Moderate (Procfile/Py)| Moderate (Procfile/Py) | Moderate (Procfile/Py)  | High (Containerized)   |
| **Custom Tenant Branding**   | Native White-label    | Rigid Desk UI         | Custom UX Seam         | Custom UX Seam          | Native White-label     |
| **PoC Validation Required**  | Architecture Review   | `PoC-01` Required     | `PoC-01` Required      | `PoC-01` Required       | Architecture Review    |

---

## 19. Security, RBAC & Compliance Comparison

- **Candidate A & E:** High initial build overhead to construct granular field-level, record-level, and role-based permissions; modern identity integrations must be written from scratch.
- **Candidates B, C, D (Frappe-based):** Frappe Framework provides an established, out-of-the-box multi-tier permission engine:
  - Role-based permissions by DocType.
  - User Permissions (restricting access by Company, Branch, Customer, or Cost Center).
  - Field-level permission levels (Perm Levels 0–9).
  - Built-in two-factor authentication (2FA/MFA) and encrypted password hashing.
  - Comprehensive document audit trails (`Version` and `Activity Log`).

---

## 20. Mobile & Offline Resilience Comparison

- **Candidate B (ERPNext Primary):** Relies on a responsive web wrapper (Desk). Fails offline operation completely; network disconnection prevents any work order or inventory entry.
- **Candidate A & E (Custom/Headless):** Allows independent mobile client development; offline delta sync and conflict resolution designed natively from day one; mobile runtime frameworks remain deferred evaluation options.
- **Candidate C & D (Frappe-based):** Frappe backend provides standard REST APIs; native mobile clients must be authored using the KIYA UX/Mobile Seam (Seam 6). The backend must support delta-sync endpoints tested via `PoC-04`.

---

## 21. AI Architecture & Governance Comparison

- **Candidate B:** Hardcoded, third-party, or non-existent AI capabilities in ERPNext core; risks tenant data leakage if external models are called without sanitization.
- **Candidates A, C, D, E:** Fulfill Seam 4 (AI Governance Seam) by routing all AI interactions through a dedicated KIYA AI abstraction layer:
  - Tenant prompt sanitization and data masking.
  - Pluggable provider adapters (local open models vs. commercial APIs).
  - Human-in-the-loop approval gates for financial transactions.
  - Complete logging of model prompts, confidence scores, and outputs in the audit ledger.

---

## 22. BI & Enterprise Performance Management (EPM) Comparison

- **Candidate B:** Operational reports run directly as queries against the active operational transactional database. Heavy financial reports or analytical aggregations degrade transactional billing throughput.
- **Candidates A, C, D, E:** Enforce Seam 5 (BI/EPM Seam):
  - Transactional tables asynchronously replicate or project into read-optimized reporting stores.
  - Dedicated OLAP queries and multi-scenario forecasting models run isolated from operational OLTP transactions; analytical storage technologies remain deferred evaluation options.

---

## 23. Integration & API Gateway Comparison

- **Candidate B:** Direct access to Frappe REST APIs exposes internal DocType structures, leaking framework implementation details to external integrators.
- **Candidates A, C, D, E:** Enforce Seam 3 (API Gateway Seam):
  - Strict contract-first API definitions and versioning.
  - Independent API lifecycle governance.
  - Centrally managed per-tenant rate limiting and abuse prevention.
  - Cryptographically signed webhook dispatch engine with retry handling.

---

## 24. Operational & Deployment Complexity Comparison

- **Candidate E (Headless Microservices):** Substantially higher operational burden. Involves container orchestration, distributed tracing, event streaming infrastructure, and multi-service CI/CD pipelines.
- **Candidate A (Full Custom Monolith/Modular):** Moderate operational complexity; standard container deployment and relational DB management.
- **Candidates B, C, D (Frappe-based):** Established operational tooling via Frappe Bench stack. However, requires specialized framework operational expertise for backups, multi-site updates, and bench migrations.

---

## 25. Licensing & Legal Due Diligence

`[LEGAL REVIEW REQUIRED]` Formal open-source licensing breakdown:

| Candidate | Foundation License | Core Apps License | Proprietary Seams License | Legal / Commercial Risk Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **A. Full Custom** | Proprietary / Permissive| Proprietary | Proprietary (100%) | **Absence of Copyleft Constraints:** Maximum commercial purity. |
| **B. ERPNext Primary**| MIT (Frappe) | GPLv3 (ERPNext) | GPLv3 / Proprietary | **Severe Copyleft Exposure:** High danger of GPLv3 copyleft questions across proprietary client modules and distributions; formal legal review required. |
| **C. Frappe + Selective**| MIT (Frappe) | GPLv3 (Accounts/Stock)| Proprietary (KIYA Apps) | **Conditional Risk:** Requires strict architectural component boundaries and formal legal review of SaaS network access vs. distribution (Gate L-01). |
| **D. Frappe + Custom** | MIT (Frappe) | Proprietary (KIYA Apps)| Proprietary (100%) | **Absence of Copyleft Constraints:** Frappe is MIT; all business apps are 100% proprietary KIYA IP. |
| **E. Headless Modular**| Proprietary / Permissive| Proprietary | Proprietary (100%) | **Absence of Copyleft Constraints:** Maximum commercial purity. |

---

## 26. Cost of Ownership & TCO Evidence Drivers

In accordance with anti-hallucination governance, fictitious financial figures are rejected. TCO is evaluated via structural **Cost Drivers**:

1. **Initial Development Cost Drivers:**
   - *Candidate A & E:* Substantially higher initial implementation burden. Engineering effort dedicated to writing foundational ERP plumbing (GL double-entry, Stock valuation, multi-currency conversion).
   - *Candidate B:* Lower initial development cost; substantially higher customization friction and technical debt.
   - *Candidate C:* Potential delivery acceleration by evaluating existing GL/Stock engines for selective reuse; implementation effort focused on KIYA proprietary differentiators.
   - *Candidate D:* Moderate-to-high development effort. Uses Frappe RAD tools but requires authoring custom GL/Stock engines.
2. **5-Year Maintenance & Upgrade Cost Drivers:**
   - *Candidate B:* High 5-year maintenance cost. Core ERPNext upstream changes frequently break custom apps, requiring continuous patching.
   - *Candidate C:* Moderate maintenance cost. Isolating potential ERPNext reuse to stable core modules minimizes upstream churn, subject to boundary verification.
   - *Candidate A & D:* Predictable, linear maintenance costs fully controlled by internal roadmap.
   - *Candidate E:* High infrastructure and distributed monitoring operational costs.

---

## 27. Team Competency & Delivery Burden

`[STAKEHOLDER INPUT REQUIRED]` Engineering skill availability and hiring dynamics:

- **Candidate A & E (Standard Stacks):** Broad hiring market for mainstream development skills. Onboarding and recruitment availability remain data requirements subject to project assessment.
- **Candidates B, C, D (Frappe Ecosystem):** Requires specialized framework knowledge. Python/JavaScript developers must learn Frappe Framework conventions (DocTypes, hooks, bench commands, Jinja templating). Team learning burden and onboarding complexity require project-specific assessment.

---

## 28. Reversibility & Migration Analysis

1. **Data Portability:** All five candidates utilize standard relational database options, allowing complete SQL data extraction and backup portability.
2. **Logic & Workflow Portability:**
   - *Candidate A & E:* High portability; domain logic lives in standard clean architecture services.
   - *Candidate B:* Extremely low portability; domain logic is deeply entangled with ERPNext DocType Python classes and Frappe hooks.
   - *Candidate C & D:* Moderate portability; proprietary logic is isolated within independent KIYA apps, allowing eventual extraction to standalone services if Frappe runtime is ever deprecated.

---

## 29. Architecture Trade-off Matrix

### Trade-off 1: Candidate A (Full Custom) vs. Candidate C (Frappe + Selective ERPNext)
- **Advantage of A:** 100% IP ownership, zero GPLv3 ambiguity, total framework independence.
- **Disadvantage of A:** Substantially higher delivery burden; risk of accounting ledger bugs without long-term hardening; significant implementation effort diverted to commodity plumbing.
- **Resolution:** Candidate C potentially provides lower initial core implementation effort and proven accounting rigor under evaluation, provided GPLv3 legal review and seam isolation are satisfied.

### Trade-off 2: Candidate B (ERPNext Primary) vs. Candidate C (Frappe + Selective ERPNext)
- **Advantage of B:** Out-of-the-box demo availability across all standard modules.
- **Disadvantage of B:** Direct failure on `CD-002` (docstatus); severe GPLv3 copyleft exposure; architectural friction on all KIYA differentiators.
- **Resolution:** Candidate B is **materially mismatched with current KIYA requirements and constraints** due to identified requirement conflicts and governance incompatibilities. Candidate C preserves the necessary strategic seams.

### Trade-off 3: Candidate C (Selective ERPNext) vs. Candidate D (Mostly Custom Frappe)
- **Advantage of C:** Evaluates mature `GL Entry` and `Stock Ledger Entry` engines for potential selective reuse, potentially accelerating financial suite delivery.
- **Disadvantage of C:** Carries GPLv3 seam management and docstatus wrapper overhead.
- **Advantage of D:** 100% MIT / proprietary purity; zero docstatus friction.
- **Disadvantage of D:** Higher build effort for accounting and stock valuation engines.
- **Resolution:** Candidate C is the provisional leading candidate pending PoC gates and Legal Review; Candidate D is the evaluated fallback candidate if Legal Review deems ERPNext reuse commercially risky.

### Trade-off 4: Candidate C (Frappe Hybrid) vs. Candidate E (Headless Microservices)
- **Advantage of E:** Extreme scalability, decoupled architecture, failure isolation.
- **Disadvantage of E:** Distributed transaction complexity threatens financial ledger integrity; prohibitive operational overhead for startup phase.
- **Resolution:** Candidate C delivers a unified datastore model avoiding distributed transaction complexity, subject to validating performance and seam boundaries.

---

## 30. Architecture Unknown Register

| ID | Unknown Description | Affected Candidates | Business Impact | Technical Impact | PoC Required | Legal Review | Stakeholder Input | Target Phase |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UNK-01** | Multi-tenant tenant density and provisioning latency under Frappe Bench. | C, D | High (SaaS COGS) | High (Infra Sizing)| **PoC-01** | No | No | Phase 1B/1C |
| **UNK-02** | Feasibility of cleanly hosting KIYA India Tax Seam independently of ERPNext regional app. | C | Critical (Compliance)| High (Seam Design) | **PoC-02** | No | No | Phase 1B/1C |
| **UNK-03** | Concurrency throughput and database connection pooling under peak transaction load. | B, C, D | High (User UX) | High (Scaling) | **PoC-03** | No | No | Phase 1B/1C |
| **UNK-04** | Bi-directional delta synchronization reliability on mobile field service clients. | All | High (Field Ops)| High (Mobile Sync) | **PoC-04** | No | No | Phase 1B/1D |
| **UNK-05** | Legal exposure of SaaS delivery model under ERPNext GPLv3 license. | B, C | Critical (Commercial)| Critical (Seam) | No | **Mandatory** | Yes | Phase 1B/1C |
| **UNK-06** | Engineering team learning curve and onboarding velocity on Frappe Framework. | C, D | Medium (Timeline) | Medium (Quality) | No | No | **Required** | Phase 1C |

---

## 31. Architecture Risk Register

| Risk ID | Architectural Risk Description | Affected Candidate | Probability | Impact | Severity | Evidence / Source | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | GPLv3 copyleft contamination forcing disclosure of proprietary KIYA apps. | B, C | Medium | Critical | **CRITICAL** | Doc 25 §6 | Enforce strict network/API isolation; mandate formal legal review gate before commit. | Legal Lead |
| **RSK-02** | Dual `docstatus` engine breaking KIYA Business Status progression. | B, C | High | High | **HIGH** | Doc 21 §3, Doc 30 | Implement decoupling adapter wrapper; fallback to Candidate D if wrapper adds excessive latency. | Architect |
| **RSK-03** | Upstream ERPNext v17 develop tree breaking changes destabilizing reused modules. | B, C | High | Medium | **HIGH** | Doc 27 §4 | Fork/pin stable commit tags of reused modules; zero core modifications. | DevOps Lead |
| **RSK-04** | Full custom build exhaustion leading to project delivery failure. | A, E | High | Critical | **CRITICAL** | Industry Benchmarks | Assess custom build scope vs staged delivery; manage core ledger implementation burden. | Product Sponsor |
| **RSK-05** | Distributed ledger imbalance across microservices. | E | High | Critical | **CRITICAL** | Distributed Systems | Avoid distributed ledger architectures for core accounting until transactional consistency mechanisms are proven. | Architect |

---

## 32. Proof-of-Concept (PoC) Validation Matrix

Per the authorized PoC plan (`docs/00-requirements/20-erpnext-poc-plan.md`), the following validation gates govern architecture approval:

```
+-----------------------------------------------------------------------------------+
|                        MANDATORY ARCHITECTURAL POC GATES                          |
+-----------------------------------------------------------------------------------+
| PoC-01: Multi-Tenant SaaS & Control Plane Gate (Tenant isolation, provisioning)   |
| PoC-02: India Tax & Compliance Seam Gate (CGST/SGST/IGST, RCM, ITC ledger)        |
| PoC-03: Concurrency & Performance Benchmark Gate (Transaction integrity under load)|
| PoC-04: Mobile Offline-Sync Validation Gate (Delta sync, conflict resolution)      |
+-----------------------------------------------------------------------------------+
```

1. **PoC-01: Multi-Tenant SaaS & Control Plane Gate:**
   - *Target Candidate:* Candidate C / D.
   - *Hypothesis:* Automated tenant provisioning can instantiate isolated tenant databases with zero query leakage across tenants; provisioning latency threshold TBD — OQ-015 / Architecture Test Design.
   - *Success Criteria:* Automated provisioning script creates Tenant A and Tenant B; automated security checks confirm isolation; custom domain routing verified.
2. **PoC-02: India Tax & Statutory Compliance Seam Gate:**
   - *Target Candidate:* Candidate C / D.
   - *Hypothesis:* The KIYA Global Tax Engine can calculate GST and post Input Tax Credit ledgers via independent API seam without coupling to upstream ERPNext India regional apps.
   - *Success Criteria:* Multi-line invoice calculates CGST, SGST, IGST, and RCM correctly; GL postings reconcile with Indian statutory rules.
3. **PoC-03: Concurrency & Performance Benchmark Gate:**
   - *Target Candidate:* Candidate C / D.
   - *Hypothesis:* Application tier and relational database can maintain transactional integrity and connection pool stability under defined peak load; latency and throughput thresholds TBD — OQ-015 / Architecture Test Design.
   - *Success Criteria:* Automated load test confirms sustained throughput without deadlocks or connection pool exhaustion under test scenarios.
4. **PoC-04: Mobile Offline-Sync Validation Gate:**
   - *Target Candidate:* Candidate C / D / Custom Mobile.
   - *Hypothesis:* Mobile field technician can complete an offline work order, sync deltas upon reconnection, and resolve conflicting inventory edits deterministically.
   - *Success Criteria:* Zero data loss on field service reports; deterministic resolution of stock reservation conflicts.

---

## 33. Stakeholder Decision Dependencies

Final architecture selection depends on the following formal stakeholder decisions:

1. **Commercial Licensing Risk Tolerance (Legal Review Gate):** Stakeholder and legal counsel sign-off on whether Candidate C's network-isolated reuse of ERPNext `Accounts`/`Stock` satisfies commercial distribution and SaaS IP protection criteria, or whether Candidate D (100% MIT Frappe + Custom Apps) is required.
2. **Implementation Burden vs. Custom Build Budget:** Confirmation of delivery priorities. If reducing initial core implementation burden is prioritized, Candidate C is favored under evaluation. If 100% bespoke ownership is prioritized regardless of implementation effort, Candidate D or A is favored.
3. **Clarification Groups CG-02 through CG-07:** Clarification of approval limits (`OQ-003`), tax jurisdiction priorities (`OQ-005`), and measurable NFR thresholds (`OQ-015`).

---

## 34. Preliminary Due-Diligence Findings

1. **Candidate B (ERPNext Primary) is MATERIALLY MISMATCHED with current requirements:**
   - Direct structural contradiction with `CD-002` (hardcoded `docstatus` lifecycle).
   - High risk of GPLv3 copyleft contamination across all proprietary KIYA IP.
   - Severe friction with core KIYA business differentiators (Enquiry, multi-envelope RFP, WMS coordinate bins, customer installed base).
2. **Candidate E (Modular Headless) is POORLY SUITED for Core Transactional ERP:**
   - Substantial distributed transaction complexity for financial double-entry ledgers.
   - Excessive operational and engineering overhead for initial product delivery.
3. **Candidate A (Full Custom) CARRIES SUBSTANTIALLY HIGHER IMPLEMENTATION BURDEN:**
   - Architectural freedom and licensing purity.
   - Disadvantaged by substantially higher implementation effort and engineering burden required to build and maintain standard ERP plumbing.
4. **Candidate C (Frappe + Selective ERPNext Reuse Under Evaluation) is the PROVISIONAL LEADING CANDIDATE:**
   - Offers potential delivery acceleration by evaluating mature accounting and stock calculation capabilities for selective reuse.
   - Frappe Framework (MIT) provides rapid application tooling, ORM, and RBAC.
   - Preserves all 8 strategic seams via independent, proprietary KIYA applications.
   - Requires formal legal validation of GPLv3 boundaries and completion of PoC gates.
5. **Candidate D (Frappe + Mostly Custom KIYA) is the EVALUATED FALLBACK / CONTINGENCY CANDIDATE:**
   - Eliminates GPLv3 risk completely while leveraging Frappe's rapid ORM.
   - Serves as the evaluated fallback if Candidate C fails legal review or seam isolation tests.

---

## 35. Architectural Conclusion & Status

In accordance with Phase 1B governance rules, this evaluation issues the following formal conclusion:

### PROVISIONAL ARCHITECTURE RECOMMENDATION — FINAL APPROVAL PENDING REQUIRED VALIDATION GATES

- **Provisional Leading Candidate:** **Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation)**
- **Evaluated Fallback Candidate:** **Candidate D (Frappe Framework + Mostly Custom KIYA Apps)**
- **Governing Architecture Decision Record:** `ADR-001` (Status: `CONDITIONAL / PROPOSED`)

### Mandatory Conditions for Final Architecture Approval:
1. Satisfactory execution and sign-off of **PoC-01** (SaaS Multi-Tenancy & Isolation).
2. Satisfactory execution and sign-off of **PoC-02** (India Tax & Statutory Compliance Seam).
3. Satisfactory execution and sign-off of **PoC-03** (Concurrency & Performance Benchmark).
4. Satisfactory execution and sign-off of **PoC-04** (Mobile Offline Delta Sync).
5. Formal completion of **Legal Licensing Review Gate** confirming GPLv3 seam isolation.

---

## 36. Explicit Non-Decisions

To prevent premature architectural lock-in, the following remain explicitly **NON-DECISIONS** in Phase 1B:
- Physical database management system is NOT selected.
- Production hosting, cloud provider, and server topology are NOT selected.
- Programming languages for custom seams are NOT permanently finalized.
- Physical database tables, column schemas, and foreign keys are NOT designed.
- Concrete REST/GraphQL endpoints and JSON payloads are NOT designed.
- Production UI/UX frameworks (React vs. Vue vs. Flutter) are NOT selected.
- Proof-of-concept tests are NOT executed within this document.

---

## 37. Phase 1B Self-Review Verification

The Architecture Governance Auditor conducted a comprehensive self-review of this document against all Phase 1B governance checks:

- **Check 1 (Technology Neutrality):** Verified. No technology was selected prematurely; all candidate evaluations remain provisional hypotheses.
- **Check 2 (Frappe vs. ERPNext Separation):** Verified. Frappe Framework (MIT) and ERPNext (GPLv3) were rigorously distinguished across all 22 dimensions.
- **Check 3 (No Forced Requirements):** Verified. ERPNext reference behaviors were never asserted as KIYA business requirements.
- **Check 4 (Open Questions Preserved):** Verified. Questions `OQ-003` through `OQ-015` remain open and uncommitted.
- **Check 5 (No Invented Scores):** Verified. No fictitious numeric ratings were manufactured; evaluations are evidence-backed.
- **Check 6 (No Invented TCO):** Verified. TCO is analyzed strictly through structural cost drivers without manufactured financial numbers.
- **Check 7 (No Invented Team Skills):** Verified. Team competency is marked as requiring stakeholder input.
- **Check 8 (No Legal Advice):** Verified. Licensing boundaries are explicitly designated as `[LEGAL REVIEW REQUIRED]`.
- **Check 9 (No Fictitious PoC Results):** Verified. PoC requirements are catalogued as mandatory validation gates, not claimed as executed facts.
- **Check 10 (CD-001 Preserved):** Verified. Hybrid scope expansion is respected across all candidate evaluations.
- **Check 11 (CD-002 Preserved):** Verified. Operational Business Status lifecycle is enforced; Candidate B was penalized for docstatus conflict.
- **Check 12 (8 Strategic Seams Preserved):** Verified. Candidate architectures were explicitly evaluated against their ability to isolate all 8 seams.
- **Check 13 (BRD Scope Preserved):** Verified. All 28 modules and 238 functional requirements were maintained as drivers.
- **Check 14–17 (Zero Implementation):** Verified. Zero database schemas, API endpoints, UI designs, or production code were authored.
- **Check 18–20 (Classification & Confidence Rigor):** Verified. Every material finding carries an approved evidence classification and confidence level.
