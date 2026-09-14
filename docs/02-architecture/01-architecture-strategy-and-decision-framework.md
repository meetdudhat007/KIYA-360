# KIYA 360 — Architecture Strategy, Principles & Decision Framework

## 1. Document Control & Governance

- **Document ID:** `01-architecture-strategy-and-decision-framework`
- **Phase:** Phase 1 — Platform Architecture & System Design (Sub-phase 1A)
- **Status:** Approved Architecture Governance Framework
- **Date:** 14 September 2026
- **Author:** Senior Enterprise Solutions Architect & Architecture Governance Lead
- **Primary Business Source:** `source/KIYA360_BRD.pdf` (Version 2.0, 13 September 2026)
- **Approved Phase 0 Baseline:** `docs/00-requirements/36-phase-0-completion-assessment.md` (and Docs `01`–`35`)
- **Approved Stakeholder Decisions:** `CD-001` (Hybrid Scope Expansion), `CD-002` (Operational Business Status Model), `DEC-001`–`DEC-013`
- **Classification System Applied:** `[REQUIREMENT-INHERITED]`, `[ARCHITECTURE-PRINCIPLE]`, `[ARCHITECTURE-CONSTRAINT]`, `[ARCHITECTURE-HYPOTHESIS]`, `[REFERENCE-EVIDENCE]`, `[ASSUMPTION]`, `[OPEN QUESTION]`, `[DEFERRED DECISION]`

---

## 2. Phase 1 Purpose & Boundaries

### 2.1 Mission of Phase 1
`[ARCHITECTURE-PRINCIPLE]` The mission of Phase 1 is to define a robust, scalable, secure, and commercially viable technical architecture for the KIYA 360 platform, strictly derived from approved business requirements, and to evaluate candidate delivery strategies using empirical, evidence-based methods.

### 2.2 What Phase 1A Establishes
- Architectural drivers and constraints derived directly from BRD v2.0 and the Phase 0 requirements baseline.
- Foundational architecture principles across enterprise data, transaction processing, security, multi-tenancy, APIs, AI, mobile, and workflow.
- Quality-attribute framework defining system behaviors, operational guarantees, and identification of non-functional metrics requiring future quantification.
- Candidate architecture evaluation framework and decision criteria.
- PoC validation gates and legal/commercial governance boundaries.
- Architecture Decision Record (ADR) process and risk management rules.

### 2.3 Strict Out-of-Scope Boundaries for Phase 1A
`[ARCHITECTURE-CONSTRAINT]` Phase 1A is a strategic framing and governance exercise. To prevent premature architectural lock-in, the following activities are strictly prohibited during Phase 1A:
- Selecting a final platform or implementation stack (e.g., Frappe vs. Full Custom).
- Selecting specific database management systems (e.g., PostgreSQL, MariaDB, MongoDB).
- Selecting specific programming languages or runtime environments.
- Selecting specific frontend/backend frameworks or cloud infrastructure providers.
- Designing physical database schemas, table definitions, or database indexes.
- Designing concrete API endpoints, payloads, or message broker schemas.
- Writing application code or implementing proof-of-concept scripts.
- Resolving unresolved stakeholder business open questions (`OQ-003` through `OQ-015`).

---

## 3. Source-of-Truth Hierarchy

`[ARCHITECTURE-PRINCIPLE]` All architectural reasoning, design trade-offs, and technology evaluations must strictly respect the following six-level authority hierarchy:

1. **Current Approved BRD:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026) — Ultimate business authority.
2. **Approved Phase 0 Requirements Baseline:** `docs/00-requirements/` (Docs `01` through `36`) — Authoritative functional and foundation baseline.
3. **Approved Stakeholder Clarification Decisions:** `.kiya/AI-DECISIONS.md` (`CD-001`, `CD-002`, `DEC-001`–`DEC-013`) — Legally binding stakeholder approvals.
4. **Phase 1 Architecture Governance Decisions (ADRs):** Formal architecture decisions approved under this framework.
5. **Reverse-Engineering & Reference Material:** `docs/00-requirements/21`–`27` (ERPNext v17 analysis) — Empirical reference benchmark only; not a direct specification.
6. **General Industry Patterns & Best Practices:** Engineering conventions, design patterns, and platform documentation.

`[ARCHITECTURE-CONSTRAINT]` A lower-level source must never silently override, weaken, or reinterpret a higher-level requirement or decision.

---

## 4. Architecture Scope

`[REQUIREMENT-INHERITED]` The architectural surface of KIYA 360 encompasses all 28 business modules and 238 functional requirement records defined in BRD v2.0:
- **Commercial & CRM:** Lead Management (01), Customer Opportunity (02), Quotation & Sales Order (03), Marketing Campaign (04), Customer Service / Helpdesk (05).
- **Supply Chain & Operations:** Supplier Management (06), Procurement (07), Inventory (08), Warehouse Management / WMS (09), Logistics & Dispatch (10), Discrete Manufacturing (11), Quality Management (12).
- **Service & Asset Management:** Corporate Asset Management (13), Field Service Management (14).
- **Projects & Delivery:** Project Management (15).
- **Financial Suite:** General Ledger & Accounting (16), Accounts Receivable (17), Accounts Payable (18), Cash & Bank (19), Multi-Currency & Global Accounting (20), Tax Governance & Regulatory Compliance (21).
- **Human Resources:** HR & Payroll (22).
- **Digital Channels & Content:** E-Commerce & Customer Portal (23), Document Management System / DMS (24).
- **Analytics & Orchestration:** Business Intelligence & Analytics (25), Enterprise Performance Management / EPM (26), Workflow Automation (27), AI Integration & Machine Learning (28).
- **Cross-Cutting Shared Foundations:** Shared Platform Foundations `SF-001` through `SF-015` (Docs `13` and `34`).

---

## 5. Business Architecture Drivers

`[REQUIREMENT-INHERITED]` The architecture must fulfill specific high-level enterprise business objectives articulated in BRD v2.0:

