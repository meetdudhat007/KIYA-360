# KIYA 360 — Phase 1 Architecture Risk Register

- **Document ID:** `ARCH-09`
- **Phase:** Phase 1 Governance — Architecture Risk Register
- **Status:** `REVIEW-READY BASELINE`
- **Date:** 14 September 2026
- **Authors:** Principal Enterprise Architect, Solution Architect, Risk & Governance Lead
- **Governing Architecture:** `docs/02-architecture/04-target-architecture.md` (Phase 1C)
- **Validation Baseline:** `docs/02-architecture/08-phase-1-validation-and-poc-register.md`

---

## 1. Executive Summary & Risk Governance

This register identifies, classifies, and evaluates the principal architectural and technical risks facing the KIYA 360 platform. 

In strict adherence to Phase 1 governance:
1. **Qualitative Risk Evaluation:** All risks are evaluated using qualitative **Likelihood (High / Medium / Low)** and **Impact (High / Medium / Low)** ratings based on architectural analysis and prior repository evidence.
2. **Defensible Mitigations:** Every risk is paired with concrete architectural mitigations, defined ownership, and allocated resolution phases.
3. **Evidence-Controlled Classifications:** Risks arising from open questions or candidate framework evaluations are made explicitly visible without unsupported certainty.

---

## 2. Architecture Risk Heat Map Summary

```
        ▲
        │  [RSK-02: Framework Coupling]     [RSK-03: GPL Licensing Gate]
   HIGH │  [RSK-04: India Tax Complexity]   [RSK-05: Mobile Offline Sync]
        │
I       │
M       │  [RSK-01: Multi-Module Dependency] [RSK-06: Financial Integrity]
P  MED  │  [RSK-08: Multi-Tenant Leakage]    [RSK-10: Statutory Integrations]
A       │  [RSK-13: Upstream Upgrade Risk]   [RSK-11: BI/EPM Scaling]
C       │
T       │  [RSK-09: AI Hallucination Risk]   [RSK-07: Cross-Module Trans]
   LOW  │  [RSK-12: Cloud Deployment Cost]   [RSK-14: Schema Complexity]
        │
        └─────────────────────────────────────────────────────────────►
                  LOW                   MEDIUM                  HIGH
                                   L I K E L I H O O D
```

---

## 3. Comprehensive Architecture Risk Register

