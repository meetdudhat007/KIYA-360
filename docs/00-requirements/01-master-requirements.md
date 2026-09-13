# KIYA 360 — Master Requirements

## 1. Document Information

| Field | Value |
| --- | --- |
| Project | KIYA 360 |
| Document | Master Requirements |
| Phase | Phase 0 |
| Sub-phase | 0A — Requirements Analysis, Scope & Module Inventory |
| Source document | `source/KIYA360_BRD.pdf` — KIYA 360 Business Requirements Document |
| BRD version | 2.0 |
| BRD date | 13 September 2026 (prepared); 13/09/2026 (document control) |
| Analysis status | Complete from the available BRD |

## 2. Purpose

This document establishes the structured requirements baseline derived from the KIYA 360 BRD. It is an analysis layer; it does not alter the source BRD or prescribe technical implementation.

## 3. Scope of Phase 0A

Phase 0A covers scope analysis, module inventory, functional-requirement identification and classification, business-flow mapping, cross-module dependency identification, traceability preparation, ambiguity and terminology identification, and assumption/constraint identification. It excludes solution design, data design, APIs, UI design, technology selection, and implementation.

## 4. Requirement Classification

| Classification | Use in this baseline |
| --- | --- |
| BRD-REQUIRED | Explicitly stated in the BRD. |
| BRD-DERIVED | Logically necessary to implement an explicit BRD requirement; not a new business capability. |
| PROPOSED | Recommendation only; not a confirmed BRD requirement. |
| TBD | The BRD does not specify this detail. |
| OUT-OF-SCOPE | Explicitly excluded from the relevant scope by the BRD. |

## 5. Source-of-Truth Rules

The BRD version 2.0 is authoritative. Requirements use its terminology and preserve its supplied IDs. No common ERP practice, role, rule, approval limit, tax treatment, integration, report, workflow, UI, API, schema, or AI design is treated as a KIYA 360 requirement unless the BRD states it. Necessary but unstated implementation-independent detail is marked BRD-DERIVED; unknown detail is marked TBD and, where consequential, recorded as an open question. The BRD remains unchanged.

## 6. Phase 0A Completion Criteria

Phase 0A is complete when the available BRD has been read; all identified modules and functional requirements are catalogued; scope, flows, stated dependencies, AI and non-functional requirements are documented; traceability is prepared without implementation invention; and material gaps, terminology, assumptions, constraints, and exclusions are visible.

## 7. Business Objectives Extracted from the BRD

- Provide one unified data platform across CRM, ERP, HRMS, WMS, and BI capabilities.
- Provide real-time end-to-end visibility of Customer-to-Cash, Procure-to-Pay, and Asset-to-Service.
- Standardise company, user, security, master-data, numbering, and notification configuration through Platform & Administration.
- Provide global tax/statutory compliance, embedded AI/automation, native mobile with offline sync, and native multi-company/country/currency/language operation.

## 8. Unified Data-Model Analysis (Conceptual Only)

The BRD requires a single data model spanning all 28 modules, with no duplicate master data between CRM, ERP, and back-office systems. This is a conceptual inventory, not a database design.

| Category | BRD-mentioned conceptual entities / transactions |
| --- | --- |
| Master / reference | Company, Branch, Business Unit, Department, Division, Location, User, Role, Customer, Supplier, Item, Employee, Tax, Currency, UOM, Warehouse, Asset |
| Business transactions | Lead, Opportunity, Enquiry, Quotation, Sales Order, Purchase Requisition, RFQ/RFP, Supplier Quotation, Purchase Order, Goods Receipt, Work Order, Inspection, Dispatch, Invoice, Payment, Service Request, Maintenance Work Order |

## 9. AI & Automation Analysis

| AI Capability | Description from BRD | Modules / areas | Classification | Details TBD |
| --- | --- | --- | --- | --- |
| AI Insights | Surfaces trends and recommended actions. | Sales, Inventory, Finance, Service | BRD-REQUIRED | Recommendation logic and governance. |
| Predictive Analytics | Forecasts demand, cash flow, and maintenance needs. | Demand, finance, maintenance | BRD-REQUIRED | Forecast horizon, inputs, accuracy criteria. |
| Process Automation / RPA Bots | Automates repetitive multi-step tasks such as invoice matching and data entry without custom code. | Cross-suite | BRD-REQUIRED | Supported processes, controls, exceptions. |
| AI Chat Assistant | In-app guidance and quick data lookups. | Cross-suite | BRD-REQUIRED | Data access boundaries and supported questions. |
| Anomaly Detection | Flags unusual transactions, stock movements, or spending patterns for review. | Finance, inventory, spending | BRD-REQUIRED | Detection criteria and review routing. |
| Machine Learning Models | Underpins scoring, forecasting, and classification features. | Cross-suite | BRD-REQUIRED | Model selection, training, monitoring. |

No model, provider, algorithm, prompt, RAG approach, or implementation architecture is selected in Phase 0A.

## 10. Non-Functional Requirements

| Category | BRD requirement | Implementation approach |
| --- | --- | --- |
| Unified Platform | Single data model across 28 modules; no duplicate master data. | TBD — later architecture phase. |
| Real-time Insights | Dashboards/reports reflect posted transactions across companies and branches. | TBD — later architecture phase. |
| Smart Automation | Workflow builder, approval matrix, and RPA reduce repetitive processing. | TBD — later architecture phase. |
| Global Tax Engine | Support GST/VAT/Sales Tax, withholding tax, e-invoicing/e-way bill, and statutory reports across countries. | TBD — later architecture phase. |
| AI Powered | AI insights, predictive analytics, and chat assistant embedded across modules. | TBD — later architecture phase. |
| Mobile First | Native Sales, Service, Dashboard, Inventory, and Approvals apps with offline sync. | TBD — later architecture phase. |
| Secure & Scalable | RBAC, encryption at rest/in transit, device/session controls, and growth scalability. | TBD — later architecture phase. |
| Multi-Company / Multi-Country | Manage legal entities, countries, currencies, and languages from one instance. | TBD — later architecture phase. |
| 24/7 Operations | Always-on availability with continuous support. | TBD — later architecture phase. |

## Phase 0A Validation Summary

| Check | Result |
| --- | --- |
| BRD successfully read | Yes |
| BRD version / date | 2.0 / 13 September 2026 |
| Modules identified | 28 |
| Functional requirements identified | 238 |
| Explicit out-of-scope items identified | 4 |
| Business flows identified | 3 |
| Cross-module dependencies identified | 11 |
| AI requirements identified | 6 |
| Non-functional requirement categories identified | 9 |
| Assumptions / constraints identified | 4 |
| Open questions identified | 15 |
| Requirement IDs preserved | Yes |
| Hallucinated requirements introduced | No |
| Application code created | No |
| Technology decisions made | No |
| Phase 0A status | COMPLETE |

Phase 0A documentation has been generated from the available BRD. Any details not specified by the BRD are explicitly marked TBD or recorded as open questions.
