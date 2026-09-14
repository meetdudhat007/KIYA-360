# KIYA 360 — Clarification Decision Record: CD-002

## 1. Decision Header & Control Information

- **Decision ID:** `CD-002`
- **Related Open Question ID:** `OQ-002` (`docs/00-requirements/06-open-questions.md` §2)
- **Title:** Transactional Lifecycle & Status Governance: Operational Business Status Model
- **Status:** **APPROVED**
- **Priority / Blocking:** CRITICAL / Formally Resolved for Lifecycle Architecture Baseline
- **Clarification Group:** `CG-01` (Scope and Shared-Data Baseline)
- **Clarification Session ID:** `CS-CG01-01`
- **Date Created:** 14 September 2026
- **Approval Date:** 14 September 2026
- **Approving Authority:** Business Leadership, Platform Architecture & Product Ownership
- **Durable Evidence Reference:** Stakeholder Decision Direction for Critical Clarification Group CG-01 (14 September 2026); BRD v2.0 §6, §7.1, §10; DEC-007.
- **Supersedes / Superseded By:** None / Initial Record

---

## 2. Problem Statement & Ambiguity Context

While BRD §10 mandates a Unified Data Model (`DEC-007`) with no duplicate master data, it does not define record fields, validation rules, or status progressions for transactional documents and master data entities. Furthermore, architectural analysis of the ERPNext reference baseline (`docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` §Shared Mechanics) identified a technical dual-state model (`docstatus` 0/1/2 combined with computed `status`). Prior to this decision, the project lacked an approved policy regarding whether to adopt ERPNext's dual framework lifecycle or establish a KIYA-specific operational status model.

---

## 3. Authoritative Stakeholder Decision

The authoritative stakeholder direction for `OQ-002` is formally recorded as follows:

> **STAKEHOLDER DECISION STATEMENT (CD-002):**
> 
> 1. **Primary Lifecycle Model:** Use **BUSINESS STATUS** as the primary transactional lifecycle and status model for KIYA 360.
> 
> 2. **Explicit ERPNext Separation:** Do **NOT** adopt ERPNext's Draft/Submitted/Cancelled dual-state (`docstatus`) model as a KIYA requirement.
> 
> 3. **Operational Representation:** Business Status must directly represent the operational and business lifecycle of transactions (e.g., commercial progression, fulfillment milestones, and financial standing).
> 
> 4. **No Premature Invention:** Detailed status values must **NOT** be invented yet unless explicitly supported by the BRD or specifically required for an immediate detailed design task. Detailed status definitions will be established progressively during detailed requirements authoring (Phase 0B-2).

---

## 4. Known Facts & Bounded Scope

- **Business Fidelity:** Rejects the mechanical imposition of external framework concepts (`docstatus`) on business users, aligning with KIYA's commitment to clean, enterprise-grade business interfaces.
- **Audit & Reversal Integrity:** While rejecting ERPNext's specific `docstatus` implementation, transactional cancellations and financial voiding must continue to adhere to immutable audit and reversal principles (`FR-PADM-1.4.1`, `DEC-007`).
- **Progressive Elaboration:** Explicitly bounds this decision to lifecycle architecture governance, leaving document-by-document status enumerations to be specified during Phase 0B-2 module workflows.

---

## 5. Scope & Impact Analysis

- **Affected Modules:** All 28 modules across all transactional entities (e.g., Lead, Opportunity, Enquiry, Quotation, Sales Order, Delivery Note, Sales Invoice, Payment, Material Request, RFQ, RFP, Purchase Order, Goods Receipt, Work Order, Job Card, Service Request, Field Service Work Order).
- **Affected Requirements:** All master and transaction capabilities across Modules 01–28.
- **Affected Business Flows:** Customer-to-Cash, Procure-to-Pay, Asset-to-Service.
- **Affected Shared Foundations:** `SF-003` (Master Data Governance), `SF-004` (Unified Data Model), `SF-005` (Universal Approvals), `SF-013` (Document Numbering), `SF-014` (Common Platform Actions).
- **Dependencies Unblocked:** Unblocks data schema modeling, status progression rules, and state machine design across `DEP-001` through `DEP-011`.

---

## 6. Unknowns, Risks, and Unresolved Portions

- **Specific Status Enumerations:** The exact list of valid status values, transition rules, and validation triggers for individual document types (e.g., Quotation statuses, Purchase Order statuses) remain `TBD` and will be defined during Phase 0B-2 detailed requirements expansion.
- **Field-Level Data Dictionaries:** Mandatory fields, data types, and cross-module link references remain to be authored in Phase 0B-2 data modeling artifacts.

---

## 7. Downstream Authorization & Requirements Strategy Alignment

- **Phase 0B-2 State Modeling:** Requirements authors are instructed to design single-model business status progressions for all transactions, avoiding coupling to Frappe/ERPNext framework-specific flags.
- **Reversals via Business States:** Cancellation must be modeled as an explicit business status (e.g., `Cancelled`, `Voided`, `Reversed`) accompanied by traceable reversing transactions.

---

## 8. Approval Evidence & Sign-off

- **Approver Type:** Business Leadership, Platform Architecture & Product Ownership
- **Approval Decision:** APPROVED
- **Date:** 14 September 2026
- **Evidence:** Stakeholder Clarification Review CS-CG01-01 / Formal Stakeholder Direction recorded in project repository.
