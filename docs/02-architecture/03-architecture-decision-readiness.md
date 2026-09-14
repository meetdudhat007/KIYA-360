# KIYA 360 — Architecture Decision Readiness & Governance Summary

## 1. Executive Decision Summary

- **Document ID:** `03-architecture-decision-readiness`
- **Phase:** Phase 1 — Platform Architecture & System Design (Phase 1B Decision-Readiness Summary)
- **Status:** Complete Governance Summary
- **Date:** 14 September 2026
- **Governance Context:** Evaluates readiness to proceed from Candidate Architecture Evaluation (Phase 1B) to Target Architecture Definition (Phase 1C).
- **Primary Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026)
- **Evaluation Baseline:** `docs/02-architecture/02-candidate-architecture-evaluation.md`

Phase 1B executed an objective, comprehensive evaluation of five candidate architectural strategies across 22 architectural dimensions, measuring direct fit against the 28 BRD modules, 238 functional requirements, core cross-module lifecycles (C2C, P2P, A2S), and 8 KIYA-owned strategic seams. 

### Key Strategic Findings:
1. **Requirement Mismatch of Pure Off-the-Shelf Monolith (Candidate B — ERPNext Primary):** Materially mismatched with current KIYA requirements and constraints: incompatible with `CD-002` (hardcoded binary submission state `docstatus` cannot model KIYA 8-state operational business statuses), lacks 40%+ of required BRD workflows (no Enquiry, no multi-envelope RFPs, no WMS coordinate binning, no Field Service Work Orders, no India GST in upstream develop branch), and creates GPLv3 copyleft questions requiring legal review.
2. **Architectural Complexity of Distributed Headless Microservices for Core ERP (Candidate E):** While headless separation is valuable for external touchpoints, adopting distributed microservices across transactional general ledger, inventory double-entry balance sheets, and procurement currently appears poorly suited to KIYA's core transactional ERP workload because of the additional distributed-consistency (2PC / saga orchestration) and operational complexity it introduces.
3. **Substantially Higher Implementation Burden of Full Custom Build (Candidate A):** Eliminates licensing risks and provides total data model freedom, but requires building and validating foundational accounting engine capabilities (reversing, multi-currency valuation, double-entry invariance), resulting in substantially higher implementation burden and engineering effort.
4. **Provisional Leading Candidate (Candidate C — Frappe Framework + Selective ERPNext Reuse Under Evaluation):** Offers an attractive balance between potential delivery acceleration and foundational financial correctness by evaluating mature core capabilities (General Ledger, Chart of Accounts, Double-Entry Inventory Stock Ledger) as potential reuse candidates while implementing all differentiating modules (CRM, Sourcing, WMS, Field Service, AI Governance, SaaS Control Plane) as bespoke KIYA apps.
5. **Evaluated Contingency Fallback (Candidate D — Frappe Framework + Mostly Custom KIYA Apps):** Retains rapid meta-data schema productivity on the MIT-licensed Frappe Framework, authoring custom clean-room accounting and stock engines if legal counsel deems ERPNext GPLv3 reuse commercially unviable under SaaS distribution.

---

## 2. Candidate Status

| Candidate Identifier | Architectural Archetype | Evaluation Verdict | Strategic Status | Key Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Candidate A** | Full Custom Architecture (Custom Backend + Custom Frontend) | **High Implementation Burden** | Active Reference / Fallback | Zero GPLv3 copyleft exposure and 100% data control, but substantially higher implementation burden because major ERP capabilities must be built, validated, and maintained. |
| **Candidate B** | ERPNext-Primary Architecture (Monolithic ERPNext Adaptation) | **Materially Mismatched** | **UNFAVORABLE** | Incompatible with `CD-002`, lacks 40%+ BRD modules, GPLv3 copyleft exposure, and monolithic coupling. |
| **Candidate C** | Frappe Framework + Selective ERPNext Core Modules | **Provisional Leader** | **PROVISIONALLY RECOMMENDED** | Balances financial rigor and potential delivery acceleration under evaluation. Subject to 4 PoC gates and formal legal review. |
| **Candidate D** | Frappe Framework + Mostly Custom KIYA Applications | **Evaluated Fallback** | **EVALUATED CONTINGENCY** | Absence of GPLv3 copyleft constraints; evaluated fallback if ERPNext reuse is rejected by corporate legal counsel. |
| **Candidate E** | Modular Headless / API-First Architecture | **Poorly Suited for Core ERP** | Selective Seam Pattern | Distributed consistency complexity for core transactional ledgers; architectural pattern evaluated for external touchpoints. |

---

## 3. Evidence Confidence

