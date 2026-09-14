# KIYA 360 — Phase 1 Validation & PoC Register

- **Document ID:** `ARCH-08`
- **Phase:** Phase 1 Governance — Validation, PoC & Legal Gates Register
- **Status:** `REVIEW-READY BASELINE`
- **Date:** 14 September 2026
- **Authors:** Principal Enterprise Architect, Solution Architect, Quality & Governance Lead
- **Governing Architecture:** `docs/02-architecture/04-target-architecture.md` (Phase 1C)
- **Decision Register:** `docs/02-architecture/07-phase-1-architecture-decision-register.md`
- **Open Questions Baseline:** `docs/00-requirements/06-open-questions.md`

---

## 1. Executive Summary & Purpose

This register formalizes the empirical validation requirements, technical Proof-of-Concept (PoC) initiatives, legal review gates, and stakeholder decision checkpoints required before architectural commitments are made in Phase 2.

In strict adherence to Phase 1 governance:
1. **Capability-Based Success Criteria:** Success criteria are defined by **demonstrated architectural capabilities and functional correctness**, rather than unvalidated performance figures or synthetic SLA targets.
2. **Definitive Legal Gatekeeping:** Legal and licensing interpretations are explicitly separated from architectural deductions and assigned to qualified legal counsel (`Gate L-01`).
3. **Traceability to Open Questions:** Every validation item directly addresses one or more open questions (`OQ-003` through `OQ-015`) using their exact Phase 0 definitions and scopes.

---

## 2. Technical Proof-of-Concept (PoC) Register

### PoC-01: Multi-Tenant SaaS Control Plane & Data Isolation Verification
- **PoC ID:** `PoC-01`
- **Target Seam:** Strategic Seams #1 (Product Boundaries) & #2 (SaaS Control Plane)
- **Affected Architecture Decision:** `ADR-001` (Provisional Platform Selection), `ADR-005` (Tenancy Model)
- **Related Requirements & Modules:** `SF-001` (Multi-Tenancy Context), `MOD-01` (Platform & Administration)
- **Objective:** Empirically validate automated tenant provisioning, database isolation, zero cross-tenant data leakage, and independent tenant backup/restoration using the Frappe site abstraction.
- **Hypothesis:** Frappe's multi-tenant site routing provides true database-per-tenant isolation with complete security enforcement, zero cross-site SQL query leakage, and programmatic lifecycle provisioning from an external control plane.
- **Evidence Required:**
  - Working script executing programmatic tenant provisioning (database creation, schema migration, admin initialization).
  - Automated security penetration test attempting cross-tenant record access via API, direct ORM queries, and background tasks.
  - Automated point-in-time backup and restore of Tenant A while Tenant B executes active transactions without interruption.
- **Capability-Based Success Criteria:**
  1. Automated provisioning succeeds without manual intervention.
  2. Zero cross-tenant data access under adversarial query injection.
  3. Independent tenant database backup and restore completes successfully with zero operational side-effects on peer tenants.
- **Failure Implication:** If cross-tenant leakage occurs or programmatic isolation fails, Candidate C tenancy is invalidated, triggering re-evaluation of Candidate A (Full Custom) or Candidate D (Clean-Room Custom).
- **Execution Phase:** Phase 2 (Architecture Validation Sprint)

---

### PoC-02: India Statutory Tax Engine & Real-Time E-Invoicing Verification
- **PoC ID:** `PoC-02`
- **Target Seam:** Strategic Seam #8 (India Statutory Compliance & Tax Engine)
- **Affected Architecture Decision:** `ADR-001` (Platform Architecture), Target Architecture Section 8
- **Related Requirements & Modules:** `MOD-18` (Tax & Statutory Compliance), `MOD-17` (Finance & Accounting)
- **Related Open Question:** `OQ-005` (Tax-country rule sets & statutory filing behavior)
- **Objective:** Verify end-to-end statutory compliance for India GST, including HSN/SAC determination, CGST/SGST/IGST calculation, Invoice Reference Number (IRN) generation, QR code embedding, and e-way bill payload generation.
- **Hypothesis:** An anti-corruption tax adapter can sit between operational sales dispatch workflows and the India GSTN/NIC sandbox, successfully generating compliant signed invoices without modifying upstream ERPNext source code.
- **Evidence Required:**
  - Successful generation of schema-compliant GST e-invoice JSON payloads matching official NIC specifications.
  - Successful mock/sandbox authentication, IRN registration, and retrieval of signed QR code.
  - Rendering of standard statutory tax invoice PDF containing signed QR code, IRN, and itemized tax breakout.
