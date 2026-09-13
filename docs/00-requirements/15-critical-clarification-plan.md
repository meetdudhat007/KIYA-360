# KIYA 360 — Critical Clarification Plan

## 1. Purpose

This plan organizes the existing 15 BRD-derived open questions so affected requirements can be clarified before approval without inventing business behavior. It does not answer any question, expand a detailed requirement, or authorize implementation.

## 2. Scope

Scope is exactly OQ-001 through OQ-015 in `06-open-questions.md`. No new official open questions are created. Any phrasing below describes a sub-clarification needed to understand an existing question, not a new requirement or business rule.

## 3. Source of Truth

The current source is `source/KIYA360_BRD.pdf`, KIYA 360 BRD v2.0, prepared 13 September 2026. This plan cross-references the approved Phase 0A baseline, the Phase 0B strategy, `SF-001`–`SF-015`, and `DEP-001`–`DEP-011`.

## 4. Clarification Governance Rules

- Preserve classifications: BRD-REQUIRED, BRD-DERIVED, PROPOSED, TBD, and OUT-OF-SCOPE.
- A BRD-REQUIRED capability may still have TBD behavior. A clarification request does not resolve it.
- Record stakeholder answers as a proposed decision first; only approved, sourced decisions may change a baseline requirement.
- Do not use general ERP practice, assumptions, or technical constraints to answer an open question.
- Stakeholder labels identify types from the BRD stakeholder list; no person, team owner, or authority is assigned here.

## 5. Priority Definitions

| Priority | Criteria |
| --- | --- |
| CRITICAL | Ambiguity materially affects a shared foundation, multiple modules/flows, core data concepts, financial/tax/security behavior, requirements approval, or significant downstream specification. |
| HIGH | Ambiguity materially affects an important module or substantial downstream work but does not block the entire requirements program. |
| MEDIUM | Important detail; independent analysis can continue safely while it remains TBD. |
| LOW | Limited immediate impact and can safely be clarified later. |

## 6. Blocking Definitions

| Status | Meaning |
| --- | --- |
| BLOCKING | Affected requirements must not be approved or specifically expanded until clarified. |
| PARTIALLY BLOCKING | Unaffected analysis may continue, but named dependent requirements must remain TBD and cannot be approved. |
| NON-BLOCKING | Analysis can proceed safely while the item remains TBD. |

## 7. Open Question Summary

| Priority | Count | Question IDs |
| --- | ---: | --- |
| CRITICAL | 9 | OQ-001, OQ-002, OQ-003, OQ-005, OQ-007, OQ-008, OQ-011, OQ-012, OQ-015 |
| HIGH | 6 | OQ-004, OQ-006, OQ-009, OQ-010, OQ-013, OQ-014 |
| MEDIUM | 0 | None |
| LOW | 0 | None |
| BLOCKING | 6 | OQ-001, OQ-002, OQ-005, OQ-007, OQ-008, OQ-011 |
| PARTIALLY BLOCKING | 9 | OQ-003, OQ-004, OQ-006, OQ-009, OQ-010, OQ-012, OQ-013, OQ-014, OQ-015 |
| NON-BLOCKING | 0 | None |

## 8. Detailed Analysis of All 15 Questions

### OQ-001 — Detailed requirements for modules 02–28

- **BRD evidence / known:** BRD §7.2–§7.28 lists sub-module capabilities and explicitly says they require expansion during detailed design.
- **Unknown / must remain TBD:** behavior, business rules, field detail, lifecycle, validations, exceptions, and acceptance criteria for modules 02–28.
- **Impact:** all modules except Platform & Administration; all SF records; all flows; requirement references BRD §7.2–§7.28; concepts vary by module.
- **Dependencies:** clarification dependency for all `DEP-001`–`DEP-011`; **CRITICAL / BLOCKING** because detailed requirements cannot be approved without bounded scope.
- **Stakeholder clarification / expected output:** Business leadership and relevant BRD stakeholder types must confirm module-by-module detailed scope; output is an approved detailed-scope clarification per affected capability.
- **Can proceed / do not assume:** Governance, source traceability, and planning can proceed; do not assume standard ERP behavior, fields, or workflows. Related: all OQs, especially OQ-002.

