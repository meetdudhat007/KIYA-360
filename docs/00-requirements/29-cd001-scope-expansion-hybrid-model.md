# KIYA 360 — Clarification Decision Record: CD-001

## 1. Decision Header & Control Information

- **Decision ID:** `CD-001`
- **Related Open Question ID:** `OQ-001` (`docs/00-requirements/06-open-questions.md` §1)
- **Title:** Scope Expansion Governance for Modules 02–28: Core-Flow Hybrid Model
- **Status:** **APPROVED**
- **Priority / Blocking:** CRITICAL / Formally Resolved for Phase 0B-2 Authoring
- **Clarification Group:** `CG-01` (Scope and Shared-Data Baseline)
- **Clarification Session ID:** `CS-CG01-01`
- **Date Created:** 14 September 2026
- **Approval Date:** 14 September 2026
- **Approving Authority:** Business Leadership & Executive Product Sponsor
- **Durable Evidence Reference:** Stakeholder Decision Direction for Critical Clarification Group CG-01 (14 September 2026); BRD v2.0 §3.1, §3.2, §6, §7.2–§7.28.
- **Supersedes / Superseded By:** None / Initial Record

---

## 2. Problem Statement & Ambiguity Context

In `source/KIYA360_BRD.pdf`, Section 7.1 (Platform & Administration) provides granular, numbered functional requirements, whereas Sections 7.2 through 7.28 list sub-module names with high-level narratives and state that detailed design must expand them. Prior to this decision, the project lacked an approved methodology for bounding detailed requirements expansion in Phase 0B-2 without either stalling delivery through exhaustive bespoke documentation or failing enterprise compliance through unguided assumptions.

---

## 3. Authoritative Stakeholder Decision

The authoritative stakeholder direction for `OQ-001` is formally recorded as follows:

> **STAKEHOLDER DECISION STATEMENT (CD-001):**
> 
> Use a **HYBRID scope-expansion approach** for KIYA 360 detailed requirements authoring:
> 
> 1. **Core Business Flows Full Detailing:** The project must fully detail the complete BRD-defined core business flows, specifically:
>    - **Customer-to-Cash (C2C)** (Stages 1–18; BRD §6.1)
>    - **Procure-to-Pay (P2P)** (Stages 1–12; BRD §6.2)
>    - **Asset-to-Service (A2S)** (Stages 1–11; BRD §6.3)
> 
> 2. **Standard ERP Reference Baseline:** For standard enterprise/ERP behavior that is not explicitly specified by the BRD, use proven ERP-standard behavior as the reference baseline where appropriate.
> 
> 3. **Mandatory Governance Guardrails:**
>    - ERPNext behavior must **NOT** automatically become a KIYA requirement.
>    - KIYA-specific requirements and differentiators must remain explicitly defined.
>    - Any ERP-standard behavior adopted for KIYA must be traceable as a reference baseline.
>    - KIYA-specific exceptions must be explicitly documented.
>    - The approach should prioritize delivery speed without sacrificing traceability.

---

## 4. Known Facts & Bounded Scope

- **BRD Fidelity:** Preserves the complete 28-module enterprise platform scope defined in BRD §3.1 and Phase 1 exclusions in BRD §3.2.
- **Core Flows Priority:** Establishes Customer-to-Cash, Procure-to-Pay, and Asset-to-Service as the first-order priority for exhaustive functional expansion under Phase 0B-2.
- **Traceability Standard:** When ERP-standard mechanisms are referenced (utilizing `docs/00-requirements/21`–`27` as reference material), they must carry explicit traceability tags (`BRD-DERIVED` or `ERPNext-REFERENCE`) and be formally vetted against KIYA requirements.

---

## 5. Scope & Impact Analysis

- **Affected Modules:** All 28 modules, prioritizing modules directly involved in C2C, P2P, and A2S:
  - CRM, Sales, Inventory, Warehouse, Manufacturing, MRP & Planning, Quality, Asset Management, Maintenance & Field Service, Procurement, Supplier Management, Finance & Accounting, and Tax & Statutory Compliance.
- **Affected Requirements:** All baseline functional requirement records (FR-CRM-001 through FR-ASC-007; 238 records).
- **Affected Business Flows:** Customer-to-Cash, Procure-to-Pay, Asset-to-Service.
- **Affected Shared Foundations:** All shared foundations (`SF-001` through `SF-015`), especially Master Data Governance (`SF-003`), Unified Data Model (`SF-004`), and Universal Approvals (`SF-005`).
- **Dependencies Unblocked:** Unblocks the authoring of detailed requirements across `DEP-001` through `DEP-008`.

---

## 6. Unknowns, Risks, and Unresolved Portions

- **Module Exception Inventories:** Specific KIYA exceptions to standard ERP workflows for peripheral sub-modules (e.g., advanced marketing journeys, e-commerce marketplace sync) remain to be cataloged during module-level Phase 0B-2 authoring.
- **Clarification Decoupling:** Non-flow open questions (e.g., `OQ-005` tax jurisdictions, `OQ-006` payroll scope, `OQ-013` mobile offline, `OQ-014` AI boundaries, `OQ-015` measurable NFRs) remain open and will be resolved in their respective clarification groups (`CG-03` through `CG-07`).

---

## 7. Downstream Authorization & Requirements Strategy Alignment

- **Phase 0B-2 Authorization:** The project is now formally authorized to initiate Phase 0B-2 (Detailed Requirements Expansion) using the hybrid flow-first methodology governed by this decision.
- **Requirement Lifecycle Status:** Detailed requirements for modules 02–28 may now transition from `Not Started` to `In Analysis` / `Draft` following `10-detailed-requirements-strategy.md`.

---

## 8. Approval Evidence & Sign-off

- **Approver Type:** Business Leadership & Executive Product Sponsor
- **Approval Decision:** APPROVED
- **Date:** 14 September 2026
- **Evidence:** Stakeholder Clarification Review CS-CG01-01 / Formal Stakeholder Direction recorded in project repository.