- **Capability-Based Success Criteria:**
  1. Accurate tax determination across intrastate, interstate, and SEZ transaction scenarios.
  2. Successful round-trip communication with statutory sandbox portal (or sandbox emulator).
  3. Complete isolation of tax logic within the KIYA-owned Global Tax Engine adapter.
- **Failure Implication:** If ERPNext's regional tax capabilities cannot be cleanly adapted or prove insufficient, KIYA must implement a clean-room custom tax calculation and e-invoicing service (`Candidate D` path).
- **Execution Phase:** Phase 2 (Architecture Validation Sprint)

---

### PoC-03: High-Concurrency Transactional Throughput & Resource Scaling
- **PoC ID:** `PoC-03`
- **Target Seam:** Core Platform Performance & Relational Persistence
- **Affected Architecture Decision:** `ADR-001`, `ADR-005`, `ADR-006`
- **Related Requirements & Modules:** `SF-015` (24/7 Scalable Operations), `MOD-28` (Audit, Security & Compliance)
- **Related Open Question:** `OQ-015` (Measurable availability, performance, scalability, and latency targets)
- **Objective:** Evaluate transaction throughput, database connection behavior, and background worker queue latency under simulated peak enterprise workloads (concurrent order entry, material dispatch, and GL posting).
- **Hypothesis:** A stateless application tier coupled with dedicated background workers and read replicas can handle high-volume enterprise transactions without database deadlocks or latency degradation.
- **Evidence Required:**
  - Automated load test scripts simulating concurrent user journeys across C2C, P2P, and A2S.
  - Latency distribution graphs for interactive API requests vs. background tasks.
  - Database telemetry showing connection pool utilization, CPU/memory saturation, and lock contention.
- **Capability-Based Success Criteria:**
  1. Transactional integrity maintained with zero dropped requests or unhandled database deadlocks.
  2. Interactive UI requests maintain responsive execution while heavy background workers process bulk jobs concurrently.
  3. Read-heavy reporting queries against read replicas cause zero lock contention on the primary transactional database.
- **Failure Implication:** If concurrency bottlenecks emerge within the framework's single-process model, architectural adjustments (such as asynchronous job queue expansion or connection pool tuning) will be mandated.
- **Execution Phase:** Phase 2 (Performance Benchmark Drill)

---

### PoC-04: Mobile Offline Synchronization & Deterministic Conflict Resolution
- **PoC ID:** `PoC-04`
- **Target Seam:** Strategic Seam #6 (User Experience, Client & Mobile Experience)
- **Affected Architecture Decision:** Target Architecture Section 14 (Mobile Architecture)
- **Related Requirements & Modules:** `SF-009` (Mobile Applications & Offline Sync), `MOD-27` (Mobile Application), `MOD-14` (Maintenance & Field Service)
- **Related Open Question:** `OQ-013` (Offline data scope, conflict resolution, synchronization behavior)
- **Objective:** Verify offline field transaction capture (Field Service Work Orders, spare parts issuance, technician notes, customer signatures) and deterministic bidirectional synchronization upon network restoration.
- **Hypothesis:** A mobile client utilizing local encrypted storage, client-generated UUIDs, and an outbox synchronization pattern can reliably synchronize operational updates to the core platform without data loss or unresolved state collisions.
- **Evidence Required:**
  - Mobile prototype capturing work order status updates and photo attachments in airplane mode.
  - Synchronous queue replay upon reconnecting to network.
  - Automated test simulating concurrent updates on mobile and web to verify deterministic conflict resolution rules.
- **Capability-Based Success Criteria:**
  1. 100% data preservation of offline mutations during simulated device restart or network drop.
  2. Idempotent ingestion of batched mutations at the API Gateway.
  3. Predictable conflict resolution (server-authoritative financial status overrides client; client notes append cleanly).
