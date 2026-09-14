# KIYA 360 — Critical Clarification Group CG-01 Stakeholder Clarification Package

## 1. Document Control, Purpose, and Governance Scope

- **Document ID:** `28-cg01-stakeholder-clarification-package`
- **Clarification Group:** `CG-01` (Scope and Shared-Data Baseline)
- **Included Open Questions:** `OQ-001` and `OQ-002`
- **Phase:** Phase 0B-1D / Phase 0B-2 Bridge (Clarification Preparation)
- **Status:** **PREPARED FOR STAKEHOLDER SESSION** (Questions remain completely unresolved; no business decision is approved)
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026)
- **Governance Framework:** `AGENTS.md`, `.kiya/AI-CONTEXT.md`, `.kiya/AI-DECISIONS.md`, `docs/00-requirements/15-critical-clarification-plan.md`, `docs/00-requirements/16-clarification-decision-register.md`, `docs/00-requirements/17-clarification-decision-template.md`

### 1.1 Purpose
This package provides a business-ready, evidence-based instrument for executive leadership, product owners, and functional stakeholders to clarify the foundational scope and data definitions of the KIYA 360 platform.
- **The purpose of this document is NOT to answer the questions.**
- **The purpose is to articulate the exact ambiguities, present genuine evidence-backed alternatives, explain the downstream architectural impact, and formulate precise, unambiguous stakeholder questions.**
- Stakeholder answers captured during the forthcoming session will be formally processed through the `CD-###` Clarification Decision governance framework (`docs/00-requirements/16-clarification-decision-register.md`).

### 1.2 Anti-Hallucination and Authority Boundaries
1. **Source Hierarchy:**
   - Primary Authority: KIYA 360 BRD v2.0 (`source/KIYA360_BRD.pdf`).
   - Project Governance Baseline: Approved requirements (`docs/00-requirements/01`–`14`), clarification framework (`docs/00-requirements/15`–`17`), and approved project decisions (`.kiya/AI-DECISIONS.md`).
   - Reference Baseline: ERPNext reverse-engineering analysis (`docs/00-requirements/21`–`27`) is consulted **strictly as an external reference system** illustrating mature ERP behavior. ERPNext behavior must **NEVER** automatically become a KIYA requirement.
2. **AI Restrictions:** AI engineering assistants are strictly prohibited from inventing stakeholder intent, assuming business answers, approving decisions, or marking `OQ-001` / `OQ-002` as resolved.
3. **Handling of Insufficient Information:** Where BRD v2.0 does not specify a detail, it is recorded explicitly as `TBD — insufficient evidence`.

---

## 2. Clarification Group CG-01 Strategic Context

Clarification Group `CG-01` is designated as **Priority: CRITICAL** and **Status: BLOCKING** in `docs/00-requirements/15-critical-clarification-plan.md`:
- It governs the foundational requirements for the entire platform.
- It sits at the root of all 11 critical cross-module dependencies (`DEP-001` through `DEP-011`).
- **No detailed requirement expansion (Phase 0B-2) or application implementation can safely be approved until the scope boundary (OQ-001) and conceptual data lifecycle (OQ-002) are formally clarified by authorized stakeholders.**

---

## 3. OQ-001 Detailed Clarification Analysis

### 3.1 Authoritative Definition and Problem Statement
- **Open Question ID:** `OQ-001`
- **Authoritative Text (`docs/00-requirements/06-open-questions.md` §1):**
  > *"What detailed requirements beyond the listed sub-module names apply to modules 02–28?"*
- **The Exact Ambiguity:**
  In `source/KIYA360_BRD.pdf`, Section 7.1 (Platform & Administration) contains granular, numbered functional requirements (FR-PADM-1.1.1 through FR-PADM-1.8.6). In stark contrast, Sections 7.2 through 7.28 (covering CRM, Sales, Marketing, Customer Service, Procurement, Supplier Management, Inventory, Warehouse, Manufacturing, MRP, Quality, Assets, Maintenance/Field Service, Logistics, Projects, Finance/Accounting, Tax, HR/Payroll, E-Commerce, DMS, BI, EPM, Workflow, AI, Integration, Mobile, and Audit) list only module titles, high-level narratives, and bulleted sub-module names. Furthermore, the BRD explicitly states in each section that detailed design must expand these modules.
  Because the BRD specifies the *what* at a capability level but does not define the *how much* or the exact operational depth for Phase 1, the boundaries of project delivery, testing, and acceptance are currently unconstrained.