1. **Unified Enterprise Suite:** Eliminate operational silos by providing a single, seamless platform spanning CRM, ERP, SCM, Field Service, HR, and Analytics.
2. **End-to-End Flow Continuity:** Execute unbroken, auditable business lifecycles across Customer-to-Cash (C2C), Procure-to-Pay (P2P), and Asset-to-Service (A2S).
3. **Multi-Entity & Global Expansion:** Support multi-company, multi-branch, multi-currency, and multi-tax jurisdictions within a single enterprise tenant.
4. **Compliance & Audit Rigor:** Maintain immutable audit trails, strict accounting integrity, separation of duties, and statutory tax compliance (including Indian GST and e-invoicing capabilities).
5. **Commercial Multi-Tenant SaaS Model:** Deliver a multi-tenant subscription offering with zero inter-tenant data leakage, rapid provisioning, and centralized operational control.
6. **AI-Assisted Operational Efficiency:** Embed predictive, assistive, and automated AI capabilities directly into operational workflows without compromising data privacy or governance.
7. **Mobile & Field Workforce Enablement:** Empower distributed field technicians, sales representatives, and warehouse staff with mobile and offline capabilities.

---

## 6. Architecture Drivers & Constraints

### 6.1 Functional Architecture Drivers
- `[REQUIREMENT-INHERITED]` **28-Module Cross-Functional Coupling:** Requires an architecture that balances deep cross-module data propagation (e.g., Sales Order → Production → Dispatch → Invoice → General Ledger) with domain modularity to prevent catastrophic regressions.
- `[REQUIREMENT-INHERITED]` **Single Master Data Authority:** Universal, non-duplicated master data for Customers, Suppliers, Items/Products, Employees, and Chart of Accounts (`DEC-007`).
- `[REQUIREMENT-INHERITED]` **Transactional Integrity:** Double-entry financial balancing, immutable ledger postings, strict stock valuation (FIFO/Moving Average), and 3-way matching validation.

### 6.2 Architectural Constraints (Non-Negotiable)
- `[ARCHITECTURE-CONSTRAINT]` **CD-001 Hybrid Model:** C2C, P2P, and A2S must be implemented strictly to detailed business flow specifications. ERP-standard conventions may be used as references for standard non-specified capabilities, but ERPNext behavior is not an automatic specification.
- `[ARCHITECTURE-CONSTRAINT]` **CD-002 Operational Business Status:** System transaction lifecycles must be governed by operational business statuses reflecting actual business milestones. ERPNext's dual technical `docstatus` integers (0, 1, 2) are explicitly rejected as a user-facing or architectural model.
- `[ARCHITECTURE-CONSTRAINT]` **The 8 Mandatory KIYA-Owned Strategic Seams:** The architecture must enforce clean, proprietary KIYA architectural seams isolating:
  1. Product & Domain Boundaries
  2. SaaS Control Plane (Tenant Provisioning, Billing, Quotas)
  3. API Gateway & External Integrations
  4. AI Governance & Orchestration
  5. Enterprise BI & EPM Analytical Engine
  6. Modern UX & Mobile Client Experience
  7. Enterprise Security, RBAC & Audit Ledger
  8. Statutory Tax & Regulatory Compliance Engine
- `[ARCHITECTURE-CONSTRAINT]` **Licensing Isolation (GPLv3 vs. Proprietary):** ERPNext is licensed under GPLv3. Where copyleft components are considered, the architecture must provide clear component boundaries that support an appropriate commercial and licensing structure, subject to formal legal review. Architectural isolation does not itself constitute a legal conclusion.

---

## 7. Architecture Quality Attributes (NFR Framework)

`[REQUIREMENT-INHERITED]` Quality attributes represent critical architectural drivers. In accordance with anti-hallucination governance, unquantified targets from the BRD are catalogued with current evidence and flagged as `[TBD]` pending resolution of `OQ-015`.

| Quality Attribute | Architectural Significance for KIYA 360 | BRD Driver | Current Evidence / Known Facts | Unknown / Target Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Availability** | System must support 24/7 continuous enterprise operations, warehouse dispatches, and field services. | BRD §8.1 NFR-AVL-001 | High availability required for SaaS operations; failover must prevent data corruption. | Target SLA percentage (e.g., 99.9% vs 99.99%) is `[TBD / OQ-015]`. |
| **Reliability & Recoverability** | Zero transactional data loss during unexpected crashes; defined RPO and RTO. | BRD §8.1 NFR-REL-001 | Financial transactions require strict transactional integrity, rollback safety, and point-in-time recovery. Specific transaction technology and recovery strategy remain subject to architecture evaluation. | Target RPO/RTO time thresholds are `[TBD / OQ-015]`. |
| **Scalability** | Must support growing transaction volumes across 28 modules and expanding multi-tenant user bases. | BRD §8.1 NFR-SCL-001 | Architecture must support workload scaling across operational tiers; scaling strategy (horizontal, read-distribution, or partitioning) remains an evaluation option `[ARCHITECTURE-HYPOTHESIS]`. | Peak concurrent users, tenant limits, and daily transaction volumes are `[TBD / OQ-015]`. |
| **Performance** | Responsive transaction processing for standard operational screens; efficient report generation without blocking core operations. | BRD §8.1 NFR-PRF-001 | Operational UI must not freeze during heavy background processing (e.g., MRP runs or bulk billing). | P95/P99 latency thresholds and background job SLAs are `[TBD / OQ-015]`. |
| **Data Integrity & Consistency** | Financial ledgers, stock balances, and tax calculations must never diverge. | BRD §7.16, §7.17, §7.21 | Single entry points for GL and Stock postings; double-entry balance check mandatory. | Zero tolerance for ledger imbalance; fully quantified audit rules established in Phase 0. |
| **Security & Privacy** | Enterprise RBAC, multi-tenant isolation, data encryption, and role segregation. | BRD §7.28, §8.1 NFR-SEC-001 | Tenant data leakage is catastrophic; role permissions must operate at entity, record, and field levels. | Specific external certification targets (SOC 2, ISO 27001) are `[TBD]`. |
| **Auditability** | Complete historical lineage of every transactional state change, user action, and approval. | BRD §7.27, §7.28, SF-008 | Immutable audit log required for all financial, inventory, and administrative actions. | Fully required; log retention duration policy is `[TBD / OQ-015]`. |
| **Maintainability & Extensibility** | Rapid deployment of new vertical modules, client custom workflows, and API connectors. | BRD §7.27, §8.1 | Modular architecture mandatory; core platform must be upgradeable without breaking customizations. | Upgrade cadence and backward compatibility policies established in Section 8. |
| **Interoperability** | Bidirectional integration with e-commerce, payment gateways, tax portals, and legacy systems. | BRD §7.23, SF-012 | Contract-governed API and webhook capabilities required; payload formats and protocols subject to architecture evaluation. | Specific third-party protocol mandates are `[TBD]`. |
| **Mobile & Offline Resilience** | Mobile apps for sales, inventory, and field technicians operating in low/no connectivity environments. | BRD §6.3, §7.14, SF-009 | Local caching, delta sync, and robust conflict resolution required. | Maximum offline duration and conflict resolution heuristics are `[TBD]`. |