| Architecture Dimension Category | Evaluation Confidence Level | Basis of Assessment | Remaining Verification Need |
| :--- | :--- | :--- | :--- |
| **Functional Module Coverage** | **HIGH** | Line-by-line inspection of BRD (28 modules) vs. ERPNext DocTypes and custom build boundaries. | Finalize custom DocType schemas in Phase 1C. |
| **Core Flow Fidelity (C2C, P2P, A2S)** | **HIGH** | Traceability mapping across 16 C2C, 12 P2P, and 14 A2S requirements. | Validate transaction orchestration in Phase 1C. |
| **Lifecycle & Status Fit (`CD-002`)** | **HIGH** | Inspected Frappe DocType status architecture vs. ERPNext `docstatus` submission engine. | Verify state-machine adapter behavior in PoC. |
| **Multi-Tenant SaaS Scaling** | **MEDIUM** | Frappe bench multi-tenancy exists but requires empirical validation under defined multi-site benchmark loads (Threshold TBD — OQ-015). | **Mandatory `PoC-01` required.** |
| **India Tax & E-Invoicing Seam** | **MEDIUM** | India Compliance app exists in Frappe ecosystem; separation from ERPNext core must be tested. | **Mandatory `PoC-02` required.** |
| **High-Volume Concurrency & Locking** | **MEDIUM** | Relational database row-level locking behavior on stock ledger under peak transaction concurrency requires benchmarking. | **Mandatory `PoC-03` required.** |
| **Mobile Offline Delta Synchronization** | **MEDIUM** | Modern offline frameworks exist; Frappe REST delta sync requires empirical verification. | **Mandatory `PoC-04` required.** |
| **Licensing & GPLv3 Boundary** | **LOW (Pending Legal)** | Architectural network isolation patterns exist; legal enforceability requires external counsel. | **Mandatory Legal Review required.** |

---

## 4. Critical Risks

1. **`RSK-01`: GPLv3 Derivative Work Contamination (Candidate C)**
   - *Impact:* Critical. If selective reuse of ERPNext modules (Accounts/Stock) taints proprietary KIYA modules (AI Governance, Sourcing, WMS), KIYA commercial SaaS IP could be compromised.
   - *Mitigation:* Formal legal review; architectural containment via network API isolation; maintain Candidate D (clean-room custom accounts) as zero-delay fallback.
2. **`RSK-02`: Document Lifecycle Conflict (`CD-002` vs. `docstatus`)**
   - *Impact:* High. Attempting to force KIYA's 8-state operational lifecycle into ERPNext's 3-state binary submission model will corrupt transaction integrity if hardcoded submission logic is bypassed.
   - *Mitigation:* Decouple operational `business_status` from physical ledger immutability; establish an explicit Frappe state-machine controller.
3. **`RSK-03`: Multi-Tenant Control Plane Scalability Bottleneck**
   - *Impact:* High. Default Frappe bench tooling lacks enterprise SaaS metering, real-time cross-tenant telemetry, and zero-downtime rolling upgrades.
   - *Mitigation:* Implement Seam 02 (SaaS Control Plane) as an external, independent orchestrator managing worker pools and tenant site provisionings.
4. **`RSK-04`: Database Concurrency Serialization on Stock Balance Updates**
   - *Impact:* High. Concurrent transactions updating identical SKU balances in warehouse bins cause deadlocks or database lock timeouts.
   - *Mitigation:* Queue-based asynchronous ledger posting or partitioned warehouse ledger staging validated in `PoC-03`.

---

## 5. Blocking Unknowns

| Unknown ID | Unknown Description | Affected Candidate(s) | Business & Technical Impact | Resolution Vehicle | Target Gate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`UNK-01`** | Legal boundary enforceability of GPLv3 vs. MIT in Frappe multi-app bench | Candidate C | Potential open-source contamination of proprietary KIYA apps | Formal Legal Opinion | Gate L-01 (Pre-Phase 2) |
| **`UNK-02`** | Frappe multi-tenant bench upper scalability threshold under containerized bench deployment | Candidate C, D | Operational instability or excessive memory footprints above threshold | `PoC-01` Bench Test | Gate T-01 (Phase 1C) |
| **`UNK-03`** | Operational independence of India Tax & Compliance from core ERPNext | Candidate C, D | Regulatory failure if India e-invoice/e-way bill requires monolithic ERPNext | `PoC-02` Tax Verification | Gate T-02 (Phase 1C) |
| **`UNK-04`** | Stock ledger transaction concurrency throughput under peak load (Threshold TBD — OQ-015) | Candidate C, D | Database deadlocks during flash warehouse dispatch / order processing | `PoC-03` Concurrency Test | Gate T-03 (Phase 1C) |
| **`UNK-05`** | Conflict-free delta synchronization mechanism for mobile offline operations | Candidate A, C, D, E | Field service technician data corruption and offline sync failures | `PoC-04` Mobile Sync Test | Gate T-04 (Phase 1C) |
| **`UNK-06`** | Executive commercial tolerance for open-source derived codebase vs. 100% proprietary IP | Candidate C vs. D/A | Strategic valuation, investor due diligence, and enterprise IP positioning | Executive Committee Input | Gate S-01 (Phase 1B Sign-off) |