### 3.2 BRD Evidence and Known Facts
- **BRD §3.1:** Establishes the full enterprise scope across 28 modules.
- **BRD §3.2:** Explicitly excludes certain domains from Phase 1 (e.g., process manufacturing, multi-country payroll beyond India + 1 reference country, complex offshore corporate structures).
- **BRD §7.2–§7.28:** Defines 238 functional requirement baseline records across modules 02–28, but formats them as sub-module capability headers rather than detailed functional specifications.
- **Known Fact:** The BRD commits to a broad 28-module enterprise platform in Phase 1, but does not provide field-level or scenario-level acceptance criteria for modules 02–28.

### 3.3 Affected Scope Across the Platform
- **Affected Modules:** Modules 02 through 28 (27 of the 28 modules).
- **Affected Requirements:** All baseline functional requirements outside Platform & Administration (FR-CRM-001 through FR-ASC-007; 238 requirement records).
- **Affected Business Flows:**
  - Customer-to-Cash (C2C): Stages 1–18.
  - Procure-to-Pay (P2P): Stages 1–12.
  - Asset-to-Service (A2S): Stages 1–11.
- **Affected Shared Foundations:** All 15 Shared Foundation capabilities (`SF-001` through `SF-015`), particularly Multi-Tenancy (`SF-001`), Master Data Governance (`SF-003`), Unified Data Model (`SF-004`), and Universal Approvals (`SF-005`).
- **Constrained Dependencies:** Directly blocks `DEP-001` (Lead-to-Order), `DEP-002` (Order-to-Fulfillment), `DEP-003` (Order-to-MRP), `DEP-004` (MRP-to-PO), `DEP-005` (Invoicing-to-Tax), `DEP-006` (Goods Receipt-to-Inspection), `DEP-007` (Asset-to-Maintenance), `DEP-008` (Project-to-Invoicing), `DEP-009` (Mobile Synchronization), `DEP-010` (Workflow Engine), and `DEP-011` (Audit & Security).

### 3.4 Genuine Evidence-Backed Interpretations & Alternatives

To assist stakeholders, three legitimate interpretations supported by the BRD evidence and project constraints are identified:

#### Alternative 1A: Comprehensive Greenfield Specification
- **Description:** Business stakeholders author and approve exhaustive, ground-up functional specifications for all sub-modules in Modules 02–28 prior to approving detailed requirements or commencing development.
- **BRD Evidence / Alignment:** Aligns with BRD §7.2–§7.28 text stating detailed design must expand every sub-module.
- **Consequences:** Maximum business customization and absolute fidelity to proprietary stakeholder workflows.
- **Downstream Trade-offs:** Very high initial documentation burden; significantly delays Phase 0B completion; risks duplicating industry-standard ERP mechanics from scratch.
- **What Remains Unknown:** Exact timelines, authoring resources, and detailed business rules for hundreds of sub-modules.

#### Alternative 1B: Core-Flow-Driven Phased Expansion (Flow-First)
- **Description:** Prioritize detailed functional expansion strictly around the 3 primary BRD business flows (Customer-to-Cash, Procure-to-Pay, Asset-to-Service) and their supporting modules. Sub-modules that do not touch the core transactional spine (e.g., advanced marketing attribution, niche AI, complex logistics route planning) remain bounded at the BRD baseline level for Phase 1.
- **BRD Evidence / Alignment:** Aligns directly with BRD §6, which elevates C2C, P2P, and A2S as the core business flows of the platform, and BRD §3.2 exclusions.
- **Consequences:** Accelerates delivery of the operational core; unblocks transaction processing while containing scope creep in peripheral modules.
- **Downstream Trade-offs:** Leaves peripheral modules (e.g., Marketing, E-Commerce, Field Service advanced dispatch) at baseline sub-module scope during initial release.
- **What Remains Unknown:** Specific cut-off criteria for which sub-modules are deemed core vs. peripheral.

#### Alternative 1C: Reference-Baseline Alignment (Standard-First with Exception Specification)
- **Description:** Formally adopt proven enterprise ERP baseline behaviors (such as the standard transactional workflows cataloged in Document 26) as the default functional specification for standard transactions, requiring stakeholders to specify only proprietary KIYA differentiators, gaps, and custom workflows (e.g., Enquiry document, RFP sourcing, WMS physical locations, India GST).
- **BRD Evidence / Alignment:** Aligns with BRD §1.2 enterprise positioning (competing with Tier-1/2 ERPs) and minimizes unnecessary re-invention of commodity accounting/inventory mechanics.
- **Consequences:** Drastically compresses time-to-market; leverages proven double-entry GL, perpetual inventory, and discrete BOM manufacturing.
- **Downstream Trade-offs:** Requires stakeholders to formally review and accept reference functional patterns; risks adopting ERPNext structural assumptions if not tightly isolated.
- **What Remains Unknown:** Explicit list of business processes where KIYA strictly refuses standard ERP conventions.