---

## 8. Core Architecture Principles

`[ARCHITECTURE-PRINCIPLE]` The following 22 principles govern all architectural choices in KIYA 360:

1. **Business-First Architecture:** Architecture exists to deliver business value, compliance, and end-to-end flow continuity, not to showcase technology trends.
2. **Unified Enterprise Data Model:** One conceptual data model for core enterprise entities across all 28 modules. No duplicate, conflicting customer, supplier, or item records (`DEC-007`).
3. **Single Source of Truth for Master Data:** Every shared master concept must have a clearly defined authoritative ownership boundary and canonical source of truth. The exact application/service ownership structure will be established during domain architecture.
4. **Modular Domain Ownership:** System capabilities are grouped into logical, cohesive domains with clearly defined interface contracts.
5. **Explicit Cross-Module Contracts:** Cross-module communication (e.g., Sales Order triggering Purchase Order or Production) must occur via explicit, documented interfaces or events.
6. **Strict Financial & Accounting Consistency:** Financial and inventory operations must preserve transactional integrity and prevent inconsistent or partially posted business states. Specific transaction technology and implementation strategy remain subject to architecture evaluation.
7. **KIYA Ownership of Strategic Seams:** The 8 strategic seams must remain proprietary to KIYA, fully decoupled from third-party or open-source internal frameworks.
8. **No Unnecessary Vendor Lock-in:** Core platform services must avoid proprietary cloud-vendor primitives where standard open alternatives exist.
9. **Component Replaceability:** External components (payment gateways, notification providers, LLM models, tax engines) must be abstracted behind swappable adapter interfaces.
10. **Security & Privacy by Design:** Least privilege by default; defense-in-depth; robust authentication and isolation across multi-tenant boundaries; protection of data at rest and in transit.
11. **Immutable Auditability by Design:** Every business-critical state transition, authorization, and override must emit an immutable, tamper-evident audit record.
12. **Failure Isolation:** Failure of a peripheral module (e.g., Marketing analytics, AI assistant, or external notification gateway) must never halt core transactional processing (billing, dispatch, order taking).
13. **Observability by Design:** Structured logging, distributed tracing, metrics, and health endpoints must be built into all architectural layers from day one.
14. **Offline-First for Edge & Mobile:** Mobile clients for Field Service and Warehouse operations must treat network disconnections as normal operational states.
15. **Configuration Over Hardcoding:** Business rules, approval limits, tax rates, workflow stages, and notification templates must be runtime-configurable.
16. **Explicit API Governance & Versioning:** Public and inter-domain APIs must be contract-governed, versioned, backward-compatible, secure, and independently evolvable. Specific API protocols and versioning mechanisms remain deferred for architecture evaluation `[DEFERRED DECISION]`.
17. **Backward Compatibility & Safe Upgrades:** Platform schema migrations and system upgrades must be automated, repeatable, and non-destructive to existing tenant data.
18. **Testability at All Levels:** Architecture must support automated unit, integration, contract, and end-to-end regression testing in isolated test environments.
19. **Operational Simplicity:** Avoid architectural over-engineering. Favor proven, maintainable patterns over highly distributed microservice topologies unless scaling demands it.
20. **Evidence-Based Technology Selection:** No technology, library, or platform may be chosen based on preference or hype; selection requires objective evaluation against criteria and empirical PoC results.
21. **Decoupled Application State [ARCHITECTURE-HYPOTHESIS]:** Business application logic should minimize in-memory session coupling to facilitate scaling and operational resilience, subject to evaluation of candidate runtimes.
22. **Decoupled Analytical & Operational Workloads:** Heavy reporting, analytical queries, and EPM driver simulations must not degrade operational transaction processing performance. Workload isolation mechanisms remain subject to evaluation.

---

## 9. Enterprise Data Architecture Principles

`[ARCHITECTURE-PRINCIPLE]` Data architecture must ensure coherence, relational integrity, and strict separation of concerns without physical table commitments at this stage:

### 9.1 Master Data Governance
- Core masters (**Customer, Supplier, Item/Product, Warehouse, Employee, Chart of Accounts**) have a single authoritative definition (`DEC-007`).
- Master data entities support polymorphic and role-based extensions (e.g., an Entity can act simultaneously as a Customer and a Supplier, sharing base tax and legal identities while maintaining separate credit and payable ledgers).

### 9.2 Mandatory Domain Disambiguations
- `[REQUIREMENT-INHERITED]` **Customer Installed Base ≠ Corporate Financial Fixed Asset:**
  - *Customer Installed Base* (governed under A2S / Module 14): Represents customer-owned equipment located at client sites, associated with warranties, AMC contracts, maintenance schedules, and field service history.
  - *Corporate Fixed Asset* (governed under Module 13 / Finance): Represents enterprise-owned capital assets, capitalized on the balance sheet, subject to asset classes, depreciation schedules, revaluation, and financial disposal.
  - The data model must strictly maintain separate entity structures for these concepts.