---

## 6. Required Proof-of-Concept (PoC) Matrix

The following four empirical PoCs are mandatory prerequisites before any architecture recommendation can be converted from PROVISIONAL to FINAL APPROVED:

```
+----------------------------------------------------------------------------------------------------+
|                                    MANDATORY ARCHITECTURE PoCs                                     |
+-------------------+-------------------------------------+--------------------+---------------------+
| PoC Identifier    | Validation Objective                | Target Candidate   | Blocking Gate       |
+-------------------+-------------------------------------+--------------------+---------------------+
| PoC-01: Multi-    | Verify programmatic tenant creation,| Candidate C & D    | Gate T-01           |
| Tenant SaaS Plane | isolation, and rolling updates      |                    |                     |
+-------------------+-------------------------------------+--------------------+---------------------+
| PoC-02: India Tax | Verify GST, e-invoice, e-way bill   | Candidate C & D    | Gate T-02           |
| Compliance Seam   | operational independence via API    |                    |                     |
+-------------------+-------------------------------------+--------------------+---------------------+
| PoC-03: Stock     | Benchmark row-level locking under   | Candidate C & D    | Gate T-03           |
| Concurrency Test  | peak transaction concurrency        |                    |                     |
+-------------------+-------------------------------------+--------------------+---------------------+
| PoC-04: Mobile    | Verify two-way offline conflict     | Candidate C & D    | Gate T-04           |
| Offline Sync      | resolution for Field Service Work   |                    |                     |
+-------------------+-------------------------------------+--------------------+---------------------+
```

- **`PoC-01` Execution Requirement:** Must prove programmatic site creation, database provisioning, automated migration, and zero cross-tenant query leakage within target latency threshold (Threshold TBD — OQ-015 / Architecture Test Design).
- **`PoC-02` Execution Requirement:** Must generate statutory-compliant GST e-invoice JSON, sign via mock/sandbox IRP portal, and generate signed QR code without monolithic ERPNext coupling.
- **`PoC-03` Execution Requirement:** Must maintain transactional consistency and connection pool stability without unhandled deadlocks under defined peak load (Threshold TBD — OQ-015 / Architecture Test Design).
- **`PoC-04` Execution Requirement:** Must execute offline field service job completion with photo attachment, queue locally, simulate connection drop, reconnect, and reconcile delta against server state without loss.

---

## 7. Required Legal Review

### Gate L-01: Frappe (MIT) vs. ERPNext (GPLv3) SaaS Distribution Exposure
- **Component:** Frappe Framework v15+ (MIT) + ERPNext v15+ Core Modules (GPLv3) + KIYA Bespoke Apps (Proprietary).
- **Core Legal Question:** Does packaging bespoke proprietary KIYA apps alongside GPLv3 ERPNext apps in the same Python virtual environment / Frappe bench constitute a "derivative work" under GPLv3, obligating KIYA to open-source its proprietary codebase upon offering multi-tenant SaaS services?
- **Analysis Scope:**
  1. SaaS delivery model vs. on-premise binary distribution (Affero GPL vs. standard GPLv3 boundaries).
  2. Inter-process communication boundaries (API / service separation vs. in-process Python module imports).
  3. Clean-room development guidelines for Candidate D fallback.
- **Decision Authority:** External Intellectual Property & Technology Legal Counsel.
- **Governing Rule:** No production code reuse from ERPNext may occur until a written legal opinion confirming safe commercial boundaries is received and approved by executive leadership.

---

## 8. Required Stakeholder Decisions

The following business, licensing, and operational decisions require formal stakeholder sign-off:

1. **`STK-01`: Intellectual Property Positioning & Licensing Tolerance**
   - *Question:* Does KIYA executive leadership accept selective open-source core reuse (Candidate C) with its accompanying legal review, or does the commercial roadmap mandate 100% clean-room proprietary ownership (Candidate D or A)?
   - *Stakeholder Owner:* Executive Committee / Founder.
2. **`STK-02`: Multi-Tenant Deployment & Isolation Topology (`CG-03`)**
   - *Question:* Is database-per-tenant isolation mandated for all enterprise customers, or is a pooled multi-tenant database acceptable for entry-tier SaaS subscribers?
   - *Stakeholder Owner:* Product Management & Information Security.