### 3.5 Stakeholder Clarification Question: OQ-001

> **STAKEHOLDER QUESTION (OQ-001):**
> *"How should the project team expand the detailed functional scope for Modules 02–28 to enable formal sign-off and downstream development?"*
> 
> - **Option A (Comprehensive Custom Expansion):** Require full, bespoke functional specifications for all 238 sub-module areas across all 28 modules before approving detailed requirements.
> - **Option B (Core-Flow Phased Expansion - Recommended):** Prioritize exhaustive, detailed specification for the modules directly driving Customer-to-Cash, Procure-to-Pay, and Asset-to-Service, while retaining baseline capability definitions for secondary modules in Phase 1.
> - **Option C (Standard Reference Baseline with Custom Exceptions):** Adopt mature, standard ERP transactional baselines (as cataloged in the ERP reference analysis) for standard GL, inventory, and procurement, focusing stakeholder specification strictly on identified KIYA gaps (Enquiry, RFP, Physical WMS, India GST, AI, and Customer Equipment).

---

## 4. OQ-002 Detailed Clarification Analysis

### 4.1 Authoritative Definition and Problem Statement
- **Open Question ID:** `OQ-002`
- **Authoritative Text (`docs/00-requirements/06-open-questions.md` §2):**
  > *"What data fields, validation rules, and status values apply to each master and transaction?"*
- **The Exact Ambiguity:**
  The BRD mandates a Unified Data Model (`DEC-007`, BRD §10) with zero duplicate master data across CRM, ERP, and back-office modules. It lists conceptual entities (Customer, Supplier, Item, Warehouse, Lead, Opportunity, Sales Order, Invoice, Payment, Asset). However, the BRD **does not specify**:
  1. Record-level field dictionaries and required validations.
  2. Document lifecycle states (e.g., What are the exact valid statuses for a Sales Order, Quotation, or Work Order?).
  3. Master data ownership and cross-module synchronization boundaries.
  4. Cancellation, voiding, and reversal policies across transactions (e.g., Under what conditions can a submitted Sales Order or Goods Receipt be cancelled, and what are the exact reversal side-effects?).

### 4.2 BRD Evidence and Known Facts
- **BRD §10 (NFRs):** Requires a unified data model, single source of truth, and auditability.
- **BRD §7.1 (Platform & Administration):** FR-PADM-1.4.1 requires system-wide audit logging of all data changes.
- **BRD §6 (Business Flows):** Defines sequential transaction handoffs (e.g., Quotation → Sales Order → Dispatch → Invoice), implying lifecycle progression.
- **Known Fact:** The BRD provides conceptual entity names and flow sequences, but provides no data dictionaries, status enumerations, state transition matrices, or cancellation policies.

### 4.3 Affected Scope Across the Platform
- **Affected Modules:** All 28 modules.
- **Affected Requirements:** Every transaction and master capability across the platform.
- **Affected Business Flows:** All stages of C2C, P2P, and A2S.
- **Affected Shared Foundations:** `SF-003` (Master Data Governance), `SF-004` (Unified Data Model), `SF-013` (Document Numbering), `SF-014` (Common Platform Actions: Create, Edit, View, Submit, Cancel, Print).
- **Constrained Dependencies:** Directly blocks all data schema definitions, API contract designs, validation engine development, and workflow state machines.

### 4.4 Genuine Evidence-Backed Interpretations & Alternatives

#### Alternative 2A: Dual-State Model (Framework Submission + Dynamic Business Status)
- **Description:** Adopt a two-tier lifecycle model:
  1. *Document Commitment State:* Standardized platform states: `Draft` (editable, no ledger impact), `Submitted` (locked/posted, ledger impact posted), and `Cancelled` (voided, reverse ledger posted).
  2. *Business Milestone State:* Dynamic sub-status tracking operational progress (e.g., a submitted Sales Order has business statuses: `To Deliver and Bill`, `Partially Delivered`, `Fully Delivered`, `Completed`, `Closed`, `On Hold`).
- **Evidence / Context:** Observed in mature enterprise platforms (documented as `ERPNext-REFERENCE` in Doc 21 §Shared Mechanics and Doc 26 §2.1).
- **Consequences:** Provides clean architectural separation between financial ledger commitment and operational stage tracking; enables robust cancellation via automated reversal entries.
- **Downstream Trade-offs:** Requires users to understand the distinction between document submission and operational completion.
- **What Remains Unknown:** Specific allowed status transitions per transaction type in KIYA.

