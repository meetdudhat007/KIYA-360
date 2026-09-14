# Architecture Decision Record: ADR-001

# Provisional Platform Architecture Selection: Frappe Framework + Selective ERPNext Core Reuse Under Evaluation with Clean-Room Custom Fallback

- **ADR ID:** `ADR-001`
- **Title:** Provisional Platform Architecture Selection: Frappe Framework + Selective Core Reuse Under Evaluation with Fallback to Custom Apps
- **Status:** `PROPOSED / CONDITIONAL`
- **Date:** 14 September 2026
- **Authors:** Senior Enterprise Solutions Architect & Architecture Governance Lead
- **Deciders:** KIYA Executive Committee, Architecture Governance Board, Information Security Lead
- **Primary Business Source:** `source/KIYA360_BRD.pdf` (Version 2.0, 13 September 2026)
- **Evaluation Baseline:** `docs/02-architecture/02-candidate-architecture-evaluation.md`
- **Readiness Baseline:** `docs/02-architecture/03-architecture-decision-readiness.md`

---

## 1. Context & Problem Statement

KIYA 360 is a unified, multi-tenant CRM + ERP platform encompassing 28 distinct modules, 238 functional requirements, and three end-to-end mission-critical business flows (Customer-to-Cash, Procure-to-Pay, Asset-to-Service). 

The platform requires:
1. Strict financial correctness (double-entry general ledger, immutability, automated reversing entries, multi-currency valuation).
2. Deep Indian statutory tax compliance (GST e-invoicing, e-way bill generation, real-time ITC reconciliation).
3. Flexible, 8-state operational business status tracking (`CD-002`) independent of binary database submission flags.
4. Complete control over 8 strategic seams (Product Boundaries, SaaS Control Plane, API Gateway, AI Governance, BI/EPM, UX/Mobile, Security/Audit, Tax Compliance).
5. Enterprise multi-tenancy with strict data isolation, zero leakage, and independent tenant lifecycle management.
6. Faster delivery velocity without compromising long-term platform reversibility or intellectual property ownership.

Five candidate architectural archetypes were evaluated in Phase 1B:
- **Candidate A:** Full Custom Architecture (Custom Backend + Custom Frontend)
- **Candidate B:** ERPNext-Primary Architecture (Monolithic ERPNext Adaptation)
- **Candidate C:** Frappe Framework + Selective ERPNext Core Modules (Accounts, Stock Ledger)
- **Candidate D:** Frappe Framework + Mostly Custom KIYA Applications (Clean-room custom accounting)
- **Candidate E:** Modular Headless / API-First Microservices Architecture

A strategic architectural foundation must be provisionally established to guide Target Architecture Definition (Phase 1C) while respecting essential empirical and legal gates.

---

## 2. Requirements Traceability

This decision directly traces to and is governed by:
- **BRD Modules:** All 28 modules (`MOD-01` through `MOD-28`).
- **Core Business Flows:**
  - `DR-C2C-001` through `DR-C2C-016` (Customer-to-Cash Lifecycle)
  - `DR-P2P-001` through `DR-P2P-012` (Procure-to-Pay Lifecycle)
  - `DR-A2S-001` through `DR-A2S-014` (Asset-to-Service Lifecycle)
- **Shared Foundation Requirements:** `SF-001` through `SF-015` (Multi-Company Context, Access Control, Unified Master Data, Shared Workflow Engine, Audit Trail, Mobile Sync, AI Insights, Real-Time Dashboards, Numbering Engine, Common Record Capabilities).
- **Approved Architectural Decisions:**
  - `CD-001`: Hybrid Scope Expansion (BRD-Required vs. Derived Foundation).
  - `CD-002`: Transactional Lifecycle Business Status (Operational status != `docstatus`).
  - `DEC-007`: Unified Master Data Entities (Customer, Supplier, Item, Facility).
  - `DEC-009`: Financial Posting Immutability and Reversing Entries.

---

## 3. Options Considered