### OQ-002 — Fields, validations, and status values

- **BRD evidence / known:** BRD requires a single data model and names platform masters and transaction capabilities; it does not define record fields, validation rules, or status values.
- **Unknown / must remain TBD:** data content, validation, lifecycle/status values, master ownership, and transaction detail.
- **Impact:** all modules, SF-003/SF-004/SF-013/SF-014; all flows; conceptual masters and transactions recorded in `01-master-requirements.md`.
- **Dependencies:** affects all shared foundations and `DEP-001`–`DEP-011`; **CRITICAL / BLOCKING** because detailed record/process requirements cannot be approved without the business definition.
- **Stakeholder clarification / expected output:** Platform Administrator and relevant business module stakeholder types; output is approved conceptual data/validation/lifecycle decisions, without database design.
- **Can proceed / do not assume:** dependency analysis can continue; do not assume common fields, statuses, numbering formats, or validations. Related: OQ-001, OQ-003, OQ-007–OQ-011.

### OQ-003 — Approval conditions, matrices, escalation, delegation

- **BRD evidence / known:** Workflow Builder, Approval Matrix, Escalation Rules, Delegation, and shared KIYA Engine are BRD-required; approval levels/delegation are also listed in Platform & Administration.
- **Unknown / must remain TBD:** applicable processes, conditions, limits, approvers, matrix rules, timing, delegation, and exceptions.
- **Impact:** all modules/flows using SF-005; related SF-002/SF-006/SF-008; related IDs FR-WFA-001–007 and FR-PADM-1.2.4.
- **Dependencies:** `DEP-010` and `DEP-011`; **CRITICAL / PARTIALLY BLOCKING** because approval-dependent requirements cannot be approved, while unrelated capability analysis may continue.
- **Stakeholder clarification / expected output:** Platform Administrator and relevant business stakeholder types; output is approved business approval/escalation/delegation policy per applicable process.
- **Can proceed / do not assume:** non-approval portions can proceed; do not assume thresholds, authorities, workflow states, or escalation timing. Related: OQ-002, OQ-004, OQ-015.

### OQ-004 — Notification triggers and templates

- **BRD evidence / known:** BRD lists Email, WhatsApp, SMS, Push, and In-App notifications, templates, reminders, and workflow/mobile notifications.
- **Unknown / must remain TBD:** event triggers, recipients, template content, channel selection, timing, failure/exception behavior, and reminders/calendar behavior.
- **Impact:** SF-006; related SF-005/SF-009; all flows as enablers; IDs FR-PADM-1.7.1–1.7.6, FR-WFA-005, FR-MOB-006.
- **Dependencies:** shared workflow `DEP-010`; **HIGH / PARTIALLY BLOCKING** because dependent process specifications must remain TBD.
- **Stakeholder clarification / expected output:** Platform Administrator and affected business module stakeholder types; output is approved notification-event and communication requirement definition.
- **Can proceed / do not assume:** channel inventory and traceability can proceed; do not assume who receives what or when. Related: OQ-003, OQ-013.

### OQ-005 — Tax-country coverage and statutory filing behavior

- **BRD evidence / known:** BRD requires Global Tax Engine/country rules/GST-VAT/withholding/e-invoicing/statutory reports; Phase 1 assumption states India is primary with one additional reference country.
- **Unknown / must remain TBD:** reference country, country rule coverage, statutory filing behavior, and detailed tax treatment.
- **Impact:** Tax & Statutory Compliance, Finance & Accounting, Sales, Procurement; SF-003/SF-015; Customer-to-Cash and Procure-to-Pay; FR-TAX-001–007.
- **Dependencies:** `DEP-005`; **CRITICAL / BLOCKING** for tax/invoice requirements because it determines applicable business scope and behavior.
- **Stakeholder clarification / expected output:** Finance, Tax & EPM stakeholder type; output is approved jurisdiction scope and tax/statutory behavior boundary.
- **Can proceed / do not assume:** generic BRD taxonomy analysis can proceed; do not assume rates, calculations, filings, or additional countries. Related: OQ-006, OQ-015.