- `[REQUIREMENT-INHERITED]` **Field Service Work Order ≠ Manufacturing Production Work Order:**
  - *Field Service Work Order (`DR-A2S-005`):* Technician dispatch, customer site arrival, diagnostic checklists, on-site labor hours, and truck-stock spare parts consumption.
  - *Manufacturing Work Order (`FR-MFG-003`):* Discrete shop-floor production, Bill of Materials (BOM) multi-level explosion, machine routing, scrap tracking, and WIP ledger accounting.
  - These are completely distinct transactional entities with separate schemas, lifecycles, and accounting effects.

### 9.3 Financial Data Rigor
- Double-entry accounting is enforced at the transaction boundary: Total Debits must equal Total Credits per posting.
- Posted General Ledger entries and Stock Ledger entries are strictly immutable. Corrections must be executed via reversal entries and credit/debit notes, never in-place database updates.

### 9.4 Multi-Entity & Organizational Context
- Every transaction record must carry explicit organizational context: `Tenant ID`, `Company ID`, `Branch / Cost Center ID`, `Currency ID`, and `Tax Jurisdiction ID`.

---

## 10. Cross-Module Transaction Architecture

`[ARCHITECTURE-PRINCIPLE]` Cross-module flows represent the operational backbone of KIYA 360. The architecture must enforce strict boundaries between synchronous transactional consistency and asynchronous event orchestration:

```
+-----------------------------------------------------------------------------------+
|                           SYNCHRONOUS TRANSACTIONAL CORE                          |
|  (Transactional Integrity Boundaries: Validation, Document State, Ledger Postings)|
+-----------------------------------------+-----------------------------------------+
                                          | Emits Domain Event
                                          v
+-----------------------------------------------------------------------------------+
|                 ASYNCHRONOUS EVENT & WORKFLOW ORCHESTRATION                       |
|                 [ARCHITECTURE-HYPOTHESIS / CANDIDATE PATTERN]                     |
|  (At-Least-Once Delivery, Idempotent Processing, Eventual Notification & BI Sync) |
+-----------------------------------------------------------------------------------+
```

### 10.1 Flow Transaction Boundaries
1. **Customer-to-Cash (C2C):**
   - *Synchronous Core:* Sales Order reservation check; Delivery Note inventory deduction and COGS posting; Sales Invoice tax calculation and AR/GL ledger accrual; Payment Entry AR reconciliation.
   - *Asynchronous Propagation:* Lead conversion notifications; quotation PDF generation; dispatch tracking updates; customer portal status reflection.
2. **Procure-to-Pay (P2P):**
   - *Synchronous Core:* Goods Receipt warehouse quantity increase and stock accrual; Supplier Invoice 3-way match validation, tax calculation, and AP/GL liability posting; Payment AP clearing.
   - *Asynchronous Propagation:* RFQ distribution to supplier portal; supplier scorecard recalculation; automated reorder suggestions.
3. **Asset-to-Service (A2S):**
   - *Synchronous Core:* Service Work Order spare parts inventory issuance from technician truck stock; Service Invoice billing and AR posting.
   - *Asynchronous Propagation:* SLA escalation timers; technician GPS routing; customer satisfaction surveys; maintenance history analytics update.

### 10.2 Reliability & Idempotency Rules
- `[ARCHITECTURE-PRINCIPLE]` All cross-module service interfaces and event consumers must enforce **idempotency safeguards** to prevent duplicate financial postings, duplicate dispatches, or duplicate payments during network retries.
- `[ARCHITECTURE-PRINCIPLE]` Cross-module failures must execute controlled compensation logic or explicit document rejection states; partial half-posted transactions are prohibited.

---

## 11. SaaS & Multi-Tenancy Architecture Principles

`[ARCHITECTURE-PRINCIPLE]` Multi-tenancy is an essential commercial requirement for KIYA 360. The architecture framework establishes strict governance for tenant isolation, lifecycle, and administration without pre-selecting the physical tenancy implementation:

### 11.1 Tenancy Isolation & Security Mandates
- **Absolute Tenant Isolation:** Zero possibility of cross-tenant data access. Every query, cache lookup, file storage path, background task, and search index must be scoped by verified tenant context.
- **Tenant Context Injection:** Tenant identity must be derived securely from authenticated session tokens at the API Gateway layer, never accepted as an unverified client request parameter.

### 11.2 Tenancy Architecture Evaluation Options [ARCHITECTURE-HYPOTHESIS / EVALUATION OPTIONS]
The following candidate tenancy patterns represent evaluation options for subsequent phases; none is pre-selected as approved architecture:
1. **Option 1: Database-per-Tenant [EVALUATION OPTION]:** Physical database isolation per tenant; evaluated for security, compliance, and infrastructure overhead.
2. **Option 2: Schema-per-Tenant [EVALUATION OPTION]:** Shared database engine with isolated schema namespaces per tenant; evaluated for isolation and connection management.
3. **Option 3: Shared Database / Discriminator Column with Row-Level Security [EVALUATION OPTION]:** Shared tables with strict row-level isolation policies; evaluated for density and operational complexity.
4. **Option 4: Site / Virtual Multi-Tenancy [EVALUATION OPTION]:** Application-level site partitioning (e.g., virtual tenant tenancy in candidate frameworks); evaluated for scaling and lifecycle control.

`[DEFERRED DECISION]` Physical tenancy model selection is deferred to Phase 1B/1C, subject to empirical evaluation in `PoC-01` (SaaS Control Plane & Multi-Tenancy).

---

## 12. Security & Compliance Architecture Principles

`[ARCHITECTURE-PRINCIPLE]` Security must be built into the architectural foundation:

### 12.1 Authentication & Identity
- Centralized identity verification through modern, standardized token-based mechanisms.
- Native multi-factor authentication (MFA) support for privileged and administrative roles `[ARCHITECTURE-PRINCIPLE]`.
- Pluggable enterprise Single Sign-On (SSO) support for enterprise tenants. Specific protocols (e.g., SAML 2.0, OIDC) remain candidate integration options `[EVALUATION OPTION / DEFERRED DECISION]`.