1. **Option A (Full Custom Stack):** Build 100% bespoke microservices/monolith from scratch using modern enterprise stacks (e.g., modular application runtimes and relational datastores under evaluation).
2. **Option B (ERPNext Monolithic Customization):** Adopt upstream ERPNext as the primary platform and heavily customize DocTypes.
3. **Option C (Frappe Framework + Selective ERPNext Core):** Build upon the MIT-licensed Frappe Framework; evaluate selective reuse of battle-tested, non-differentiating ERPNext capabilities (identifying General Ledger, Stock Ledger, Chart of Accounts as potential reuse candidates under evaluation); build all differentiating and KIYA-specific modules as bespoke, proprietary Frappe applications.
4. **Option D (Frappe Framework + Mostly Custom KIYA Apps):** Build upon Frappe Framework; write custom clean-room accounting and stock ledgers; strictly avoid all GPLv3 ERPNext code.
5. **Option E (Modular Headless Microservices):** Build independent domain services with headless API boundaries and independent datastores.

---

## 4. Evaluation Evidence Summary

- **Option B (Unfavorable):** Materially mismatched with current KIYA requirements due to direct conflict with `CD-002` (hardcoded binary `docstatus` cannot model KIYA 8-state lifecycles), absence of 40%+ BRD workflows (no Enquiry, no multi-envelope RFP, no coordinate WMS, no Field Service), and GPLv3 copyleft exposure across proprietary IP.
- **Option E (Poorly Suited for Core ERP):** Distributed transactions (2PC / sagas) across double-entry general ledger, inventory valuation, and procurement introduce substantial consistency risks and operational overhead.
- **Option A (Substantially Higher Implementation Burden):** Provides 100% IP ownership and absence of GPLv3 copyleft constraints, but rebuilding foundational ledger edge cases, multi-currency valuation, and tax engines requires substantially higher implementation effort.
- **Option C (Provisional Leading Candidate):** Offers potential delivery acceleration and verified financial ledger algorithms by evaluating mature accounting engines for selective reuse while maintaining clean app boundaries for KIYA IP.
- **Option D (Evaluated Fallback):** Retains rapid metadata productivity while eliminating all GPLv3 copyleft exposure if legal review rejects ERPNext reuse.

---

## 5. Decision: Conditional Provisional Recommendation

The KIYA 360 Architecture Governance Board adopts **Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation)** as the **PROVISIONAL ARCHITECTURE FOUNDATION**, with **Candidate D (Frappe Framework + Mostly Custom KIYA Apps)** designated as the **EVALUATED ARCHITECTURAL FALLBACK**.

### Nature of Approval:
This decision is strictly **PROVISIONAL / CONDITIONAL**. Final architecture approval and permission to commence production development are withheld pending the successful clearance of four mandatory technical PoCs and one formal legal licensing opinion.

---

## 6. Architectural Consequences

### Positive Consequences:
1. **Accelerated Time-to-Market:** Potentially reduces initial core implementation effort compared to a full custom build; exact impact requires project estimation.
2. **Foundational Financial Correctness:** Evaluates proven double-entry ledger algorithms, currency revaluations, and stock valuation queues for selective reuse.
3. **Rapid Data Modeling:** Capitalizes on Frappe's declarative JSON-based DocType metadata engine, automated schema migrations, and built-in REST API generation.
4. **Clean IP Partitioning:** Proprietary KIYA business logic (AI Governance, Sourcing, WMS, Field Service) is encapsulated in separate Frappe applications, distinct from upstream core modules.

### Negative Consequences & Trade-offs:
1. **Framework Coupling:** The platform architecture becomes structurally coupled to Python, Frappe Framework runtime conventions, and underlying database semantics.
2. **State Machine Adaptation:** An explicit architectural adapter layer must be maintained to map KIYA's 8-state operational `business_status` onto the underlying ledger submission triggers without breaking framework expectations.
3. **Multi-Tenant Overhead:** Multi-tenant scaling requires custom orchestration beyond standard bench capabilities to support automated enterprise SaaS provisioning.

---

## 7. Critical Risks & Mitigations

- **Risk 1 (GPLv3 License Contamination):** Reusing ERPNext core modules could trigger copyleft obligations for KIYA proprietary apps.
  - *Mitigation:* Require formal external legal review (Gate L-01). Enforce architectural network/API isolation between GPLv3 and proprietary modules. Fall back to Candidate D immediately if legal risk is unacceptable.
- **Risk 2 (Database Concurrency Locking):** High-concurrency warehouse dispatches may encounter row-level lock contention on stock ledger balance tables.
  - *Mitigation:* Validate transaction throughput and lock resolution under defined peak load in `PoC-03` (Threshold TBD — OQ-015). Design asynchronous queuing for ledger posting if contention exceeds thresholds.
