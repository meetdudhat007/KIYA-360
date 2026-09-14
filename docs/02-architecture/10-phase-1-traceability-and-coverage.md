# KIYA 360 — Phase 1 Traceability & Complete Coverage Audit

- **Document ID:** `ARCH-10`
- **Phase:** Phase 1 Governance — Complete Architecture Traceability & Requirements Audit
- **Status:** `REVIEW-READY BASELINE`
- **Date:** 14 September 2026
- **Authors:** Principal Enterprise Architect, Solution Architect, Requirements Traceability Lead
- **Primary Source:** `source/KIYA360_BRD.pdf` (Version 2.0, 13 September 2026)
- **Phase 0 Baseline:** `docs/00-requirements/` (`01-master-requirements.md` through `36-phase-0-completion-assessment.md`)
- **Phase 1 Architecture Suite:** `docs/02-architecture/` (`01-architecture-strategy-and-decision-framework.md` through `09-phase-1-architecture-risk-register.md`)

---

## 1. Executive Summary & Audit Purpose

This document provides the definitive **end-to-end traceability audit** verifying that the Phase 1 Architecture suite comprehensively covers, preserves, and operationalizes the entire Phase 0 requirements baseline.

### Formal Verification Assertions:
1. **100% Module Coverage:** All **28 authoritative modules** (`MOD-01` through `MOD-28`) defined in the approved BRD Module Inventory are formally mapped to bounded logical domains, master data owners, and integration contracts.
2. **100% Functional Requirement Record Coverage:** All **238 functional requirement records** established in Phase 0 are fully accounted for in the target architecture without omissions, unauthorized scope downgrades, or fabricated requirements.
3. **100% Shared Foundation Coverage:** All **15 Shared Foundations** (`SF-001` through `SF-015`) are realized as horizontal platform services in the Target Architecture (`L04`, `L11`, `L12`).
4. **100% Critical Dependency Coverage:** All **11 Critical Dependencies** (`DEP-001` through `DEP-011`) are enforced by transaction, data, and financial posting boundaries.
5. **100% Strategic Seam Governance:** All **8 KIYA-Owned Strategic Seams** established in Phase 1A are preserved and protected by formal anti-corruption adapters.

*Requirement Counting & Traceability Disambiguation:* The 238/238 figure refers strictly to the Phase 0 functional requirement record baseline established in `02-module-inventory.md`. Detailed C2C (18 stages), P2P (12 stages), and A2S (11 stages) records are subordinate elaboration specifications and must not be numerically conflated with the 238 functional requirement baseline records. All 238 Phase 0 functional requirement records have an architecture traceability mapping. This establishes architectural coverage, not implementation completeness or technical validation.

---

## 2. Global Traceability Chain

The platform enforces a continuous, bidirectional traceability chain linking business requirements to architectural specifications and validation gates:

```
[BRD v2.0 Scope & Business Intent]
       │
       ▼
[Phase 0 Requirements Baseline (28 Modules, 238 FR Records, 15 SFs, 11 DEPs)]
       │
       ▼
[Phase 1A Architecture Strategy & 8 Strategic Seams (ARCH-01)]
       │
       ▼
[Phase 1B Candidate Architecture Evaluation (ARCH-02 & ARCH-03)]
       │
       ▼
[Phase 1C Target Architecture Definition & 14 Conceptual Layers (ARCH-04)]
       │
       ▼
[Phase 1D Application, API & Master Data Architecture (ARCH-05)]
       │
       ▼
[Phase 1E Deployment & Operational Architecture (ARCH-06)]
       │
       ▼
[Phase 1 Governance & Validation Gates (ARCH-07, ARCH-08, ARCH-09)]
```

---

## 3. Comprehensive 28-Module Architectural Mapping & Traceability

The table below maps all 28 authoritative modules from `docs/00-requirements/02-module-inventory.md` to their architectural realization.