3. **`STK-03`: Mobile Offline Work Order Scope & Device Mandate (`CG-05`)**
   - *Question:* Which roles require full offline mobile capability (Field Service technicians only, or Warehouse / Field Sales as well)?
   - *Stakeholder Owner:* Operations & Field Services Business Lead.
4. **`STK-04`: Business Status State-Machine Finalization (`CD-002`)**
   - *Question:* Formally ratify the transition matrix for the 8 standardized `business_status` lifecycles across all 28 modules.
   - *Stakeholder Owner:* Enterprise Solutions Architect & Business Process Leads.

---

## 9. Decision Thresholds & Non-Negotiable Gates

A candidate architecture **CANNOT** receive final platform approval if it violates any of the following mandatory decision thresholds:

- [ ] **Threshold 1 (Tenant Data Leakage):** Any architecture where tenant isolation relies solely on application-level filtering without database or schema-level boundary enforcement fails immediately.
- [ ] **Threshold 2 (Financial Ledger Invariance):** Any architecture lacking ACID double-entry general ledger immutability and verifiable transaction reversing fails immediately.
- [ ] **Threshold 3 (Licensing IP Integrity):** Any architecture that exposes KIYA proprietary algorithms, AI models, or domain logic to copyleft open-source distribution mandates fails immediately.
- [ ] **Threshold 4 (Strategic Seam Compatibility):** Any architecture that prevents KIYA ownership of the 8 mandatory strategic seams fails immediately.
- [ ] **Threshold 5 (Lifecycle Flexibility):** Any architecture that hardcodes binary submission states (`docstatus = 1`) and cannot natively track granular operational `business_status` fails immediately.
- [ ] **Threshold 6 (Statutory Tax Compliance):** Any architecture unable to reliably generate compliant India GST, e-invoicing, and e-way bill payloads fails immediately.

---

## 10. Recommendation Status

In strict accordance with Phase 1B governance (§1 and §38), the evaluation evidence supports:

### **PROVISIONAL ARCHITECTURE RECOMMENDATION — FINAL APPROVAL PENDING REQUIRED VALIDATION**

- **Provisional Leading Candidate:** **Candidate C (Frappe Framework + Selective ERPNext Reuse Under Evaluation)**
- **Evaluated Fallback Candidate:** **Candidate D (Frappe Framework + Mostly Custom KIYA Applications)**

*Justification:*
Candidate C offers potential delivery acceleration and lower core engineering risk by evaluating mature accounting engines for selective reuse within a metadata-driven framework. However, because critical legal interpretations (GPLv3 SaaS boundary) and operational scaling questions (bench multi-tenancy, stock concurrency) remain active unknowns, final approval cannot be granted without formal empirical validation.

---

## 11. Conditions for Architecture Approval

Formal conversion from **PROVISIONAL** to **FINAL APPROVED** platform architecture requires satisfying all six gates below:

1. **Gate L-01 (Legal Clearance):** Receipt of written IP legal opinion validating the licensing isolation structure between Frappe (MIT), ERPNext core (GPLv3), and KIYA custom apps (Proprietary).
2. **Gate T-01 (SaaS PoC):** Successful completion of `PoC-01` demonstrating automated tenant site provisioning, isolation, and backup orchestration.
3. **Gate T-02 (Tax PoC):** Successful completion of `PoC-02` demonstrating independent statutory India GST e-invoicing and e-way bill generation.
4. **Gate T-03 (Concurrency PoC):** Successful completion of `PoC-03` proving stock ledger locking resilience and transactional integrity under defined peak load (Threshold TBD — OQ-015).
5. **Gate T-04 (Mobile PoC):** Successful completion of `PoC-04` demonstrating offline field service delta sync and conflict resolution.
6. **Gate S-01 (Executive Sign-off):** Formal ratification of the licensing model, tenancy topology, and commercial roadmap by the KIYA Executive Committee.

---

## 12. Next Phase Authorization

Upon formal acceptance of this Phase 1B evaluation baseline:

- **Next Authorized Phase:** **PHASE 1C — TARGET ARCHITECTURE DEFINITION**
- **Phase 1C Immediate Scope:**
  1. Author `docs/02-architecture/04-target-architecture-definition.md` detailing the logical component topology, application boundaries, and data synchronization patterns for the provisional architecture.
  2. Formally specify the technical contracts, interface protocols, and governance boundaries for the 8 KIYA-owned strategic seams.
  3. Define the concrete execution test plans and harness requirements for `PoC-01`, `PoC-02`, `PoC-03`, and `PoC-04`.
  4. Author Architectural Decision Record `ADR-001` with status `PROPOSED / CONDITIONAL`.

`[FINAL-GOVERNANCE-STOP]` Phase 1B is hereby concluded. Production coding, physical database design, API authoring, UI wireframing, and PoC code execution remain strictly out of scope until authorized in subsequent phases.