### OQ-006 — Payroll/statutory calculations

- **BRD evidence / known:** HR & Payroll includes Payroll Processing; BRD out-of-scope limits country-specific payroll/statutory calculations beyond India and one additional reference country.
- **Unknown / must remain TBD:** payroll/statutory calculations for the included jurisdictions and their applicability.
- **Impact:** HR & Payroll, Tax & Statutory Compliance; SF-001/SF-003; related FR-HR-004; no direct named core-flow mapping.
- **Dependencies:** tax scope in OQ-005; **HIGH / PARTIALLY BLOCKING** for payroll-specific detailed requirements.
- **Stakeholder clarification / expected output:** HR and Finance, Tax & EPM stakeholder types; output is approved payroll/statutory business-scope clarification for included jurisdictions.
- **Can proceed / do not assume:** non-payroll HR capability analysis can proceed; do not assume statutory formulas, benefits, deductions, or localization. Related: OQ-005, OQ-002.

### OQ-007 — Inventory reservation, valuation, shortages, availability outcomes

- **BRD evidence / known:** Sales orders check real-time stock and reserve inventory; dispatch reduces stock. Inventory includes stock quantity and stock valuation.
- **Unknown / must remain TBD:** reservation timing/rules, valuation application, shortage handling, and availability-check outcomes.
- **Impact:** Sales, Inventory, Warehouse; SF-003/SF-004; Customer-to-Cash; transaction concepts Sales Order, availability check, item, stock/warehouse; FR-SALES-003–005 and FR-INV-002–006.
- **Dependencies:** `DEP-002`, `DEP-003`, `DEP-004`; **CRITICAL / BLOCKING** because core sales-to-fulfilment behavior cannot be coherently approved without it.
- **Stakeholder clarification / expected output:** Sales, Inventory & Warehouse stakeholder types; output is approved availability/reservation/shortage/valuation business behavior.
- **Can proceed / do not assume:** scope/flow mapping can proceed; do not assume allocation, backorder, stock valuation method, or exception process. Related: OQ-002, OQ-008, OQ-009.

### OQ-008 — Demand, capacity, work-order release, exceptions

- **BRD evidence / known:** BRD names Demand/Material/Capacity/Production/Supply/Schedule Planning and states unmet demand feeds planning, producing production/work orders.
- **Unknown / must remain TBD:** planning decisions, capacity rules, release behavior, schedules, and exceptions.
- **Impact:** MRP & Planning, Manufacturing, Inventory, Sales; SF-003/SF-004; Customer-to-Cash; FR-MRP-001–006 and FR-MFG-003–005.
- **Dependencies:** `DEP-003`, `DEP-004`; **CRITICAL / BLOCKING** for planning/production requirement approval.
- **Stakeholder clarification / expected output:** Manufacturing, MRP & Quality stakeholder types; output is approved planning/work-order decision and exception behavior.
- **Can proceed / do not assume:** other module analysis can continue; do not assume planning algorithms, capacity calculations, release states, or production rules. Related: OQ-007, OQ-009.

### OQ-009 — Quality criteria and NCR/CAPA lifecycle

- **BRD evidence / known:** BRD names incoming, in-process, final inspection and NCR/CAPA, and requires inspection before warehouse put-away.
- **Unknown / must remain TBD:** inspection criteria, acceptance/rejection behavior, NCR/CAPA lifecycle, and quality-control rules.
- **Impact:** Quality, Procurement, Manufacturing, Inventory, Warehouse; SF-004; Customer-to-Cash and Procure-to-Pay; FR-QLTY-001–006.
- **Dependencies:** `DEP-004`; **HIGH / PARTIALLY BLOCKING** because quality-gate dependent specifications cannot be approved.
- **Stakeholder clarification / expected output:** Manufacturing, MRP & Quality stakeholder type; output is approved inspection and non-conformance business behavior.
- **Can proceed / do not assume:** named inspection capability analysis can proceed; do not assume criteria, disposition, NCR/CAPA states, or acceptance rules. Related: OQ-007, OQ-008.