- **Failure Implication:** If generic mobile sync frameworks fail to handle complex ERP entity relationships, a specialized, domain-specific synchronization protocol must be specified in Phase 2.
- **Execution Phase:** Phase 2 (Mobile Architecture Drill)

---

## 3. Legal & Commercial Review Gates

### Gate L-01: Frappe (MIT) vs. ERPNext (GPLv3) Intellectual Property & Licensing Review
- **Gate ID:** `Gate L-01`
- **Status:** `MANDATORY PRE-COMMITMENT GATE` (Required prior to Phase 2 production code authoring)
- **Reviewing Authority:** Qualified Legal Counsel & Corporate Intellectual Property Advisor
- **Affected Architecture:** `ADR-001`, Strategic Seams #1, #3, #4, and #8
- **Core Legal Questions:**
  1. Does hosting a SaaS platform that utilizes Frappe Framework (MIT) alongside selective ERPNext core modules (GPLv3) trigger copyleft distribution obligations under standard commercial SaaS hosting?
  2. Does developing proprietary KIYA applications (such as the dedicated Enquiry engine, SaaS Control Plane, and custom UI) as separate Frappe apps constitute a "derivative work" of ERPNext under GPLv3, or are they legally independent under MIT/proprietary licensing?
  3. If anti-corruption adapters and API gateways mediate all communication between proprietary KIYA modules and ERPNext modules, does this provide adequate legal containment?
- **Consequence If Unresolved or Unfavorable:**
  - If legal counsel determines that selective ERPNext reuse imposes unacceptable licensing risks on KIYA's proprietary intellectual property, the project will immediately invoke **Candidate D (Frappe Framework + Clean-Room Custom KIYA Apps)** as the evaluated fallback option, building custom accounting and stock engines under pure MIT / proprietary ownership.

---

## 4. Stakeholder & Business Decision Gates

The following governance gates track unresolved business clarifications (`OQ-003` through `OQ-015`) requiring formal executive sign-off during Phase 2:

| Gate ID | Governing Open Question | Topic & Exact Phase 0 Subject | Stakeholder Authority | Impacted Architecture & Deferral Rationale | Current Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **STK-01** | `OQ-003` / `OQ-004` | **Approvals & Notifications:** Approval conditions, matrices, thresholds, escalation timing, delegation (`OQ-003`); notification triggers, channels, templates (`OQ-004`). | VP Sales, CCO, Head of Operations | Governs workflow escalation thresholds in `MOD-24` and notification triggers in `SF-006`. Safely deferred; shared workflow engine supports configurable threshold rules. | `OPEN / DEFERRED TO PHASE 2` |
| **STK-02** | `OQ-005` | **Tax-Country Scope & Statutory Filing:** Initial tax-country rule sets in scope beyond India and statutory filing behaviors (`OQ-005`). | Head of Tax & Compliance, CFO | Governs multi-country rule sets in `MOD-18`. Safely deferred; India tax engine implemented first via pluggable adapter. | `OPEN / DEFERRED TO PHASE 2` |
| **STK-03** | `OQ-006` | **Payroll & Statutory Calculations:** Payroll and statutory calculations required for India and reference country (`OQ-006`). | Head of HR, CFO | Governs salary structure formula rules in `MOD-19`. Safely deferred; formula engine designed to support dynamic components. | `OPEN / DEFERRED TO PHASE 2` |
| **STK-04** | `OQ-015` | **Formal Non-Functional SLAs:** Measurable availability, performance, scalability, security-monitoring, and latency targets defining NFRs (`OQ-015`). | Product Management & Executive Committee | Establishes quantitative pass/fail metrics for `PoC-03`. Safely deferred; architecture is designed for horizontal scaling. | `OPEN / DEFERRED TO PHASE 2` |

---

## 5. Conclusion & Handoff

The Validation, PoC, and Legal Gates Register establishes a rigorous empirical framework for testing all critical architectural hypotheses. By defining capability-based success criteria and formal review gates, Phase 1 guarantees that Phase 2 can proceed with controlled validation rather than unmanaged assumptions.