### 12.2 Role-Based & Attribute-Based Access Control (RBAC / ABAC)
- Multi-tier authorization:
  - *Functional Role:* What modules/features a user can access (e.g., Sales Manager, Billing Clerk).
  - *Organizational Scope:* Which Company, Branch, or Cost Center a user has access to.
  - *Record-Level Permission:* Document ownership, department scoping, or customer territory assignment.
  - *Field-Level Security:* Masking sensitive fields (e.g., salary, bank account details, profit margins).

### 12.3 Cryptographic Standards & Secrets Management
- All data in transit must be protected using industry-standard secure transport protocols `[ARCHITECTURE-PRINCIPLE]`.
- Sensitive data at rest (passwords, payment tokens, API keys, statutory tax credentials) must be encrypted using strong cryptographic standards. Specific algorithms and key management technologies remain deferred `[DEFERRED DECISION]`.
- Zero hardcoded secrets, database passwords, or private keys in source code or configuration files.

---

## 13. Integration & API Principles

`[ARCHITECTURE-PRINCIPLE]` KIYA 360 must serve as an extensible enterprise platform:

1. **API Gateway Seam:** All client applications (Web, Mobile, External Systems, Portal) access backend services via the KIYA API Gateway seam `[ARCHITECTURE-CONSTRAINT]`.
2. **Contract-First Design:** Public APIs must be defined by formal machine-readable schemas before implementation `[ARCHITECTURE-PRINCIPLE]`.
3. **Robust Lifecycle & Versioning:** Public APIs must be contract-governed, versioned, backward-compatible, secure, and independently evolvable. Specific API protocols (e.g., REST, GraphQL, gRPC) and versioning mechanisms remain deferred for architecture evaluation `[DEFERRED DECISION]`.
4. **Rate Limiting & Abuse Prevention:** Per-tenant and per-user traffic controls to protect system availability `[ARCHITECTURE-PRINCIPLE]`.
5. **Webhook Architecture:** Webhook integrations must provide authenticity, integrity, replay protection, retry handling, and observability. Specific cryptographic signing mechanisms (e.g., HMAC) and delivery infrastructure (e.g., dead-letter queueing) remain subject to architecture evaluation `[EVALUATION OPTION / DEFERRED DECISION]`.
6. **External System Failure Isolation:** Third-party integration calls (e.g., shipping carriers, payment processors, SMS gateways) must be isolated to prevent external latency or failures from impacting core transaction processing. Failure isolation mechanisms (e.g., asynchronous queuing, circuit breakers) remain candidate implementation patterns `[ARCHITECTURE-HYPOTHESIS]`.

---

## 14. AI Architecture & Governance Principles

`[REQUIREMENT-INHERITED]` AI is an embedded platform capability across Lead Scoring, Predictive Maintenance, Cash Flow Forecasting, and Natural Language Assistance. The architecture must govern AI responsibly:

```
+-----------------------------------------------------------------------------------+
|                           KIYA AI GOVERNANCE SEAM                                 |
|  (Tenant Data Masking, Policy Enforcement, Rate Limiting, Audit Logging)          |
+-----------------------------------------+-----------------------------------------+
                                          | Sanitized Request
                                          v
+-----------------------------------------------------------------------------------+
|                        PLUGGABLE AI PROVIDER ADAPTER                              |
|  (Local SLM / Enterprise LLM / Specialized Heuristic Models / Cost Optimizer)     |
+-----------------------------------------------------------------------------------+
```

1. **Strict Data Boundary & Zero Leakage:** Tenant proprietary business data must never be used to train public models. Request payloads sent to external models must be sanitized and scoped strictly to the calling tenant.
2. **Model & Provider Neutrality:** The platform must not be locked into a single AI vendor. AI capabilities must sit behind an abstraction layer allowing swappable backends (e.g., commercial API providers or self-hosted open models).
3. **Human-in-the-Loop by Default:** AI recommendations (e.g., approving a credit override, dispatching a high-value purchase order, or altering a ledger classification) must require human confirmation. AI cannot autonomously execute irreversible financial transactions without explicit configuration.
4. **Explainability & Auditing:** Every AI-generated score, recommendation, or draft must record the model identifier, prompt context hash, and confidence score in the audit log.
5. **Graceful Fallback:** If AI services are unavailable or latency exceeds thresholds, the platform must seamlessly fall back to deterministic business heuristics without breaking operational workflows.

---

## 15. Mobile & Edge Architecture Principles

`[REQUIREMENT-INHERITED]` Mobile enablement is vital for Field Service (`Module 14`), Warehouse WMS (`Module 09`), and Field Sales (`Module 01/03`):

1. **Native Client Experience:** Mobile applications must provide responsive, ergonomic, touch-friendly interfaces tailored to handheld devices and barcode scanners.
2. **Offline-First Data Architecture:**
   - Local storage on the device holds necessary working sets (e.g., assigned work orders, customer site details, local truck stock inventory, product price lists).
   - Read/write operations succeed locally during network disconnection.
3. **Bi-directional Delta Synchronization:**
   - On network reconnection, only modified records (deltas) are transmitted.
   - Server-side timestamp and version checks enforce deterministic conflict resolution (e.g., server-wins for inventory reservation; technician-wins for on-site diagnostic checklists; manual escalation for concurrent edits).
4. **Secure Local Caching:** Client-side local data storage on mobile devices must be encrypted and subject to remote wipe capability upon employee deactivation `[ARCHITECTURE-PRINCIPLE]`. Specific embedded storage technologies remain deferred `[DEFERRED DECISION]`.

---

## 16. BI & Enterprise Performance Management (EPM) Principles

`[REQUIREMENT-INHERITED]` BI (`Module 25`) and EPM (`Module 26`) require deep analytical power across all 28 modules:

1. **Workload Separation:** Heavy analytical aggregations, financial consolidations, and multi-scenario forecast models must not run directly against the primary operational transaction database in production.
2. **Read-Optimized Projections [ARCHITECTURE-HYPOTHESIS]:** Analytical queries may be served via read-optimized projections, analytical snapshots, or a dedicated reporting store to protect transactional performance. Exact data pipeline technology remains deferred `[DEFERRED DECISION]`.
3. **Canonical Semantic Metric Definitions:** Financial metrics (EBITDA, Gross Margin, DSO, DPO, Working Capital) and operational metrics (OTIF, MTTR, Scrap Rate) must have a single authoritative definition in the platform to prevent conflicting dashboard numbers.
4. **Tenant-Scoped Analytics:** Multi-tenant isolation applies fully to the analytics tier; cross-tenant data aggregation is strictly restricted to anonymized platform telemetry if authorized.

---

## 17. Document Management System (DMS) Principles

`[REQUIREMENT-INHERITED]` DMS (`Module 24`) manages transactional attachments, contracts, drawings, and tax invoices:

1. **Decoupled Binary Storage:** Document binaries (PDFs, images, scans) must be stored in specialized, cost-effective object/file storage, never as raw BLOBs in the transactional relational database.
2. **Metadata & Relational Linkage:** Document metadata (hash, MIME type, size, version, uploader, access ACL, linked business entity) resides within the relational data model.
3. **Content Integrity:** Documents associated with posted financial records (e.g., signed Delivery Notes, Supplier Tax Invoices, signed Contracts) must be tamper-evident using cryptographic hashing mechanisms. Specific hashing algorithms and storage providers remain deferred `[DEFERRED DECISION]`.
4. **Tenant Storage Partitioning:** Object storage paths and access policies must enforce strict tenant-level isolation.

---

## 18. Workflow & Automation Architecture Principles

`[REQUIREMENT-INHERITED]` Automated workflows, approvals, and escalations (`MOD-24` and `SF-005`) must utilize a unified platform engine:

1. **Single Workflow Engine:** A unified workflow engine governs approvals, state transitions, and business notifications across all 28 modules (preventing separate, fragmented approval logic in Sales, Procurement, and HR).
2. **Business Status Alignment:** Workflow transitions drive the `CD-002` operational business status model.
3. **Configurable Escalation & Delegation:** Approval rules must support dynamic hierarchies (manager approval, department head approval, threshold-based routing, out-of-office delegation) without code modification.
4. **State Machine Determinism:** Workflow transitions must be deterministic; invalid state transitions must be rejected with descriptive error codes and audited.

---

## 19. Candidate Architecture Categories

`[ARCHITECTURE-HYPOTHESIS]` To ensure rigorous, unbiased evaluation during Phase 1B, the following five candidate architectural archetypes are formally recognized:

| Category | Description | Core Premise | Strategic Trade-off |
| :--- | :--- | :--- | :--- |
| **A. Full Custom Architecture** | Purpose-built modern web architecture (e.g., custom frontend, custom backend services, relational DB, custom SaaS control plane). | Maximum control, zero legacy baggage, perfect alignment with KIYA 8 seams, no copyleft licensing risks. | Highest initial build effort, longer time-to-market, team must build standard ERP plumbing from scratch. |
| **B. ERPNext-Primary Architecture** | Deploy standard ERPNext v17 as the core foundation, extending it via custom apps and standard hooks. | Maximum out-of-the-box functional coverage, rapid early demo capability. | Extreme vendor lock-in, GPLv3 legal risk, technical docstatus friction (`CD-002`), UI/UX rigidity, difficult SaaS multi-tenancy control. |
| **C. Frappe Framework + Selective ERPNext** | Utilize Frappe Framework as the rapid application engine; selectively reuse proven ERPNext domain modules while building custom apps for KIYA seams. | Reuses robust metadata engine and standard accounting/stock plumbing; isolates proprietary KIYA apps. | GPLv3 boundary management required; Python single-thread performance constraints; tightly coupled docstatus engine. |
| **D. Frappe Framework + Mostly Custom KIYA Apps** | Utilize Frappe Framework strictly as an application runtime/ORM, but author proprietary KIYA business applications for all core modules. | Leverages Frappe's rapid ORM, auth, and schema tooling while avoiding ERPNext legacy workflows and GPLv3 dependencies. | Requires authoring 28 modules on Frappe ORM; still carries framework-level constraints and MariaDB coupling. |
| **E. Modular Headless Services (Polyglot / API-First)** | Decoupled modular backend services communicating via an event broker and unified API gateway, with a clean independent frontend. | High scalability, failure isolation, best-of-breed technology per domain (e.g., high-performance financial ledger). | Operational complexity, higher distributed systems overhead, requires robust DevOps and coordination. |

`[ARCHITECTURE-CONSTRAINT]` No candidate is selected in Phase 1A. All candidates remain hypotheses until evaluated against formal criteria and empirical PoC results.

---

## 20. Architecture Option Evaluation Framework

`[ARCHITECTURE-PRINCIPLE]` Candidate architectures will be evaluated across 22 objective dimensions grouped into five strategic pillars:

```
+-----------------------------------------------------------------------------------+
|                        KIYA 360 ARCHITECTURE SCORECARD                            |
+-----------------------------------------------------------------------------------+
| 1. Functional & Flow Completeness (BRD Coverage, C2C/P2P/A2S, Seams, Status)     |
| 2. Architectural Quality & Rigor (Data Model, Tenancy, Security, Scalability)     |
| 3. Technology & Operational Fit (Maintainability, Observability, Mobile, Upgrade) |
| 4. Commercial, Legal & Strategic Freedom (GPLv3 Isolation, IP Ownership, Lock-in) |
| 5. Delivery Viability & Cost (Time-to-Market, Team Skills, Dev Cost, Reversibility)|
+-----------------------------------------------------------------------------------+
```

