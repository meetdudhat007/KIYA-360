# KIYA 360 — Phase 1 Architecture Decision Register

- **Document ID:** `ARCH-07`
- **Phase:** Phase 1 Governance — Consolidated Architecture Decision Register
- **Status:** `REVIEW-READY BASELINE`
- **Date:** 14 September 2026
- **Authors:** Principal Enterprise Architect, Solution Architect, Architecture Governance Lead
- **Governing Framework:** `docs/02-architecture/01-architecture-strategy-and-decision-framework.md`
- **Candidate Evaluation:** `docs/02-architecture/02-candidate-architecture-evaluation.md`
- **Decision Readiness:** `docs/02-architecture/03-architecture-decision-readiness.md`
- **ADR Repository:** `docs/02-architecture/adrs/`

---

## 1. Governance & Classification Rules

In strict compliance with Phase 1 governance principles:
1. **Zero Fabricated Approvals:** Only decisions backed by documented stakeholder sign-offs or approved Phase 0 clarification records (`CD-001`, `CD-002`, `DEC-001` through `DEC-013`) may be designated as `APPROVED`.
2. **Standardized Decision Status Taxonomy:**
   - `PROPOSED`: Formulated and under review by architecture governance.
   - `CONDITIONAL`: Formulated with explicit pre-conditions, pending technical PoC or legal gate resolution.
   - `PROVISIONAL`: Currently favored baseline direction, subject to empirical validation.
   - `APPROVED`: Fully authorized by the Architecture Governance Board and Executive Committee.
   - `DEFERRED`: Intentionally postponed to Phase 2 due to open business questions or lack of empirical data.
   - `REJECTED`: Formally evaluated and rejected with documented evidence.
   - `SUPERSEDED`: Replaced by a subsequent approved architectural decision.
3. **Decision Confidence Taxonomy:**
   - `HIGH`: Fully supported by authoritative source documents, established software engineering standards, and complete requirements traceability.
   - `MEDIUM`: Conceptually sound and supported by candidate analysis, but requires empirical benchmarking or legal review.
   - `LOW`: Feasible option, but heavily dependent on unvalidated external variables or unresolved open questions.

---

## 2. Consolidated Architecture Decision Register