### OQ-010 — Supplier evaluation and performance-scorecard measures

- **BRD evidence / known:** Supplier Evaluation/Performance Scorecard are BRD capabilities; RFQ/RFP and PO activity feeds the scorecard.
- **Unknown / must remain TBD:** performance measures, calculation rules, ratings, and evaluation behavior.
- **Impact:** Supplier Management, Procurement; SF-003/SF-011; Procure-to-Pay; Supplier, RFQ/RFP, PO; FR-SUPM-003/005.
- **Dependencies:** `DEP-006`; **HIGH / PARTIALLY BLOCKING** because supplier-performance specifications cannot be approved.
- **Stakeholder clarification / expected output:** Procurement & Supplier Management stakeholder type; output is approved evaluation/scorecard business measures and behavior.
- **Can proceed / do not assume:** sourcing scope and dependency mapping can proceed; do not assume score formulas, weights, ratings, or thresholds. Related: OQ-002, OQ-005.

### OQ-011 — Asset installation, warranty, dispatch, spare parts, service billing

- **BRD evidence / known:** Asset-to-Service names installation through asset history; BRD explicitly links installed assets under warranty to service requests, work orders, spare-parts consumption, and history.
- **Unknown / must remain TBD:** installation/warranty rules, technician dispatch, spare-parts treatment, service billing/payment behavior, and exceptions.
- **Impact:** Asset Management, Maintenance & Field Service, Inventory, Finance & Accounting; SF-003/SF-004; Asset-to-Service; Asset, Service Request, Work Order, Payment; FR-AST-001–006 and FR-MFS-001–007.
- **Dependencies:** `DEP-007`; **CRITICAL / BLOCKING** for Asset-to-Service detailed requirements.
- **Stakeholder clarification / expected output:** Asset & Maintenance / Field Service stakeholder type; output is approved asset-to-service operational and billing behavior.
- **Can proceed / do not assume:** lifecycle scope and links can proceed; do not assume warranty terms, dispatch workflow, parts valuation, service pricing, or payment rules. Related: OQ-002, OQ-007.

### OQ-012 — Integration counterparties and behavior

- **BRD evidence / known:** BRD requires API management, system integration, data sync, webhooks, third-party apps, middleware, and integration monitoring.
- **Unknown / must remain TBD:** counterparties, interfaces, mappings, events, sync behavior, error/exception handling, and operations.
- **Impact:** Integration & API, all modules/flows as enabler; SF-012/SF-008/SF-009; FR-INTG-001–007.
- **Dependencies:** shared integration foundation; **CRITICAL / PARTIALLY BLOCKING** because integration-specific requirements cannot be approved while unrelated module business analysis can continue.
- **Stakeholder clarification / expected output:** IT / Integration & Security stakeholder type; output is approved integration scope/boundaries and business interaction requirements.
- **Can proceed / do not assume:** integration capability inventory can proceed; do not assume systems, APIs, webhooks, data formats, or error handling. Related: OQ-013, OQ-015.

### OQ-013 — Mobile offline data and synchronization

- **BRD evidence / known:** BRD requires native Sales, Service, Dashboard, Inventory, and Approvals apps with offline sync and real-time web-mobile sync.
- **Unknown / must remain TBD:** offline data, supported tasks, synchronization timing, conflict behavior, and exceptions.
- **Impact:** Mobile Application, Sales, Service, BI, Inventory, Workflow & Approvals; SF-009/SF-005/SF-006; all flows as mobile enabler; FR-MOB-001–007.
- **Dependencies:** mobile/shared workflow foundations; **HIGH / PARTIALLY BLOCKING** for mobile-specific detailed requirements.
- **Stakeholder clarification / expected output:** IT / Integration & Security and affected business stakeholder types; output is approved mobile/offline business-behavior boundary.
- **Can proceed / do not assume:** app capability mapping can proceed; do not assume offline operations, sync conflict rules, or supported mobile workflow. Related: OQ-004, OQ-012.