### 20.1 Evaluation Dimensions
1. **BRD 28-Module Coverage:** Out-of-the-box fit vs. development delta.
2. **Core Flow Fidelity:** Native support for C2C, P2P, and A2S without painful workarounds.
3. **Data Model Control:** Ability to enforce `DEC-007` (single unified master data, disambiguated assets and work orders).
4. **Business Status Lifecycle Fit:** Native support for `CD-002` without fighting hardcoded framework status integers.
5. **KIYA Strategic Seams Decoupling:** Ease of cleanly isolating the 8 mandatory KIYA-owned seams.
6. **Multi-Tenant SaaS Viability:** Architecture's capability to deliver secure, scalable multi-tenancy.
7. **Security & RBAC Granularity:** Field-level, record-level, and role-based permissions capability.
8. **Performance & Concurrency:** Throughput under peak enterprise transactional load.
9. **Scalability & Resource Efficiency:** Horizontal and vertical scaling cost profile.
10. **Mobile & Offline Capability:** Feasibility of integrating native mobile clients with offline sync.
11. **AI Integration Flexibility:** Ability to embed AI seamlessly across workflows.
12. **BI & Analytics Separation:** Capability to run reporting without impacting operational OLTP performance.
13. **API & Integration Maturity:** Clean REST/Webhook APIs with strong contract management.
14. **Operational Complexity:** Deployment, monitoring, backup, and infrastructure overhead.
15. **Upgradeability & Extensibility:** Ability to upgrade platform components without breaking tenant customizations.
16. **Vendor & Platform Lock-In:** Risk of becoming trapped in an inflexible third-party ecosystem.
17. **Licensing & Legal Risk:** Exposure of proprietary IP to GPLv3 copyleft contamination.
18. **Time to Market:** Speed of delivering initial production-ready releases.
19. **Team Competency & Hiring:** Availability and cost of engineering talent for the technology stack.
20. **Development & Maintenance Cost:** Total Cost of Ownership (TCO) over a 5-year horizon.
21. **Reversibility & Migration:** Cost and difficulty of migrating away if the foundation fails.
22. **Empirical Evidence Maturity:** Degree to which performance and feasibility claims are backed by verifiable tests.

`[REFERENCE-EVIDENCE]` Prior scores recorded in Documents `18` and `19` are classified strictly as preliminary reference benchmarks. Final scoring will occur in Phase 1B following PoC executions.

---

## 21. Proof-of-Concept (PoC) & Evidence Governance

`[ARCHITECTURE-PRINCIPLE]` Architectural commitments must be backed by empirical test evidence. Per the authorized PoC plan (`docs/00-requirements/20-erpnext-poc-plan.md`), the following validation gates must be executed before final platform approval:

1. **PoC-01: Multi-Tenant SaaS & Control Plane Gate:**
   - *Hypothesis Tested:* Candidate platform can support multi-tenant provisioning, tenant isolation, and custom branding without manual server configuration.
   - *Evidence Required:* Automated tenant provisioning script, verification of zero cross-tenant query leakage, tenant-specific schema/database separation metrics.
2. **PoC-02: India Tax & Statutory Compliance Seam Gate:**
   - *Hypothesis Tested:* The platform can host the KIYA proprietary Global Tax Engine and India GST e-invoicing seam cleanly without being tied to upstream ERPNext regional app changes.
   - *Evidence Required:* Working calculation of CGST/SGST/IGST and RCM with Input Tax Credit ledger generation on multi-line invoices via independent API.
3. **PoC-03: Concurrency & Performance Benchmark Gate:**
   - *Hypothesis Tested:* The platform architecture meets response time and concurrency thresholds under simulated multi-user operational load.
   - *Evidence Required:* Automated load test results recording P95 response times, database connection pool behavior, and CPU/memory utilization.
4. **PoC-04: Mobile Offline-Sync Validation Gate:**
   - *Hypothesis Tested:* Bi-directional delta synchronization and conflict resolution can reliably sync field service work orders.
   - *Evidence Required:* Working offline edit, reconnection sync, and conflict resolution test script.

`[ARCHITECTURE-CONSTRAINT]` No candidate architecture may be declared the approved platform without passing its required PoC validation gates.

---

## 22. Legal & Commercial Governance Gates

`[ARCHITECTURE-CONSTRAINT]` Architecture decisions must protect the commercial viability and intellectual property of KIYA 360:

1. **Open Source Licensing Audit:**
   - *Frappe Framework:* MIT License (Permissive — allows commercial use, closed-source derivative works, and custom extensions).
   - *ERPNext:* GNU General Public License v3 (GPLv3) (Strong Copyleft — derivative works or combined works distributed to third parties may be required to disclose source code under GPLv3).
2. **Legal Review Gate:**
   - Prior to committing to any architecture that includes ERPNext code reuse, a formal legal review must evaluate the commercial and licensing structure of the SaaS delivery model.
   - Where copyleft components are considered, the architecture must provide clear component boundaries that support an appropriate commercial and licensing structure, subject to formal legal review. Architectural isolation does not itself constitute a legal conclusion.
3. **Commercial IP Protection:**
   - Proprietary workflow definitions, AI models, custom industry modules, and SaaS control-plane software must reside strictly in proprietary KIYA repositories with clear copyright headers.

---

## 23. Architecture Decision Governance Model

`[ARCHITECTURE-PRINCIPLE]` Architecture governance will operate via a lightweight, auditable Architecture Decision Record (ADR) framework:

### 23.1 Architecture Decision Record (ADR) Lifecycle
```
[PROPOSED] ---> [UNDER REVIEW] ---> [APPROVED] ---> [SUPERSEDED]
                      |
                      v
                 [REJECTED]
```

- **PROPOSED:** Authored by an architect; documents context, problem statement, options considered, and proposed decision.
- **UNDER REVIEW:** Subject to stakeholder review, technical evaluation, and PoC evidence gathering.
- **APPROVED:** Formally approved by the Architecture Lead and Product Sponsor. Becomes binding project architecture.
- **REJECTED:** Decided against with documented rationale preserved.
- **SUPERSEDED:** Replaced by a subsequent approved ADR (must explicitly cite the superseding ADR ID).