#### Alternative 2B: Single Unified Lifecycle State Machine
- **Description:** Every master and transaction possesses a single, linear enumerated status field (e.g., Sales Order: `Draft` → `Pending Approval` → `Approved` → `Confirmed` → `In Picking` → `Dispatched` → `Invoiced` → `Paid` → `Closed` / `Cancelled`).
- **Evidence / Context:** Traditional custom-built business software pattern; aligns with high-level user expectation of a single status badge.
- **Consequences:** Simple and intuitive for end users to view on list pages.
- **Downstream Trade-offs:** Highly rigid; struggles with parallel operational milestones (e.g., an order that is 100% delivered but 0% billed cannot be represented cleanly on a single linear track); requires complex custom rollback logic on cancellation.
- **What Remains Unknown:** Exact state transition diagrams and exception paths for all 50+ business documents.

#### Alternative 2C: Phased Conceptual Baseline (Core Masters First, Dynamic Transaction States)
- **Description:** Establish an immediate approved baseline for primary Master Data entities (`Customer`, `Supplier`, `Item`, `Warehouse`, `Company`, `Chart of Accounts`), while defining transactions through a standardized state lifecycle contract (`Draft` → `Active/Submitted` → `Completed` / `Cancelled`) with configurable milestone tags.
- **Evidence / Context:** Directly satisfies `DEC-007` (Unified Data Model) while deferring non-critical edge-case status enumerations to module-level workshops.
- **Consequences:** Unblocks database and API foundation work immediately; guarantees master data consistency across CRM and ERP.
- **Downstream Trade-offs:** Transaction status details must be finalized during individual functional clarification sessions (CG-04, CG-05).
- **What Remains Unknown:** Field-level validation rules for secondary transactions.

### 4.5 Stakeholder Clarification Question: OQ-002

> **STAKEHOLDER QUESTION (OQ-002):**
> *"What architectural lifecycle and status governance model should KIYA 360 establish for transactional documents and master data?"*
> 
> - **Option A (Dual-State Model - Recommended):** Adopt a dual-state architecture separating financial/document commitment (`Draft` / `Submitted` / `Cancelled`) from operational business progress (`Pending`, `Partially Fulfilled`, `Completed`, `On Hold`), with mandatory reversal entries for cancellations.
> - **Option B (Single Linear State Machine):** Enforce a single, unified status progression for each document type, requiring an exhaustive state-machine specification for every document before implementation.
> - **Option C (Core Master Freeze with Configurable Transaction States):** Immediately define and freeze core Master Data schemas (Customer, Vendor, Product, Facility, Account), while allowing transactional workflows to use a standardized status template governed by the workflow engine.

---

## 5. Dependency & Blocking Impact Summary

The resolution of `CG-01` (`OQ-001` and `OQ-002`) dictates the execution order of the remaining clarification groups:

```
[CG-01: Scope & Shared Data (OQ-001, OQ-002)] <--- YOU ARE HERE (CRITICAL / BLOCKING)
       |
       +---> [CG-02: Workflow & Approvals (OQ-003, OQ-004)]
       |
       +---> [CG-03: Finance, Tax & Payroll (OQ-005, OQ-006)]
       |
       +---> [CG-04: Supply, Mfg, Quality & Scorecard (OQ-007, OQ-008, OQ-009, OQ-010)]
       |
       +---> [CG-05: Asset-to-Service Behavior (OQ-011)]
       |
       +---> [CG-06: Digital Enablers: Mobile, AI, Integrations (OQ-012, OQ-013, OQ-014)]
       |
       +---> [CG-07: Measurable NFR Targets (OQ-015)]
```

- **If OQ-001 is resolved:** Requirements analysts can safely bound detailed specifications in Phase 0B-2 without risking scope rejection.
- **If OQ-002 is resolved:** Data architects can establish the platform-wide conceptual schema, entity relationship diagrams, and common API contracts without risking data model redesign.

---

## 6. Stakeholder Information & Decision Pre-requisites

Before providing formal decisions on `OQ-001` and `OQ-002`, stakeholders should consider:
1. **Commercial & Delivery Timelines:** Full greenfield specification (Option 1A) will require substantial time before engineering can begin, whereas phased or reference-first models (Options 1B/1C) permit rapid development of the core engine.
2. **Audit & Regulatory Rigor:** An enterprise platform serving public or regulated entities requires immutable audit trails and formal financial reversals (supporting Option 2A).
3. **Product Differentiation:** Focus bespoke design effort on KIYA differentiators (AI insights, unified CRM-to-ERP visibility, India GST statutory automation) rather than re-inventing standard journal entry posting rules.