### OQ-014 — AI and automation boundaries/governance

- **BRD evidence / known:** BRD requires six AI/automation capabilities across stated areas and identifies predictive analytics/anomaly/assistant purposes.
- **Unknown / must remain TBD:** data access, human review, outcome criteria, governance, and usage boundaries.
- **Impact:** AI & Automation, BI, Sales, Inventory, Finance, Maintenance, Service; SF-010/SF-011/SF-008; all flows as enabler; FR-AIAU-001–007 and FR-BI-006.
- **Dependencies:** shared AI/analytics foundation; **HIGH / PARTIALLY BLOCKING** for AI-specific requirements.
- **Stakeholder clarification / expected output:** Business leadership, affected business stakeholder types, and IT / Integration & Security; specific stakeholder owner TBD. Output is approved AI use/governance boundary.
- **Can proceed / do not assume:** BRD-level capability traceability can proceed; do not assume models, providers, prompts, automation decisions, training, or human-review rules. Related: OQ-012, OQ-015.

### OQ-015 — Measurable NFR targets

- **BRD evidence / known:** BRD requires real-time insights, security/scalability, multi-entity operation, mobile-first, and 24/7 operations, but presents qualitative expectations rather than measurable targets.
- **Unknown / must remain TBD:** measurable availability, performance, scalability, security-monitoring, support, and real-time latency targets.
- **Impact:** all modules/flows; SF-015/SF-002/SF-011; FR-ASC-001–005 and BRD §10.
- **Dependencies:** all-module BI/EPM, workflow, audit/security, integration/mobile foundations; **CRITICAL / PARTIALLY BLOCKING** because measurable NFR acceptance cannot be approved, while functional analysis can continue.
- **Stakeholder clarification / expected output:** Business leadership and IT / Integration & Security stakeholder types; output is approved measurable NFR target set and scope.
- **Can proceed / do not assume:** qualitative NFR traceability can proceed; do not assume service levels, latency, retention, scale, support model, or security thresholds. Related: OQ-003, OQ-005, OQ-012–OQ-014.

## 9. Shared Foundation Impact

All existing questions map to existing foundations; no new foundation capability is proposed. The most cross-cutting impacts are SF-003/SF-004 (OQ-001, OQ-002, OQ-007–OQ-011), SF-005/SF-006 (OQ-003–OQ-004), SF-012/SF-009/SF-010 (OQ-012–OQ-014), and SF-015 (OQ-005, OQ-015).

## 10. Dependency Impact

`DEP-001`–`DEP-011` remain the dependency baseline. OQ-007/008/009 directly constrain Customer-to-Cash dependencies; OQ-005/010 constrain Procure-to-Pay; OQ-011 constrains Asset-to-Service; OQ-003/004/012/013/014/015 affect shared enablement. This plan adds no new module dependency.

## 11. End-to-End Flow Impact

| Flow / enabler | Questions requiring coordinated clarification |
| --- | --- |
| Customer-to-Cash | OQ-001, OQ-002, OQ-003, OQ-004, OQ-005, OQ-007, OQ-008, OQ-009, OQ-012–OQ-015 |
| Procure-to-Pay | OQ-001, OQ-002, OQ-003, OQ-004, OQ-005, OQ-009, OQ-010, OQ-012–OQ-015 |
| Asset-to-Service | OQ-001, OQ-002, OQ-003, OQ-004, OQ-007, OQ-011–OQ-015 |
| Shared enablers | Workflow: OQ-003; notifications: OQ-004; integration: OQ-012; mobile: OQ-013; AI: OQ-014; audit/security/NFR: OQ-015. |

## 12. Master Data Impact

OQ-002 is the master-data baseline question. Customer (OQ-001/002/007), Supplier (OQ-001/002/010), Item and Warehouse (OQ-002/007/008/009/011), Employee/User/Role (OQ-002/003/006/013), Asset (OQ-002/011), Tax/Currency (OQ-001/002/005/006), and UOM (OQ-002) are conceptual impacts only. No fields, ownership model, tables, keys, or relationships are defined.