### 23.2 ADR Canonical Template
Every ADR created in Phase 1 must include:
1. Title and Sequential Identifier (`ADR-###`)
2. Governance Status and Date
3. Context and Problem Statement
4. Requirements Traceability (BRD FRs, SFs, DEPs cited)
5. Decision Drivers & Quality Attributes Affected
6. Options Considered (Pros, Cons, Risks for each)
7. Decision Made & Justification
8. Consequences (Positive, Negative, Neutral)
9. PoC Evidence & Validation Reference
10. Compliance with the 8 KIYA Strategic Seams

### 23.3 Architecture Risk & Assumption Management
- All architectural assumptions must be recorded in the Architecture Assumptions Register.
- All technical risks must be catalogued in the Architecture Risk Register with severity, probability, mitigation strategy, and owner.

---

## 24. Architectural Risks, Assumptions & Constraints

### 24.1 Architecture Constraints Summary
- `[ARCHITECTURE-CONSTRAINT]` Strict compliance with BRD v2.0 and approved Phase 0 requirements baseline.
- `[ARCHITECTURE-CONSTRAINT]` Strict enforcement of `CD-001` (hybrid model) and `CD-002` (operational business status).
- `[ARCHITECTURE-CONSTRAINT]` Mandatory physical separation of Customer Installed Base vs. Corporate Fixed Assets.
- `[ARCHITECTURE-CONSTRAINT]` Mandatory isolation of the 8 KIYA-owned strategic seams.
- `[ARCHITECTURE-CONSTRAINT]` No proprietary vendor lock-in for core enterprise data.

### 24.2 Architecture Assumptions
- `[ASSUMPTION]` Enterprise clients will require multi-entity corporate structures (multiple subsidiaries operating under a consolidated parent company).
- `[ASSUMPTION]` Production deployments will utilize containerized cloud infrastructure or managed enterprise virtual infrastructure.
- `[ASSUMPTION]` The primary database workload will remain heavily relational, requiring strong transactional integrity and rollback protection for financial and inventory operations.

### 24.3 Architecture Risks
- `[ARCHITECTURE-HYPOTHESIS]` **Risk AR-01 (Framework Inflexibility):** Reusing an existing ERP framework may impose rigid metadata conventions, slow query generators, or opinionated docstatus models that conflict with KIYA requirements.
  - *Mitigation:* Thorough execution of PoC-01, 02, and 03; strict architectural seam decoupling.
- `[ARCHITECTURE-HYPOTHESIS]` **Risk AR-02 (Copyleft Contamination):** Utilizing GPLv3-licensed components could introduce commercial licensing ambiguity.
  - *Mitigation:* Formal legal review; network-isolated API architecture.
- `[ARCHITECTURE-HYPOTHESIS]` **Risk AR-03 (Custom Architecture Delivery Delay):** Choosing a 100% custom architecture from scratch could delay time-to-market and exhaust engineering bandwidth on generic accounting plumbing.
  - *Mitigation:* Objective evaluation of hybrid reuse (e.g., candidate D or headless kernels) in Phase 1B.

---

## 25. Deferred Decisions

`[DEFERRED DECISION]` The following technical decisions are intentionally deferred to subsequent Phase 1 sub-phases:

1. **Target Platform / Foundation Selection:** Deferred to Phase 1B/1C (pending candidate evaluation and PoC evidence).
2. **Primary Database Engine:** Deferred to Phase 1C (pending data architecture and performance benchmarks).
3. **Programming Language & Service Runtimes:** Deferred to Phase 1C (pending component architecture).
4. **Physical Tenancy Topology (DB-per-tenant vs. Schema vs. RLS):** Deferred to Phase 1B/1C (pending PoC-01).
5. **Frontend Application Framework (Web & Mobile):** Deferred to Phase 1D (pending UX architecture).
6. **Message Broker / Event Mesh Technology:** Deferred to Phase 1C (pending integration architecture).
7. **Cloud Hosting / Infrastructure Provider:** Deferred to Phase 1E (pending deployment architecture).

---

## 26. Phase 1A Self-Review & Governance Verification

The Architecture Governance Lead performed a comprehensive self-review of this document against all governing baselines:

1. **BRD v2.0 Compliance:** Verified. All 28 modules, 238 functional requirements, and core business flows (C2C, P2P, A2S) are fully incorporated as drivers.
2. **CD-001 Compliance:** Verified. The hybrid model is explicitly established as an architectural constraint. ERP-standard behavior remains reference-only.
3. **CD-002 Compliance:** Verified. Operational Business Status is enshrined as the sole platform lifecycle model; ERPNext's dual `docstatus` integers are rejected.
4. **Preservation of Open Questions:** Verified. Questions `OQ-003` through `OQ-015` remain explicitly open and unresolved; quality attribute targets are flagged as `[TBD / OQ-015]`.
5. **The 8 Strategic Seams:** Verified. All 8 KIYA-owned seams are preserved as architectural constraints.
6. **Zero Code / Design / Platform Lock-in:** Verified. No database engines, programming languages, frontend/backend frameworks, API payloads, or schemas were selected.
7. **Classification Integrity:** Verified. Material architecture decisions and hypotheses are classified; explanatory prose and tables are governed by the classification of their containing section.

---

## 27. Phase 1B Entry Criteria

`[ARCHITECTURE-PRINCIPLE]` Transition from Phase 1A to Phase 1B (Candidate Evaluation & Trade-off Analysis) is authorized only when:

1. Phase 1A document (`01-architecture-strategy-and-decision-framework.md`) is approved and sealed.
2. Project tracking records (`PROJECT-STATE.md`, `AI-HANDOFF.md`, `AI-CHANGELOG.md`) are synchronized.
3. Phase 1A governance framework has been reviewed and accepted as the working evaluation framework. Material business decisions discovered during architecture evaluation continue to require appropriate stakeholder approval.
4. Authorization is granted to execute Phase 1B candidate evaluation, scoring, and PoC preparation.