---

## 7. Explicit Statements of What AI Must NOT Decide

In accordance with project governance (`AGENTS.md` and `.kiya/AI-DECISIONS.md`), the AI engineering assistant explicitly declares that it **CANNOT and WILL NOT**:
- Decide the functional scope boundary of any KIYA module.
- Select between Option A, B, or C for OQ-001 or OQ-002.
- Invent missing fields, validation rules, or status codes.
- Approve or sign off on a Clarification Decision (`CD-###`).
- Declare any open question resolved without an approved, durable stakeholder decision record.

---

## 8. Blank Answer-Capture Records (Governance Format)

The following blank templates are prepared for recording stakeholder input during the clarification session. In compliance with `16-clarification-decision-register.md`, the `Decision ID` (`CD-###`) remains blank until formally initiated by the governance process.

### 8.1 Answer Capture Record: OQ-001

```markdown
### Clarification Decision Capture: OQ-001
- **Decision ID:** CD-[TBD]
- **Related Open Question ID:** OQ-001
- **Title:** Scope Expansion Governance for Modules 02–28
- **Clarification Session ID:** [TBD - e.g., CS-CG01-01]
- **Session Date:** [TBD]
- **Participating Stakeholders:** [Names / Roles / Authority Types]
- **Selected Option / Stakeholder Answer:** [Option A / Option B / Option C / Custom Formulated Decision]
- **Exact Stakeholder Decision Text:**
  > [Insert verbatim stakeholder statement or approved policy text]
- **Decision Rationale:** [Why this option was chosen]
- **Scope & Affected Requirements:** [All modules 02–28 / Specific core modules]
- **Exceptions & Boundaries:** [List any specific exclusions or conditional overrides]
- **Decision Status:** PROPOSED (Pending formal sign-off)
- **Approving Authority Type:** [Business Leadership / Executive Product Sponsor]
- **Formal Sign-off Date:** [TBD]
- **Durable Evidence Reference:** [Meeting Minutes / Document Link / Signed Approval]
```

### 8.2 Answer Capture Record: OQ-002

```markdown
### Clarification Decision Capture: OQ-002
- **Decision ID:** CD-[TBD]
- **Related Open Question ID:** OQ-002
- **Title:** Platform Document Lifecycle, Status, and Data Schema Baseline
- **Clarification Session ID:** [TBD - e.g., CS-CG01-01]
- **Session Date:** [TBD]
- **Participating Stakeholders:** [Names / Roles / Authority Types]
- **Selected Option / Stakeholder Answer:** [Option A / Option B / Option C / Custom Formulated Decision]
- **Exact Stakeholder Decision Text:**
  > [Insert verbatim stakeholder statement or approved policy text]
- **Decision Rationale:** [Why this option was chosen]
- **Scope & Affected Requirements:** [All transactional documents and master data entities]
- **Cancellation & Reversal Policy Mandate:** [Explicit rule regarding reversals vs. hard deletion]
- **Exceptions & Boundaries:** [List any specific exceptions]
- **Decision Status:** PROPOSED (Pending formal sign-off)
- **Approving Authority Type:** [Platform Administrator / Enterprise Data Architect / Product Owner]
- **Formal Sign-off Date:** [TBD]
- **Durable Evidence Reference:** [Meeting Minutes / Document Link / Signed Approval]
```

---

## 9. Next Governance Steps After Stakeholder Answers

Once stakeholders provide answers using the capture format:
1. **Record Input:** Transcribe the answers into candidate decision records using `docs/00-requirements/17-clarification-decision-template.md`.
2. **Assign CD IDs:** Assign sequential identifiers (e.g., `CD-001` for OQ-001 scope, `CD-002` for OQ-002 lifecycle) in `docs/00-requirements/16-clarification-decision-register.md`.
3. **Execute Approval Gate:** Submit candidate records to the authorized stakeholder authority for formal `APPROVED` status sign-off.
4. **Update Requirements Baseline:** Trace approved decisions into `docs/00-requirements/05-requirement-traceability.md` and initiate detailed requirements authoring (Phase 0B-2) strictly within the approved scope boundaries.

---

## 10. Document Metadata

- **Prepared By:** Antigravity AI Engineering Assistant
- **Creation Date:** 14 September 2026
- **Status:** Complete / Ready for Session
- **Traceability Baseline:** `docs/00-requirements/06-open-questions.md`, `docs/00-requirements/15-critical-clarification-plan.md`