| Risk ID | Risk Category | Risk Title & Description | Cause | Consequence | Likelihood | Impact | Overall Severity | Mitigation Strategy | Owner | Phase Addressed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Dependency Risk | **Cross-Module Dependency Cascades** | Interdependence across 28 modules and 3 core business flows. | Change in one upstream module (e.g., Sales Pricing) unexpectedly breaks downstream billing or inventory. | **Medium** | **High** | **HIGH** | Strict domain boundary encapsulation; explicit event and data contracts; integration test suites. | Solution Architect | Phase 1D / Phase 2 |
| **RSK-02** | Coupling Risk | **Tight Coupling to ERPNext Internals** | Directly subclassing or extending upstream ERPNext Python classes and DocTypes. | KIYA becomes locked into ERPNext implementation quirks, preventing future refactoring or platform migration. | **High** | **High** | **CRITICAL** | Enforce anti-corruption layer (`ADR-004`) and 8 Strategic Seams; forbid direct core modifications; treat ERPNext as an implementation detail under evaluation. | Principal Architect | Phase 1E / Phase 2 |
| **RSK-03** | Licensing Risk | **GPLv3 License Copyleft Uncertainty on Proprietary IP** | Legal ambiguity regarding derivative work status under GPLv3 when combining Frappe (MIT) and ERPNext (GPLv3). | Legal risk to commercial SaaS model or requirement to release proprietary KIYA code. | **Medium** | **High** | **HIGH** | Mandatory Legal Review Gate `Gate L-01`; complete isolation of proprietary apps; maintain Candidate D (Clean-Room Custom) as evaluated fallback option. | Corporate Legal / Executive Board | Phase 1 / Phase 2 Gate |
| **RSK-04** | Statutory Risk | **Statutory Tax Engine Implementation Complexity** | Complex HSN/SAC rules, dynamic e-invoicing and e-way bill schema updates from tax authorities. | Inability to issue legal tax invoices; business stoppage for enterprise clients; regulatory penalties. | **High** | **High** | **CRITICAL** | Abstract Tax & Statutory Compliance (`MOD-18`); sandbox integration validation in `PoC-02`; pluggable statutory payload generators. | Compliance Lead / Architect | Phase 1C / Phase 2 |
| **RSK-05** | Complexity Risk | **Mobile Offline Data Collisions & Sync Failures** | Field service engineers and sales reps operating offline for extended durations, mutating shared entity states. | Data loss, overwriting concurrent server updates, corrupted inventory levels in mobile vans. | **High** | **High** | **CRITICAL** | Client-generated UUIDs; outbox sync pattern; deterministic conflict resolution rules (`PoC-04`); immutable audit logs. | Mobile Architect | Phase 1C / Phase 2 |
| **RSK-06** | Integrity Risk | **Financial Posting Imbalance or Ledger Corruption** | Unhandled exceptions or race conditions during multi-step operational transactions (e.g., dispatch billing). | Unbalanced General Ledger; audit failure; inaccurate financial statements; loss of enterprise client trust. | **Low** | **High** | **HIGH** | Atomic double-entry balancing validation (`L05`); immutable reversing entries (`DEC-009`); closed period locks; automated balance test suites. | Lead Financial Architect | Phase 1C / Phase 2 |
| **RSK-07** | Transaction Risk | **Cross-Module Transaction Boundary Failures** | Inconsistent business status propagation across asynchronous operational boundaries. | Orders marked as dispatched while inventory was never decremented; invoices issued without matching receipts. | **Medium** | **Medium** | **MEDIUM** | Strict single-source master data (`ADR-002`); two-phase inventory reservation; mandatory 3-way matching rules. | Integration Architect | Phase 1D / Phase 2 |
| **RSK-08** | Security Risk | **Multi-Tenant Data Leakage** | Bug in application-layer query filtering or shared caching layer. | Tenant A accesses Tenant B's confidential pricing, customer lists, or financial journals; severe regulatory breach. | **Low** | **High** | **HIGH** | Provisionally evaluate Database-per-Tenant isolation (`ADR-005`); independent site routing; automated query penetration testing (`PoC-01`). | Information Security Lead | Phase 1C / Phase 2 |
| **RSK-09** | Governance Risk | **AI Model Hallucination & Autonomous Execution** | Generative AI models making unverified operational commitments or unauthorized ledger postings. | Incorrect commercial discounts, invalid inventory allocations, financial statement distortions. | **Medium** | **Medium** | **MEDIUM** | Invariant AI Safety Guardrail: Zero direct database writes; AI outputs restricted to draft proposals requiring human-in-the-loop review. | AI Governance Lead | Phase 1C / Phase 2 |
| **RSK-10** | Integration Risk | **External Banking & Government Portal Downtime** | Unscheduled downtime or throttling by statutory e-invoice servers, e-Way portals, or commercial bank APIs. | Operational bottlenecks; users unable to finalize invoices or dispatches during peak hours. | **High** | **Medium** | **HIGH** | Circuit breakers; asynchronous retry queues with exponential backoff; offline queueing of dispatch payloads. | Platform Operations Lead | Phase 1E / Phase 2 |
| **RSK-11** | Performance Risk | **BI & Reporting Starvation of Operational OLTP** | Complex analytical queries, multi-year financial consolidations, or heavy reports executed on live OLTP tables. | Database lock contention, interactive UI lag, request timeouts during month-end financial closing. | **Medium** | **Medium** | **MEDIUM** | Asynchronous decoupling (`ADR-006`); route analytical reporting to near-real-time read replicas and dedicated data marts. | Database Architect | Phase 1C / Phase 1E |
| **RSK-12** | Operational Risk | **Deployment Sprawl & Infrastructure Sizing Overhead** | Premature over-provisioning or excessive operational complexity from unneeded microservices. | High infrastructure cloud costs; complex container orchestration overhead for early deployments. | **Low** | **Medium** | **LOW** | Unified modular platform deployment topology (`ARCH-06`); stateless web tiers; deferred hyperscaler lock-in until Phase 2 benchmarking. | DevOps Lead | Phase 1E / Phase 2 |
| **RSK-13** | Maintenance Risk | **Upstream Framework Upgrade Breakage** | Incompatible database schema or hook changes introduced by upstream Frappe or ERPNext framework updates. | Inability to apply critical security patches without breaking bespoke KIYA functionality. | **Medium** | **Medium** | **MEDIUM** | Forbid core modifications; implement custom behavior exclusively in isolated KIYA apps; automated upgrade regression pipeline. | Technical Lead | Phase 1E / Phase 2 |
| **RSK-14** | Data Model Risk | **Master Data Schema Inconsistency & Duplication** | Different development teams creating separate entity models for Customer, Supplier, or Warehouse. | Fragmented customer profiles; broken Customer 360 reporting; impossible cross-module traceability. | **Low** | **Medium** | **LOW** | Authoritative Master Data Ownership Matrix (`ARCH-05`); centrally governed data dictionaries; mandatory architecture review for new entities. | Enterprise Data Architect | Phase 1D / Phase 2 |

---

## 4. Conclusion & Risk Monitoring

The Phase 1 Architecture Risk Register provides complete visibility into the critical technical, legal, and operational risks facing KIYA 360. All high-severity risks have concrete, active mitigations integrated directly into the Target Architecture, the Validation Register (`ARCH-08`), and the Phase 2 plan.