## 13. Clarification Groups

| Group ID | Group Name | Included Questions | Reason / expected decisions | Affected Modules and Foundations | Dependencies | Suggested Sequence |
| --- | --- | --- | --- | --- | --- | --- |
| CG-01 | Scope and shared-data baseline | OQ-001, OQ-002 | Bound detailed scope and conceptual master/transaction detail. | All modules; SF-001/SF-003/SF-004/SF-013/SF-014 | All DEP records | FIRST |
| CG-02 | Workflow and communication governance | OQ-003, OQ-004 | Define approval/escalation/delegation and notification requirements. | All modules; SF-002/SF-005/SF-006/SF-008/SF-009 | DEP-010, DEP-011 | NEXT |
| CG-03 | Finance, tax, and payroll scope | OQ-005, OQ-006 | Confirm jurisdiction boundaries and included business behavior. | Tax, Finance, HR; SF-001/SF-003/SF-015 | DEP-005 | NEXT |
| CG-04 | Supply, production, quality, supplier measures | OQ-007, OQ-008, OQ-009, OQ-010 | Clarify core operational rules across linked flows. | Sales, Inventory, Warehouse, MRP, Manufacturing, Quality, Procurement, Supplier Management; SF-003/SF-004/SF-011 | DEP-002–006 | THEN |
| CG-05 | Asset-to-Service behavior | OQ-011 | Clarify the complete service-flow business behavior. | Asset, Maintenance & Field Service, Inventory, Finance; SF-003/SF-004 | DEP-007 | THEN |
| CG-06 | Digital shared-enabler boundaries | OQ-012, OQ-013, OQ-014 | Confirm integration, mobile, and AI scope/governance boundaries. | Integration, Mobile, AI, BI; SF-008–012 | Shared enablers | THEN |
| CG-07 | Measurable platform expectations | OQ-015 | Establish NFR measures without choosing an implementation. | All modules; SF-002/SF-011/SF-015 | DEP-009–011 | LATER; begin evidence collection early |

## 14. Stakeholder Type Mapping

Stakeholder types are taken from the BRD stakeholder categories; the responsible owner for any decision remains TBD unless separately assigned.

| Stakeholder type | Questions |
| --- | --- |
| Business leadership / relevant business module stakeholders | OQ-001, OQ-014, OQ-015 |
| Platform Administrator / affected module stakeholders | OQ-002, OQ-003, OQ-004 |
| Finance, Tax & EPM | OQ-005, OQ-006, OQ-015 |
| HR | OQ-006 |
| Sales; Inventory & Warehouse | OQ-007 |
| Manufacturing, MRP & Quality | OQ-008, OQ-009 |
| Procurement & Supplier Management | OQ-010 |
| Asset & Maintenance / Field Service | OQ-011 |
| IT / Integration & Security with affected business stakeholders | OQ-012, OQ-013, OQ-014, OQ-015 |

## 15. Recommended Clarification Sequence

1. **FIRST:** CG-01 (OQ-001/002) to bound detailed scope and common conceptual data.
2. **NEXT:** CG-02 (OQ-003/004) and CG-03 (OQ-005/006), because approvals/communication and financial/tax scope constrain multiple specifications.
3. **THEN:** CG-04 (OQ-007–010), CG-05 (OQ-011), and CG-06 (OQ-012–014) in coordinated domain sessions.
4. **LATER:** CG-07 (OQ-015), while collecting evidence early; measurable acceptance must be resolved before NFR approval.

This is a sequencing recommendation, not a requirement that the business must follow it.

## 16. Safe Parallel Work

### Safe to Continue

- Maintain BRD/Phase 0A traceability, glossary, source integrity, dependency mapping, and clarification scheduling.
- Analyze requirements only at their existing BRD scope and identify linked requirements/foundations/TBDs.
- Prepare neutral detailed-requirement shells using `11-detailed-requirement-template.md`, without populating unsupported behavior or marking them approved.

### Must Wait for Clarification