- **Risk 3 (Upstream Framework Breaking Changes):** Upstream Frappe/ERPNext version upgrades could break bespoke hooks and monkey patches.
  - *Mitigation:* Absolute ban on monkey patching upstream core files; interact strictly via public hooks, DocEvents, and external REST APIs.

---

## 8. Proof-of-Concept (PoC) Dependencies

Final platform approval is contingent upon successful execution and passing of four empirical PoCs:
1. **`PoC-01` (Multi-Tenant SaaS Control Plane):** Prove automated tenant site creation, database isolation, and migration execution within target threshold without cross-tenant data leakage (Threshold TBD — OQ-015).
2. **`PoC-02` (India Tax & Compliance Seam):** Prove statutory GST e-invoicing and e-way bill generation via API with sandbox IRP signing independent of monolithic ERPNext.
3. **`PoC-03` (High-Volume Concurrency Benchmark):** Prove database transaction integrity and lock resolution under defined peak load (Threshold TBD — OQ-015).
4. **`PoC-04` (Mobile Offline Delta Synchronization):** Prove two-way offline conflict resolution and queued data sync for Field Service Work Orders.

---

## 9. Legal & Licensing Dependencies

- **Gate L-01 Mandatory Clearance:** Formal written opinion from qualified technology IP counsel confirming that:
  1. Operating ERPNext core modules alongside bespoke KIYA apps in a SaaS environment does not trigger GPLv3 source disclosure requirements for proprietary KIYA apps.
  2. Inter-process or REST-based integration boundaries between proprietary AI/WMS modules and ERPNext core satisfy open-source compliance requirements.
- *Default Action on Failure:* Immediate switch to Candidate D (100% MIT-licensed Frappe Framework + clean-room custom accounting).

---

## 10. Compliance with 8 KIYA-Owned Strategic Seams

| Strategic Seam | Compliance Strategy under Provisional Architecture |
| :--- | :--- |
| **1. Product / Domain Boundaries** | Differentiating domains (CRM, Sourcing, WMS, A2S) are built as independent KIYA apps; ERPNext core is restricted strictly to Accounts and Stock ledgers under evaluation. |
| **2. SaaS Control Plane** | External SaaS control plane service manages tenant lifecycle, automated DNS, and subscription metering; implementation runtime remains an evaluation option. |
| **3. API Gateway** | API gateway terminates external traffic, enforces tenant JWT validation, applies rate limiting, and routes to appropriate tenant sites; gateway technology remains an evaluation option. |
| **4. AI Governance** | Bespoke KIYA AI Service mediates all LLM interactions, enforces prompt redaction, records audit logs, and requires human approval before invoking ERP mutations. |
| **5. BI / EPM Separation** | Operational datastore replicates asynchronously to an external analytical datastore; operational ERP never executes heavy analytical queries; analytical storage technology remains deferred. |
| **6. UX / Mobile** | Dedicated mobile applications interact with KIYA via the API Gateway using custom API endpoints, completely independent of Frappe Desk UI; mobile UI framework remains an evaluation option. |
| **7. Security & Audit** | Enterprise IdP handles OIDC/SAML SSO; immutable audit logs are streamed to tamper-proof external storage; field-level permissions are strictly enforced. |
| **8. Tax Compliance** | Dedicated India Compliance service interfaces with statutory IRP/NIC portals via API, decoupling tax calculation and e-invoice generation from platform upgrades. |

---

## 11. Reversibility & Migration Strategy

To prevent proprietary vendor lock-in:
1. **Database Schema Neutrality:** All custom DocType schema definitions are stored as version-controlled JSON files in Git, allowing automated migration to standard relational DDL if a future rewrite is required.
2. **Standard API Contracts:** All client applications (Web, Mobile, External Integrations) communicate exclusively through documented OpenAPI-compliant contracts, isolating frontend assets from Frappe backend mechanics.
3. **Modular Domain Encapsulation:** Domain business logic is encapsulated in discrete Python service modules rather than inlined in database triggers or UI scripts.

---

## 12. Approval Authority & Governance Sign-Off

- **Current Status:** `PROPOSED / CONDITIONAL`
- **Recommending Lead:** Senior Enterprise Solutions Architect
- **Next Review Date:** Upon completion of Phase 1C and PoC Execution
- **Final Approval Authorities:**
  - Executive Committee (Business & IP Licensing Approval)
  - Architecture Governance Board (Technical Architecture Approval)
  - Legal Counsel (Open-Source Licensing Sign-Off)
