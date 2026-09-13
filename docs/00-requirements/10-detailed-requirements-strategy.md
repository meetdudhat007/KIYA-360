# KIYA 360 — Detailed Requirements Strategy

## 1. Purpose

Phase 0A establishes the scope baseline, but most modules remain at capability/sub-module level. Phase 0B will clarify those requirements into consistent, reviewable specifications without converting gaps or common ERP practice into unsupported KIYA 360 business behavior.

## 2. Objectives

Phase 0B will expand the approved baseline incrementally; preserve BRD and Phase 0A traceability; expose gaps for business decisions; check end-to-end and common-platform consistency; and prepare observable acceptance criteria where the available evidence permits. It does not authorize solution design or implementation.

## 3. Requirements Expansion Philosophy

- **BRD-first:** begin from the current approved BRD and its recorded Phase 0A requirement.
- **Evidence-based:** label every statement by its supporting evidence and classification.
- **Technology-neutral:** describe business need and observable behavior, never a technical solution.
- **Traceable:** retain a link to the BRD requirement and related flow/dependencies.
- **Cross-module aware:** check shared masters, flows, workflow, audit, notifications, and global capabilities.
- **Testable where information permits:** make criteria observable; otherwise retain a visible TBD.
- **Uncertainty explicit:** missing detail is recorded, not inferred.

## 4. Source-of-Truth Hierarchy

| Priority | Authority | Use |
| --- | --- | --- |
| 1 | Current approved BRD (v2.0) | Primary source for baseline business requirements. |
| 2 | Approved requirement clarification / decision | May resolve the exact recorded gap it addresses. |
| 3 | Approved project decision | May constrain a requirement where it is explicitly applicable. |
| 4 | Clearly derived requirement | Only a logically necessary consequence of explicit source material; label BRD-DERIVED. |
| 5 | Proposed recommendation | Optional idea, labelled PROPOSED; never baseline fact. |
| 6 | Unresolved information | Retain as TBD/open question. |

Model knowledge, general ERP conventions, older/superseded BRDs, and unapproved stakeholder statements are not authoritative KIYA 360 requirements.

## 5. Requirement Classification Rules

| Classification | Definition and permitted use | Must not be used for | Example |
| --- | --- | --- | --- |
| BRD-REQUIRED | Explicitly stated in the current BRD. | Inferences or conventions. | `FR-CRM-001 Leads`. |
| BRD-DERIVED | A logically necessary consequence of an explicit BRD requirement, with source recorded. | New business capabilities, rules, or choices. | Inventory participation in Asset-to-Service because the BRD flow explicitly names spare parts. |
| PROPOSED | A recommendation not confirmed by the BRD. | A requirement presented as approved. | A future recommendation labelled “Not a confirmed BRD requirement.” |
| TBD | Detail the BRD/approved decisions do not provide. | An implied out-of-scope decision. | Availability-check shortage behavior. |
| OUT-OF-SCOPE | Explicitly excluded by the BRD for relevant scope. | Anything merely not described. | Marketplace storefront integrations beyond native E-Commerce. |

## 6. Detailed Requirement Template

Every detailed requirement uses the canonical template in `11-detailed-requirement-template.md`. Its fields cover ID, module/sub-module, title, BRD source, classification, objective, actors, trigger, preconditions, inputs, behavior, rules, outputs, validation, lifecycle, approvals, notifications, exceptions, dependencies, master/transaction concepts, audit/security/mobile/AI considerations, acceptance criteria, open questions, related requirements, and traceability. A field is not permission to invent its value: use TBD where evidence is absent.

## 7. Requirement Expansion Rules

1. Locate the original BRD statement and Phase 0A record.
2. State the exact scope and explicit behavior using BRD terminology.
3. Identify actors, triggers, inputs, outputs, rules, and lifecycle only when supported; record a necessary inference as BRD-DERIVED with rationale.
4. Identify applicable cross-module dependencies and shared conceptual data using existing BRD evidence.
5. Record every missing material detail as a linked TBD/open question.
6. Draft acceptance criteria only to the extent behavior is supported and observable.
7. Preserve links to the source requirement, business flow, related requirements, and open questions.
8. Send any new interpretation, conflict, or proposed capability through clarification/change control before treating it as baseline.

## 8. Anti-Hallucination Rules

Do not invent business rules, fields, workflows, approval limits, statuses, calculations, tax/payroll rules, permissions, notification triggers, integrations, APIs, screens, reports, AI models/algorithms, infrastructure, or technology choices. General ERP conventions may be explanatory context or explicitly labelled PROPOSED only; they must never silently become a KIYA 360 requirement. If evidence is insufficient, the correct result is TBD.

## 9. TBD Governance

Each TBD must state what is unknown, why it matters, the affected module/requirement, downstream impact, and the clarification needed. It remains visible in the detailed requirement and links to an open question where consequential. An assumption cannot resolve a TBD unless explicitly approved and recorded with source.

## 10. Open Question Governance

The existing OQ-001–OQ-015 remain unanswered. During Phase 0B, each question will be maintained with: Question ID; question; related requirement/module; BRD evidence; reason clarification is required; impact; status; decision; decision source; and date. Valid statuses are Open, Under Review, Answered Pending Approval, Approved, Deferred, or Superseded. Only an approved decision may change a baseline requirement.