- Approval of any affected detailed requirements under the blocking/partially-blocking questions.
- Business rules, fields, statuses, validations, workflow/notification behavior, tax/payroll treatment, inventory/planning/quality/service behavior, integration/mobile/AI boundaries, and measurable NFR acceptance.

## 17. Requirements That Must Remain TBD

All unknowns described in OQ-001–OQ-015 remain TBD until an approved, source-recorded clarification is received. No question is answered by this plan.

## 18. Risks

- Premature expansion could turn ERP convention into unsupported requirements.
- Delaying CG-01, tax, workflow, supply-chain, service, integration, or NFR clarification can create inconsistent downstream drafts.
- Combining unrelated questions would obscure decision ownership; groups therefore reflect documented shared impact only.

## 19. Exit Criteria

Phase 0B-1B is complete when exactly the 15 existing questions are analyzed, each has evidence-based priority/blocking/impact/clarification planning, related groups and stakeholder types are identified, safe parallel work is separated, traceability is retained, and no business question is answered. These criteria do not require stakeholder answers.

## 20. Traceability

Each record maintains: **Open Question → BRD evidence → Phase 0A requirement/module → SF record → DEP record/flow → clarification request → future approved decision → requirement status**. No requirement ID is created by this plan. Where a question cites a BRD section rather than a functional ID, that reference remains the authoritative identifier until a later approved detailed-requirement ID is assigned.

## 21. Clarification Register