| Module ID | Authoritative Module Name | BRD Section Reference | Phase 0 Detailed Baseline Document | Phase 1C Conceptual Layer | Phase 1D Domain Cluster | Architectural Decision / Seam | Validation Gate Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MOD-01** | Platform & Administration | Section 7.1 | `01-master` / `34-sf` | L04, L12 | Cluster 6: Platform Foundations | `ADR-001`, `ADR-005`, Seam #2, Seam #7 | PoC-01 |
| **MOD-02** | CRM | Section 7.2 | `31-c2c` / `35-remaining` | L01, L03, L05 | Cluster 1: Customer Engagement | `ADR-001`, `ADR-002`, Seam #1 | PoC-01 |
| **MOD-03** | Sales | Section 7.3 | `31-customer-to-cash` | L03, L05, L06, L07 | Cluster 1: Customer Engagement | `ADR-001`, `ADR-003`, Seam #1 | PoC-01, STK-01 |
| **MOD-04** | Marketing | Section 7.4 | `35-remaining-module-baselines` | L01, L03 | Cluster 1: Customer Engagement | `ADR-001`, Seam #1 | Architecture Review |
| **MOD-05** | Customer Service | Section 7.5 | `35-remaining-module-baselines` | L01, L03, L05 | Cluster 1: Customer Engagement | Case/Ticket Management, Seam #1 | Architecture Review |
| **MOD-06** | Procurement | Section 7.6 | `32-procure-to-pay` | L03, L05, L06, L07 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002`, Seam #1 | PoC-01 |
| **MOD-07** | Supplier Management | Section 7.7 | `32-p2p` / `35-remaining` | L01, L03, L07 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002`, Seam #1 | Architecture Review |
| **MOD-08** | Inventory | Section 7.8 | `31-c2c` / `32-p2p` / `34-sf` | L05, L07, L08 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002`, Seam #4 | PoC-03 |
| **MOD-09** | Warehouse | Section 7.9 | `31-c2c` / `32-p2p` / `34-sf` | L05, L07, L08 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002` | Architecture Review |
| **MOD-10** | Manufacturing | Section 7.10 | `31-customer-to-cash` / `35` | L03, L05, L06 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002`, Seam #4 | PoC-03 |
| **MOD-11** | MRP & Planning | Section 7.11 | `31-c2c` / `35-remaining` | L03, L05 | Cluster 2: Supply Chain Ops | `ADR-001`, Seam #1 | Architecture Review |
| **MOD-12** | Quality | Section 7.12 | `31-c2c` / `32-p2p` / `35` | L05, L06, L11 | Cluster 2: Supply Chain Ops | `ADR-001`, Seam #1 | Architecture Review |
| **MOD-13** | Asset Management | Section 7.13 | `33-asset-to-service` / `35` | L05, L08 | Cluster 3: Service & Maintenance | Corporate Fixed Asset Boundary, `ADR-002` | Architecture Review |
| **MOD-14** | Maintenance & Field Service | Section 7.14 | `33-asset-to-service` | L02, L03, L05, L06 | Cluster 3: Service & Maintenance | Customer Installed Base Boundary, Seam #6 | PoC-04 |
| **MOD-15** | Logistics & Transportation | Section 7.15 | `35-remaining-module-baselines` | L03, L05, L07 | Cluster 2: Supply Chain Ops | `ADR-001`, `ADR-002`, Seam #1 | Architecture Review |
| **MOD-16** | Projects | Section 7.16 | `35-remaining-module-baselines` | L03, L05, L06 | Cluster 3: Service & Maintenance | `ADR-001`, Seam #1 | Architecture Review |
| **MOD-17** | Finance & Accounting | Section 7.17 | `31-c2c` / `32-p2p` / `34-sf` | L05, L08, L12 | Cluster 4: Financial Governance | `ADR-001`, `ADR-002`, `DEC-009`, Seam #8 | PoC-02, PoC-03 |
| **MOD-18** | Tax & Statutory Compliance | Section 7.18 | `31-c2c` / `32-p2p` / `34-sf` | L04, L05, L14 | Cluster 4: Financial Governance | Global Tax Engine, Seam #8 | PoC-02 |
| **MOD-19** | HR & Payroll | Section 7.19 | `35-remaining-module-baselines` | L03, L05, L08, L12 | Cluster 5: Human Capital Mgmt | `ADR-001`, `ADR-002`, Seam #7 | STK-03 |
| **MOD-20** | E-Commerce | Section 7.20 | `35-remaining-module-baselines` | L01, L07, L14 | Cluster 1: Customer Engagement | `ADR-001`, Seam #3, Seam #6 | PoC-01 |
| **MOD-21** | Document Management | Section 7.21 | `34-shared-foundations` | L11 | Cluster 6: Platform Foundations | `ADR-001`, `SF-007` | Architecture Review |
| **MOD-22** | Business Intelligence | Section 7.22 | `35-remaining-module-baselines` | L09 | Cluster 6: Platform Intelligence | `ADR-006`, Seam #5 | PoC-03 |
| **MOD-23** | EPM / Budget / Forecast | Section 7.23 | `35-remaining-module-baselines` | L09 | Cluster 4: Financial Governance | `ADR-006`, Seam #5 | STK-03 |
| **MOD-24** | Workflow & Approvals | Section 7.24 | `34-shared-foundations` | L06 | Cluster 6: Platform Foundations | `ADR-003`, `SF-005` | STK-01 |
| **MOD-25** | AI & Automation | Section 7.25 | `35-remaining-module-baselines` | L10 | Cluster 6: Platform Intelligence | Invariant AI Safety Guardrail, Seam #4 | Architecture Review |
| **MOD-26** | Integration & API | Section 7.26 | `34-shared-foundations` | L07 | Cluster 6: Platform Foundations | Unified Ingress / API Gateway, Seam #3 | Architecture Review |
| **MOD-27** | Mobile Application | Section 7.27 | `34-shared-foundations` | L02 | Cluster 6: Platform Foundations | Native Offline Sync, Seam #6 | PoC-04 |
| **MOD-28** | Audit, Security & Compliance | Section 7.28 | `34-shared-foundations` | L12 | Cluster 6: Platform Foundations | Immutable Audit Ledger, Seam #7 | Architecture Review |

---

## 4. 238 Functional Requirement Records Audit Verification

The audit verifies that all 238 functional requirement records defined in Phase 0 (`docs/00-requirements/02-module-inventory.md`) are accounted for in the architecture:

| Module Inventory Block | Module Name | BRD Requirements Count | Architectural Layer Realization | Traceability Status |
| :--- | :--- | :--- | :--- | :--- |
| **Module 01** | Platform & Administration | **50 Requirements** (`FR-PADM-1.1.1` to `1.8.6`) | L04, L12 | **100% Traceable** |
| **Module 02** | CRM | **8 Requirements** (`FR-CRM-001` to `008`) | L01, L03, L05 | **100% Traceable** |
| **Module 03** | Sales | **8 Requirements** (`FR-SALES-001` to `008`) | L03, L05, L06, L07 | **100% Traceable** |
| **Module 04** | Marketing | **7 Requirements** (`FR-MKT-001` to `007`) | L01, L03 | **100% Traceable** |
| **Module 05** | Customer Service | **7 Requirements** (`FR-CSVC-001` to `007`) | L01, L03, L05 | **100% Traceable** |
| **Module 06** | Procurement | **7 Requirements** (`FR-PROC-001` to `007`) | L03, L05, L06, L07 | **100% Traceable** |
| **Module 07** | Supplier Management | **6 Requirements** (`FR-SUPM-001` to `006`) | L01, L03, L07 | **100% Traceable** |
| **Module 08** | Inventory | **7 Requirements** (`FR-INV-001` to `007`) | L05, L07, L08 | **100% Traceable** |
| **Module 09** | Warehouse | **7 Requirements** (`FR-WH-001` to `007`) | L05, L07, L08 | **100% Traceable** |
| **Module 10** | Manufacturing | **7 Requirements** (`FR-MFG-001` to `007`) | L03, L05, L06 | **100% Traceable** |
| **Module 11** | MRP & Planning | **7 Requirements** (`FR-MRP-001` to `007`) | L03, L05 | **100% Traceable** |
| **Module 12** | Quality | **7 Requirements** (`FR-QLTY-001` to `007`) | L05, L06, L11 | **100% Traceable** |
| **Module 13** | Asset Management | **7 Requirements** (`FR-AST-001` to `007`) | L05, L08 | **100% Traceable** |
| **Module 14** | Maintenance & Field Service | **7 Requirements** (`FR-MFS-001` to `007`) | L02, L03, L05, L06 | **100% Traceable** |
| **Module 15** | Logistics & Transportation | **7 Requirements** (`FR-LOG-001` to `007`) | L03, L05, L07 | **100% Traceable** |
| **Module 16** | Projects | **7 Requirements** (`FR-PROJ-001` to `007`) | L03, L05, L06 | **100% Traceable** |
| **Module 17** | Finance & Accounting | **7 Requirements** (`FR-FIN-001` to `007`) | L05, L08, L12 | **100% Traceable** |
| **Module 18** | Tax & Statutory Compliance | **7 Requirements** (`FR-TAX-001` to `007`) | L04, L05, L14 | **100% Traceable** |
| **Module 19** | HR & Payroll | **7 Requirements** (`FR-HR-001` to `007`) | L03, L05, L08, L12 | **100% Traceable** |
| **Module 20** | E-Commerce | **7 Requirements** (`FR-ECOM-001` to `007`) | L01, L07, L14 | **100% Traceable** |
| **Module 21** | Document Management | **7 Requirements** (`FR-DOCM-001` to `007`) | L11 | **100% Traceable** |
| **Module 22** | Business Intelligence | **7 Requirements** (`FR-BI-001` to `007`) | L09 | **100% Traceable** |
| **Module 23** | EPM / Budget / Forecast | **7 Requirements** (`FR-EPM-001` to `007`) | L09 | **100% Traceable** |
| **Module 24** | Workflow & Approvals | **7 Requirements** (`FR-WFA-001` to `007`) | L06 | **100% Traceable** |
| **Module 25** | AI & Automation | **7 Requirements** (`FR-AIAU-001` to `007`) | L10 | **100% Traceable** |
| **Module 26** | Integration & API | **7 Requirements** (`FR-INTG-001` to `007`) | L07 | **100% Traceable** |
| **Module 27** | Mobile Application | **7 Requirements** (`FR-MOB-001` to `007`) | L02 | **100% Traceable** |
| **Module 28** | Audit, Security & Compliance | **5 Requirements** (`FR-ASC-001` to `005`) | L12 | **100% Traceable** |
| **TOTAL BRD BASELINE** | **All 28 Modules** | **238 Functional Requirement Records** | **All 14 Layers** | **100% AUDIT PASS** |

---

## 5. Shared Foundation Traceability Matrix (SF-001 to SF-015)

The table below maps all 15 authoritative Shared Foundation records from `docs/00-requirements/13-shared-foundation-requirements-map.md`.

| SF ID | Authoritative Shared Foundation Name | Architectural Layer Realization | Concrete Architecture Mechanism | Associated Architecture Decision |
| :--- | :--- | :--- | :--- | :--- |
| **SF-001** | Organizational / Enterprise Context & Multi-Company | Layer L04 / Layer L12 | Hierarchical Company -> Branch/Unit entity models in relational core; multi-company context. | `ADR-001`, `ADR-005` |
| **SF-002** | Users, Roles, Permissions & Access Control | Layer L04 / Layer L12 | RBAC/ABAC permission matrix; authentication gatekeeper; session and device controls. | `ADR-001`, `MOD-28` |
| **SF-003** | Shared Master-Data Management & Unified Data Model | Layer L04 / Layer L05 | Single-source master data registry; single data model without duplicate entities across modules. | `ADR-002`, `DEC-007` |
| **SF-004** | Consistent Conceptual Master Usage | Layer L04 / Layer L05 | Consistent entity references across Customer, Supplier, Item, Employee, and Assets. | `ADR-002`, `DEC-007` |
| **SF-005** | Shared KIYA Engine Workflow, Approvals & Escalation | Layer L04 / Layer L06 | Universal rule-based routing, multi-tier approvals, dynamic thresholds, and delegations. | `ADR-003`, `MOD-24` |
| **SF-006** | Notifications, Reminders & Communication Channels | Layer L04 / Layer L06 | Decoupled event-driven notification dispatcher routing across Email, SMS, WhatsApp, Push, In-App. | Target Architecture Section 9 |
| **SF-007** | Document Capture, Storage, Versioning & Signatures | Layer L04 / Layer L11 | Universal DMS metadata index, secure object storage, SHA-256 hashing, and digital signing. | Target Architecture Section 10 |
| **SF-008** | Audit Trail, Policy, Security & Compliance Monitoring | Layer L04 / Layer L12 | Immutable, write-once audit ledger capturing all create/update/delete and authentication events. | Target Architecture Section 2 |
| **SF-009** | Native Mobile Applications & Offline Synchronization | Layer L02 / Layer L04 | Local encrypted mobile store, client-generated UUIDs, and outbox synchronization queue. | Target Architecture Section 14 |
| **SF-010** | AI Insights, Predictive Analytics & Machine Learning | Layer L04 / Layer L10 | Centralized AI gateway with PII redaction, prompt auditing, and human-in-the-loop controls. | Target Architecture Section 12 |
| **SF-011** | Real-Time Dashboards, Reports, KPIs & EPM | Layer L04 / Layer L09 | Decoupled read models, real-time KPI aggregator, and financial consolidation engine. | `ADR-006`, `MOD-22`/`23` |
| **SF-012** | API Management, System Integration & Webhooks | Layer L04 / Layer L07 | Unified Ingress / API Gateway enforcing perimeter auth, rate limits, and webhook dispatching. | Target Architecture Section 2 |
| **SF-013** | Numbering Series for Documents, Transactions & Masters | Layer L04 / Layer L05 | Configurable document prefix, fiscal year sequencing, and gap-free auto-numbering engine. | Target Architecture Section 2 |
| **SF-014** | Common Record & Interaction Capabilities | Layer L04 / Layer L01 | Universal CRUD actions, global search, filter, sort, context switcher, and audit inspect. | Target Architecture Section 15 |
| **SF-015** | 24/7 Operations, Real-Time Insights & Scalable Operation | Layer L04 / Layer L13 | High-availability compute clustering, stateless web tiers, and decoupled worker queues. | Target Architecture Section 16 |

---

## 6. Critical Dependency Traceability Matrix (DEP-001 to DEP-011)

The table below maps the 11 authoritative dependency identifiers from `docs/00-requirements/14-critical-requirement-dependencies.md` to their Phase 1 architectural enforcement. The dependency names, directionality, and semantics are strictly preserved from the Phase 0 source.

| Dependency ID | Authoritative Dependency Name | Upstream → Downstream (Phase 0) | Architectural Enforcement Mechanism | Architecture Document Reference |
| :--- | :--- | :--- | :--- | :--- |
| **DEP-001** | CRM → Sales | FR-CRM-001–008 → FR-SALES-001–003 (MOD-02 → MOD-03) | Bounded domain transition; qualified leads/opportunities convert into enquiries/quotations without re-entry. | `ARCH-05` Section 6 |
| **DEP-002** | Sales → Inventory / Warehouse | FR-SALES-003–005 → FR-INV-002, FR-WH-003–005 (MOD-03 → MOD-08 / MOD-09) | Two-phase inventory reservation: ATP allocation on order confirm; stock decrement on dispatch. | `ARCH-04` Section 4.1 |
| **DEP-003** | Sales → MRP & Planning → Manufacturing | FR-SALES-003 → FR-MRP-001–006 → FR-MFG-003–005 (MOD-03 → MOD-11 → MOD-10) | Unmet demand feeds planning and generates production/work orders; BOM explosion drives shop floor. | `ARCH-05` Section 7 |
| **DEP-004** | Manufacturing → Quality → Warehouse | FR-MFG-003–005 → FR-QLTY-002–004 → FR-WH-003 (MOD-10 → MOD-12 → MOD-09) | Strict inspection gate: work-in-process/finished goods pass inspection before warehouse put-away. | `ARCH-04` Section 4.2 |
| **DEP-005** | Sales / Procurement → Finance & Tax | FR-SALES-003–005; FR-PROC-004–005 → FR-FIN-001–003; FR-TAX-001–007 (MOD-03/06 → MOD-17/MOD-18) | Sales dispatches and supplier invoices participate in statutory tax processing and AR/AP/GL accounting; GRNs provide receiving basis for 3-way matching. | `ARCH-04` Section 7 & 8 |
| **DEP-006** | Procurement → Supplier Management | FR-PROC-002–004 → FR-SUPM-003, FR-SUPM-005 (MOD-06 → MOD-07) | RFQ/RFP and PO activity feeds the supplier performance scorecard; procurement events update supplier evaluation. | `ARCH-05` Section 6 |
| **DEP-007** | Asset Management → Maintenance & Field Service | FR-AST-001–006 → FR-MFS-001–007 (MOD-13 → MOD-14) | Installed assets/warranty generate service requests, work orders, spare-parts consumption, and asset history. | `ARCH-04` Section 4.3 |
| **DEP-008** | Projects → Finance | FR-PROJ-005–006 → FR-FIN-002–003, FR-FIN-006 (MOD-16 → MOD-17) | Project time/expense and billing post to Accounts Receivable and Cost Accounting. | `ARCH-04` Section 4.1 |
| **DEP-009** | All modules → BI / EPM | All module transactions → FR-BI-001–007; FR-EPM-001–007 (All → MOD-22 / MOD-23) | Every transaction streams to dashboards, KPIs, and budget/forecast variance analysis in real time. | `ARCH-04` Section 13, `ADR-006` |
| **DEP-010** | All modules → Workflow & Approvals | All modules → FR-WFA-001–007 (All → MOD-24) | Any module can attach shared KIYA Engine approval/escalation logic; no bespoke approval hardcoding. | `ARCH-04` Section 6, `ADR-003` |
| **DEP-011** | All modules → Audit, Security & Compliance | All modules → FR-PADM-1.8.1–1.8.6; FR-ASC-001–005 (All → MOD-01/MOD-28) | Every create/update/delete and login event is captured in the immutable audit trail. | `ARCH-04` Section 2, `SF-008` |

> **Note:** Phase 1 architecture also establishes additional important architectural boundaries (such as 3-way matching enforcement, payment clearing rules, Customer Installed Base vs. Corporate Fixed Asset distinction, Field Service vs. Manufacturing Work Order disambiguation, multi-entity financial consolidation, and AI advisory-only guardrails). These are legitimate architectural elaborations but are NOT Phase 0 dependency IDs and must not be conflated with DEP-001 through DEP-011.

---

## 7. Strategic Seams Traceability Matrix (Seams #1 to #8)

| Seam ID | Seam Title & Scope | Architectural Realization | Anti-Corruption Mechanism | Associated Validation Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Seam #1** | KIYA Product & Platform Boundaries | Core Platform Invariant | Proprietary KIYA business domains (Enquiry, C2C) encapsulated in custom apps. | `ADR-001`, `ADR-004` |
| **Seam #2** | SaaS Control Plane & Tenancy | Layer L04 / Layer L12 | External SaaS Control Plane automates tenant database lifecycle independently. | `ADR-005`, `PoC-01` |
| **Seam #3** | Unified API Gateway & Ingress | Layer L07 (Ingress Boundary) | Single ingress gateway terminates auth, enforces rate limits, and audits requests. | `ARCH-05` Section 4 |
| **Seam #4** | AI Governance & Automation | Layer L10 (Intelligence) | Centralized AI gateway with PII redaction, prompt audit, and human approval queue. | `ARCH-04` Section 12 |
| **Seam #5** | Enterprise BI, Analytics & EPM | Layer L09 (Analytics) | Decoupled reporting tier querying near-real-time read replicas and OLAP marts. | `ADR-006`, `PoC-03` |
| **Seam #6** | Unified UX, Web & Mobile Clients | Layer L01 & Layer L02 | Modern responsive web frontend and offline-first mobile client using standard APIs. | `PoC-04` |
| **Seam #7** | Security, Identity & Compliance Audit | Layer L12 (Security) | RBAC/ABAC gatekeeper and immutable audit ledger spanning all 28 modules. | Architecture Review |
| **Seam #8** | Global Tax Engine & India Compliance | Layer L04 / MOD-18 | Pluggable tax determination and NIC e-invoice generation isolated from core code. | `PoC-02` |

---

## 8. Conclusion & Final Traceability Verdict

The Phase 1 Traceability and Coverage Audit confirms **100% complete, unbroken requirements coverage across all 28 authoritative modules (`MOD-01` to `MOD-28`), 238 functional requirement records, 15 shared foundations (`SF-001` to `SF-015`), 11 critical dependencies (`DEP-001` to `DEP-011`), and 8 strategic seams**. No requirements were dropped, downgraded, or invented. The architecture baseline is completely traceable and safe for Phase 2 progression.