### ADR-001: Provisional Platform Architecture Selection: Frappe Framework + Selective ERPNext Core Reuse Under Evaluation with Clean-Room Custom Fallback
- **ADR Reference:** [`docs/02-architecture/adrs/ADR-001-provisional-platform-architecture.md`](file:///c:/Users/Admin/Desktop/KIYA360/docs/02-architecture/adrs/ADR-001-provisional-platform-architecture.md)
- **Status:** `PROPOSED / CONDITIONAL`
- **Decision Confidence:** `MEDIUM` (Supported by extensive repository codebase analysis; conditioned on PoC-01, PoC-02, and Legal Gate L-01).
- **Context:** KIYA 360 requires rapid delivery across all 28 modules, strict statutory tax compliance, and double-entry financial integrity, while maintaining long-term IP ownership and avoiding unmaintainable ERP coupling.
- **Decision:** Provisionally adopt **Candidate C** (Frappe Framework + Selective ERPNext Core Modules) as the leading architectural direction for Phase 1 target architecture and PoC validation, with **Candidate D** (Frappe + Clean-Room Custom KIYA Apps) as the evaluated fallback / contingency option.
- **Alternatives Considered:**
  - *Candidate A (Full Custom):* Maximum IP control, but extreme engineering overhead for standard ERP accounting plumbing.
  - *Candidate B (ERPNext-Primary Monolith):* High coupling, inability to support dedicated Enquiry natively, rigid DocType submission models clashing with `CD-002`.
  - *Candidate D (Frappe + Custom Apps):* Evaluated fallback, requires bespoke development of double-entry ledger and inventory valuation.
  - *Candidate E (Modular Headless / API-First Architecture):* Distributed transaction overhead and eventual-consistency complexities for core double-entry accounting.
- **Key Evidence:** Inspected ERPNext codebase demonstrates mature General Ledger, Stock Ledger, and Manufacturing BOMs. Inspected Frappe framework provides multi-tenant site routing and metadata ORM.
- **Consequences:** Selective capability reuse remains under evaluation; requires strict anti-corruption adapters and mandatory legal review of GPLv3 vs MIT boundaries (`Gate L-01`).
- **Risks & Reversibility:** Framework coupling risk (mitigated by Seams #1 and #3); high reversibility via anti-corruption adapter layer.
- **Dependencies:** `CD-001`, `CD-002`, `PoC-01`, `PoC-02`, Gate `L-01`.
- **Related Requirements:** All 28 BRD modules (`MOD-01` to `MOD-28`), `SF-001` through `SF-015`.
- **Related Open Questions:** `OQ-005` (Tax Scope), `OQ-007` (Inventory Rules), `OQ-015` (NFR Targets).

---

### ADR-002: Authoritative Single-Source Master Data Registry Model
- **ADR Reference:** `ADR-002` (Baseline Documented in Phase 1C / Phase 1D)
- **Status:** `PROPOSED` (Aligned with Approved Decision `DEC-007`)
- **Decision Confidence:** `HIGH` (Directly traces to BRD Section 10 and Approved Decision `DEC-007`).
- **Context:** Enterprise operations require consistent Customer, Supplier, Item, Facility, and Account records across front-office, supply chain, and back-office domains without data duplication or synchronization drift.
- **Decision:** Establish an Authoritative Master Data Registry where each core enterprise entity has exactly one conceptual domain owner (e.g., Customer owned by CRM/Sales, Supplier by Supplier Management, Item by Inventory, Chart of Accounts by Finance & Accounting). Duplicate entity stores are strictly prohibited.
- **Alternatives Considered:**
  - *Independent Module Datastores with Async Sync:* High risk of synchronization lag, split-brain data, and reconciliation overhead.
  - *Centralized Master Data Management (MDM) Hub via Message Bus:* Excessive operational complexity for single-platform architecture.
- **Key Evidence:** Phase 0 Traceability Matrix, BRD Universal Master Data mandate (`BRD §10`).
- **Consequences:** Eliminates master data reconciliation; guarantees real-time consistency across C2C, P2P, and A2S flows; conceptual ownership does not mandate physical schema fragmentation.
- **Risks & Reversibility:** Requires strict domain boundary discipline during schema authoring; moderate reversibility.
- **Dependencies:** `DEC-007`, `SF-001`, `SF-003`, `SF-004`.
- **Related Requirements:** `DR-C2C-001`, `DR-P2P-001`, `SF-001` through `SF-004`.
- **Related Open Questions:** None (Governed by approved decision).

---

### ADR-003: Decoupled Operational Business Status Lifecycle Architecture
- **ADR Reference:** `ADR-003` (Baseline Documented in Phase 1C Section 6)
- **Status:** `PROPOSED` (Aligned with Approved Decision `CD-002`)
- **Decision Confidence:** `HIGH` (Directly implements approved business clarification `CD-002`).
- **Context:** Operational documents require rich, multi-state commercial lifecycles reflecting actual business milestones. Standard framework submission models enforce rigid binary submitted/draft states (`docstatus`) that do not reflect real-world execution.
- **Decision:** Decouple operational business lifecycles from technical database submission flags. Every transactional document will maintain an explicit, first-class `business_status` attribute governed by the Shared Workflow Engine (`SF-005` / `MOD-24`) and logged in the Immutable Audit Ledger (`SF-008` / `MOD-28`). Exact status taxonomies and transition rules will be defined progressively during detailed functional design.
- **Alternatives Considered:**
  - *Inherit ERPNext docstatus (0=Draft, 1=Submitted, 2=Cancelled):* Rejected by approved decision `CD-002` as overly restrictive.
  - *Ad-hoc String Status per Module:* Inconsistent terminology, broken cross-module status reporting.
- **Key Evidence:** Approved Clarification Decision `CD-002`, BRD Section 4 Business Flows.
- **Consequences:** Uniform cross-module status tracking; complete visibility for Customer 360 and Executive dashboards; requires adapter mapping if ERPNext core modules are reused.
- **Risks & Reversibility:** Low risk; high reversibility.
- **Dependencies:** `CD-002`, `SF-005`, `SF-008`.
- **Related Requirements:** All transactional requirements across C2C, P2P, and A2S.
- **Related Open Questions:** `OQ-003` (Approval conditions & limits).

---

### ADR-004: Anti-Corruption Framework Insulation & Strategic Seams
- **ADR Reference:** `ADR-004` (Baseline Documented in Phase 1A Section 7 and Phase 1E Section 8)
- **Status:** `PROPOSED`
- **Decision Confidence:** `HIGH` (Standard enterprise architecture practice for commercial software reusability).
- **Context:** If open-source or commercial components (such as ERPNext core modules) are evaluated for reuse, direct tight coupling threatens KIYA's long-term intellectual property ownership, upgradeability, and strategic independence.
- **Decision:** Enforce eight inviolable KIYA-owned Strategic Seams (Product Boundaries, SaaS Control Plane, API Gateway, AI Governance, BI/EPM, UX/Mobile, Security/Audit, Tax Compliance). Proprietary KIYA business domains must communicate with underlying framework engines exclusively through formal anti-corruption adapters. Direct upstream core modifications are strictly forbidden.
- **Alternatives Considered:**
  - *Direct Extension of Upstream Code:* Severe technical debt; breaks upstream upgradeability; risks IP contamination.
  - *Total Avoidance of Reuse (Candidate A):* Forfeits delivery velocity advantages on standard accounting.
- **Key Evidence:** Architectural Strategy (`ARCH-01`), Candidate Evaluation (`ARCH-02`).
- **Consequences:** Guarantees zero upstream modifications; ensures upstream security patches can be applied seamlessly; enables clean replacement of any reused module in the future.
- **Risks & Reversibility:** Minor initial adapter development overhead; high reversibility.
- **Dependencies:** `ARCH-01`, `ADR-001`, `PoC-01`.
- **Related Requirements:** `SF-001`, `SF-008`, `MOD-18`, `MOD-24`.
- **Related Open Questions:** None.

---

### ADR-005: Multi-Tenant Operational Isolation Topology
- **ADR Reference:** `ADR-005` (Baseline Documented in Phase 1C Section 11 and Phase 1E Section 4)
- **Status:** `PROVISIONAL / SUBJECT TO BENCHMARKING`
- **Decision Confidence:** `MEDIUM` (Supported by SaaS security standards and Frappe multi-tenant benchmarks; subject to `PoC-01` and `PoC-03`).
- **Context:** Enterprise clients require strict data segregation, zero risk of cross-tenant data leakage, independent backup/restore capability, and predictable performance.
- **Decision:** Database-per-tenant is a provisional tenancy topology under evaluation as the default baseline, governed by an independently owned SaaS Control Plane. The platform maintains architectural abstraction to permit pooled shared-database tenancy for lower-tier tenants if dictated by commercial infrastructure review.
- **Alternatives Considered:**
  - *Single Shared Database with Row-Level Security (RLS):* Lower hosting cost, but higher blast radius and complex single-tenant restore.
  - *Dedicated Virtual Machines per Tenant:* Extreme infrastructure cost and operational sprawl.
- **Key Evidence:** Phase 1B Evaluation of Candidate C, Frappe multi-tenant site architecture inspection.
- **Consequences:** Maximum data protection; independent tenant point-in-time recovery; requires automated database migration pipelines across tenant instances.
- **Risks & Reversibility:** Database connection overhead at high tenant scale; high reversibility via database abstraction layer.
- **Dependencies:** `SF-001`, `PoC-01`, `PoC-03`.
- **Related Requirements:** `SF-001` (Multi-Tenancy Foundation), `MOD-01`.
- **Related Open Questions:** `OQ-015` (Measurable NFR Targets including Concurrency & Sizing).

---

### ADR-006: Asynchronous Decoupling of Intelligence, Analytics & Background Workloads
- **ADR Reference:** `ADR-006` (Baseline Documented in Phase 1C Section 12/13 and Phase 1E Section 5)
- **Status:** `PROPOSED`
- **Decision Confidence:** `HIGH` (Standard pattern to protect OLTP database performance).
- **Context:** High-frequency transaction processing (Sales Orders, Invoices, Dispatches) must maintain responsive performance and must not be degraded by heavy analytical aggregations, PDF generation, or AI inference.
- **Decision:** Segregate operational OLTP compute from analytical (BI/EPM), generative AI, and asynchronous background worker tiers. Heavy reporting queries execute against read replicas or analytical marts. Non-blocking tasks are queued to dedicated worker pools. Exact performance targets remain subject to `OQ-015` and Phase 2 benchmarking.
- **Alternatives Considered:**
  - *Run All Reports & Jobs in Main App Thread:* Causes database lockups, high latency, and frequent user timeouts during month-end closes.
  - *Full Event Sourcing & CQRS Everywhere:* Unnecessary architectural complexity for standard operational ERP modules.
- **Key Evidence:** Phase 1C Target Architecture, Quality Attribute Evaluation (`ARCH-01`).
- **Consequences:** Protects interactive UI responsiveness; isolates failures in third-party integrations from blocking user transactions.
- **Risks & Reversibility:** Requires background worker queue monitoring; high reversibility.
- **Dependencies:** `SF-008`, `SF-006`, `MOD-22`, `MOD-23`, `MOD-25`.
- **Related Requirements:** `MOD-22`, `MOD-23`, `MOD-25`, `SF-006`.
- **Related Open Questions:** `OQ-015` (NFR Performance Benchmarks).

---

## 3. Decision Register Summary Table

| ADR ID | Decision Title | Status | Confidence | Governing Requirements | Impacted Domains | Validation Gate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ADR-001** | Provisional Platform Architecture (Frappe + Selective Core Reuse) | `PROPOSED / CONDITIONAL` | `MEDIUM` | All 28 Modules, `CD-001`, `CD-002` | Universal Platform | `PoC-01`, `PoC-02`, Gate `L-01` |
| **ADR-002** | Authoritative Single-Source Master Data Registry Model | `PROPOSED` | `HIGH` | `DEC-007`, `SF-001`-`SF-004` | Universal Platform | Architecture Review |
| **ADR-003** | Decoupled Operational Business Status Lifecycle Architecture | `PROPOSED` | `HIGH` | `CD-002`, `SF-005`, `SF-008` | C2C, P2P, A2S | Workflow Engine Drills |
| **ADR-004** | Anti-Corruption Framework Insulation & Strategic Seams | `PROPOSED` | `HIGH` | `ARCH-01`, `SF-001`, `MOD-18` | 8 Strategic Seams | Seam Isolation Audit |
| **ADR-005** | Multi-Tenant Operational Isolation Topology (DB-per-Tenant) | `PROVISIONAL` | `MEDIUM` | `SF-001`, Quality Attributes | SaaS Control Plane | `PoC-01`, `PoC-03` |
| **ADR-006** | Asynchronous Decoupling of Intelligence, BI & Background Jobs | `PROPOSED` | `HIGH` | `MOD-22`-`25`, `SF-006` | Analytics, AI, Workers | Performance Benchmarking |

---

## 4. Conclusion & Next Steps

This consolidated decision register formalizes the architectural baseline for KIYA 360. All decisions are documented with explicit evidence, rigorous risk assessments, and defined validation gates, maintaining absolute compliance with governance rules and setting up Phase 2 technical execution.