| Question ID | Priority | Blocking | Affected modules / foundations / flows | Affected requirement IDs | Stakeholder type | Clarification needed / approval-required output | Dependencies | Can proceed without answer? | Related questions | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OQ-001 | CRITICAL | BLOCKING | Modules 02–28; all SF; all flows | BRD §7.2–§7.28 | Business leadership + relevant module stakeholders | Detailed-scope clarification (approval required) | All DEP | Only governance/planning | All | Open — clarification planned |
| OQ-002 | CRITICAL | BLOCKING | All modules; SF-003/004/013/014; all flows | Various | Platform Administrator + module stakeholders | Conceptual data/validation/lifecycle clarification (approval required) | All DEP | Only non-detail analysis | OQ-001, 003, 007–011 | Open — clarification planned |
| OQ-003 | CRITICAL | PARTIALLY BLOCKING | All modules; SF-002/005/006/008; all flows | FR-WFA-001–007; FR-PADM-1.2.4 | Platform Administrator + business stakeholders | Approval/escalation/delegation clarification (approval required) | DEP-010/011 | Yes, excluding approval-dependent detail | OQ-002, 004, 015 | Open — clarification planned |
| OQ-004 | HIGH | PARTIALLY BLOCKING | All modules; SF-005/006/009; all flows | FR-PADM-1.7.1–6; FR-WFA-005; FR-MOB-006 | Platform Administrator + affected stakeholders | Notification-event clarification (approval required) | DEP-010 | Yes, excluding notification-dependent detail | OQ-003, 013 | Open — clarification planned |
| OQ-005 | CRITICAL | BLOCKING | Tax, Finance, Sales, Procurement; SF-003/015; C2C/P2P | FR-TAX-001–007 | Finance, Tax & EPM | Jurisdiction/tax-boundary clarification (approval required) | DEP-005 | Only non-tax analysis | OQ-006, 015 | Open — clarification planned |
| OQ-006 | HIGH | PARTIALLY BLOCKING | HR, Tax; SF-001/003 | FR-HR-004 | HR + Finance, Tax & EPM | Payroll/statutory scope clarification (approval required) | OQ-005 | Yes, excluding payroll detail | OQ-005, 002 | Open — clarification planned |
| OQ-007 | CRITICAL | BLOCKING | Sales, Inventory, Warehouse; SF-003/004; C2C | FR-SALES-003–005; FR-INV-002–006 | Sales + Inventory & Warehouse | Availability/reservation/shortage/valuation clarification (approval required) | DEP-002–004 | Only mapping | OQ-002, 008, 009 | Open — clarification planned |
| OQ-008 | CRITICAL | BLOCKING | MRP, Manufacturing, Inventory, Sales; SF-003/004; C2C | FR-MRP-001–006; FR-MFG-003–005 | Manufacturing, MRP & Quality | Planning/work-order clarification (approval required) | DEP-003/004 | Only mapping | OQ-007, 009 | Open — clarification planned |
| OQ-009 | HIGH | PARTIALLY BLOCKING | Quality, Procurement, Manufacturing, Inventory, Warehouse; SF-004; C2C/P2P | FR-QLTY-001–006 | Manufacturing, MRP & Quality | Inspection/NCR-CAPA clarification (approval required) | DEP-004 | Yes, excluding quality-gate detail | OQ-007, 008 | Open — clarification planned |
| OQ-010 | HIGH | PARTIALLY BLOCKING | Procurement, Supplier Management; SF-003/011; P2P | FR-SUPM-003/005 | Procurement & Supplier Management | Evaluation/scorecard-measure clarification (approval required) | DEP-006 | Yes, excluding scorecard detail | OQ-002, 005 | Open — clarification planned |
| OQ-011 | CRITICAL | BLOCKING | Asset, MFS, Inventory, Finance; SF-003/004; A2S | FR-AST-001–006; FR-MFS-001–007 | Asset & Maintenance / Field Service | Asset-to-service clarification (approval required) | DEP-007 | Only mapping | OQ-002, 007 | Open — clarification planned |
| OQ-012 | CRITICAL | PARTIALLY BLOCKING | Integration; SF-008/009/012; all flows | FR-INTG-001–007 | IT / Integration & Security | Integration scope/boundary clarification (approval required) | Shared enabler | Yes, excluding integration detail | OQ-013–015 | Open — clarification planned |
| OQ-013 | HIGH | PARTIALLY BLOCKING | Mobile; SF-005/006/009; all flows | FR-MOB-001–007 | IT / Integration & Security + affected stakeholders | Mobile/offline-boundary clarification (approval required) | Shared enabler | Yes, excluding mobile detail | OQ-004, 012 | Open — clarification planned |
| OQ-014 | HIGH | PARTIALLY BLOCKING | AI, BI, named areas; SF-008/010/011; all flows | FR-AIAU-001–007; FR-BI-006 | Business leadership + affected stakeholders + IT / Integration & Security | AI governance/use-boundary clarification (approval required) | Shared enabler | Yes, excluding AI detail | OQ-012, 015 | Open — clarification planned |
| OQ-015 | CRITICAL | PARTIALLY BLOCKING | All modules; SF-002/011/015; all flows | BRD §10; FR-ASC-001–005 | Business leadership + IT / Integration & Security | Measurable NFR-target clarification (approval required) | DEP-009–011 | Yes, excluding NFR acceptance approval | OQ-003, 005, 012–014 | Open — clarification planned |

## 22. Clarification Session Template

This session template records evidence only. Use `17-clarification-decision-template.md` if captured input proceeds to a candidate decision; do not treat a session or stakeholder statement as approval.

| Field | Record |
| --- | --- |
| Session ID | `[TBD]` |
| Date | `[TBD]` |
| Participants / stakeholder types | `[TBD]` |
| Questions covered | `[OQ-…]` |
| Current BRD evidence | `[BRD section / requirement IDs]` |
| Clarification required | `[Restate unknown; do not pre-answer]` |
| Discussion | `[Record stakeholder discussion]` |
| Captured answer(s) / stakeholder input | `[TBD; not an approved decision]` |
| Related clarification decision | `[CD-### / NOT YET CREATED]` |
| Proposed approver type | `[TBD]` |
| Affected requirements / modules / foundations / flows | `[Traceable references]` |
| New / updated TBDs | `[TBD]` |
| Follow-up actions | `[TBD]` |
| Approval status | `[Not approved unless linked CD record is explicitly APPROVED]` |
| Evidence / source | `[Session evidence; approval evidence belongs in the CD record]` |
| Traceability | `[OQ → BRD → requirement → SF/DEP → CD → requirement update]` |