Clarification decision governance is defined in `16-clarification-decision-register.md`. Its decision status is distinct from a requirement status: an approved clarification decision is valid evidence and may authorize a traceable requirement update, but does not automatically approve that requirement. Detailed-requirement records must cite applicable approved `CD-###` records and retain all unresolved portions as TBD.

## 11. Cross-Module Consistency Rules

Detailed requirements must identify relevant upstream/downstream requirements and be checked against these BRD flows:

- **Customer-to-Cash:** Lead → Opportunity → Enquiry → Quotation → Sales Order → Availability Check → Inventory → MRP / Planning → Production → Quality Check → Warehouse → Dispatch → Invoice → Tax → Payment → Accounting → Profitability → Customer History.
- **Procure-to-Pay:** Supplier → RFQ / RFP → Supplier Quotation → Purchase Order → Goods Receipt → Quality Check → Inventory → Supplier Invoice → Tax → Payment → Accounting → Supplier Performance.
- **Asset-to-Service:** Asset / Machine → Installation → Warranty → Service Request → Technician Assignment → Spare Parts → Work Order → Maintenance → Service Invoice → Payment → Asset History.

Cross-flow enablers remain Workflow & Approvals, Document Management, AI & Automation, Integration & API, Mobile Application, and Audit & Security. A detailed requirement must not independently introduce behavior that conflicts with a related module; conflicts are recorded for clarification.

## 12. Unified Data Model Consistency

Use BRD conceptual terms consistently, including Customer, Supplier, Item/Product, Warehouse, Employee, Asset, Company, Branch, User, Tax, Currency, and UOM. Do not duplicate a conceptual master by module unless the BRD requires it. This is not permission to design tables, attributes, keys, schemas, or relationships.

## 13. Requirement Prioritization Strategy

This is an analysis order, not an implementation sequence.

| Priority | Focus |
| --- | --- |
| P0 | Shared foundation: master data, workflow/approvals, audit/security, notifications, and cross-module behavior. |
| P1 | Core flows: Customer-to-Cash, Procure-to-Pay, Asset-to-Service. |
| P2 | Supporting operations: Marketing, Supplier Management, Logistics, Projects, HR, E-Commerce, Document Management. |
| P3 | Analytical/advanced capabilities: BI, EPM, AI & Automation, predictive capabilities. |

## 14. Requirement Dependency Strategy

Each detailed requirement identifies relevant upstream and downstream dependencies, shared masters/transactions, shared workflow/audit/notifications, and cross-module effects. It records business dependency only; it does not design technical mechanisms.

## 15. Acceptance Criteria Strategy

Acceptance criteria must be observable, tied to the requirement, source-supported, and testable where possible. Where the BRD does not define expected behavior, record the criterion as TBD rather than inventing a result. Criteria are not API, UI, database, or test designs.

## 16. Change-Control Strategy

Do not overwrite baseline requirements silently. Every post-baseline change record must contain the original requirement, proposed change, reason, source, affected modules/flows/dependencies, decision, approval status, and date. Approved changes update traceability while retaining the original reference.

## 17. Requirements Traceability Strategy

Maintain the chain: **BRD → Phase 0A requirement → Detailed requirement → Business flow → Entity/transaction → Future API → Future UI → Future test → Future implementation**. Future API/UI/test/implementation remain TBD until their authorized phases; no placeholder is an implementation decision.

## 18. Handling Conflicts

When requirements conflict, modules imply inconsistent behavior, BRD wording is ambiguous, a proposed design conflicts with the BRD, or an older BRD conflicts with v2.0, do not choose an interpretation silently. Record the conflict, cite sources, assess affected scope, and raise a clarification/TBD. The current approved BRD supersedes older sources unless an approved decision states otherwise.

## 19. Technology-Neutrality Rules

Requirements specification must not select programming languages, frameworks, databases, cloud providers, infrastructure, microservices/monoliths, messaging systems, AI providers, or ML frameworks unless an authoritative source explicitly requires one. None is selected by this strategy.

## 20. Phase 0B Execution Model

Work in incremental, reviewable groups: (1) P0 shared foundation and resolution planning for critical open questions; (2) Customer-to-Cash; (3) Procure-to-Pay; (4) Asset-to-Service; (5) supporting operational modules; and (6) analytics/advanced capabilities. Each group produces only detailed requirements supported by approved sources, a dependency check, a TBD/open-question update, and a stakeholder review checkpoint.

## 21. Phase 0B Exit Criteria

Detailed requirements are sufficiently complete for baseline/sign-off when in-scope scope is traceable; material TBDs are visible and dispositioned; cross-module checks are complete; critical open questions are resolved or accepted as deferred; acceptance criteria are present where evidence allows; and there are no known unsupported requirements or unresolved critical contradictions. Business-provided detail limits completeness; do not claim every requirement is fully specified when it is not.

## 22. Risks

- Modules 02–28 need detailed design expansion beyond the BRD's sub-module lists.
- Unresolved tax, payroll, workflow, data, integration, mobile, AI, and NFR questions may block detailed acceptance criteria.
- Cross-module inconsistencies may appear when individual capabilities are expanded.
- Unapproved convention-based detail could create a false baseline.

## 23. Recommended Next Sub-Phase

**Phase 0B-1 — Shared Foundation and Critical Clarification Planning.** It should define detailed requirements only for cross-module foundation items supported by the BRD and prepare the business-decision plan for critical open questions. It is not started by this document.
