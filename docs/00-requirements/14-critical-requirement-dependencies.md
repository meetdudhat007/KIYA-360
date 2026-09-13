# KIYA 360 — Critical Requirement Dependencies

## 1. Purpose

Dependency mapping prevents detailed requirements from being written in isolation where a definition in one module changes a core flow, shared foundation, or another module's behavior.

## 2. Dependency Definitions

| Type | Meaning |
| --- | --- |
| Upstream | A requirement whose definition affects another requirement. |
| Downstream | A requirement whose behavior depends on another requirement. |
| Shared | A capability used by several modules. |
| Flow | A requirement participating in an explicit BRD end-to-end flow. |
| Clarification | A requirement that cannot safely be finalized until an open question is resolved. |

## 3. Explicit BRD Dependency Records

The BRD states these cross-module relationships at relationship level; it does not map each relationship to every individual functional-requirement ID. IDs below identify the related Phase 0A capabilities, not an unsupported feature-to-feature specification. Exact behavior remains TBD until detailed requirements and clarifications are approved.

| Dependency ID | Upstream → Downstream | BRD Requirement IDs / modules | Type | Criticality | BRD Evidence | Why It Matters |
| --- | --- | --- | --- | --- | --- | --- |
| DEP-001 | CRM → Sales | FR-CRM-001–008 → FR-SALES-001–003 | Flow | Critical | BRD §8 | Qualified leads/opportunities convert into enquiries/quotations without re-entry. |
| DEP-002 | Sales → Inventory / Warehouse | FR-SALES-003–005 → FR-INV-002, FR-WH-003–005 | Flow | Critical | BRD §8 | Sales orders check real-time stock/reserve inventory; dispatch reduces stock. |
| DEP-003 | Sales → MRP & Planning → Manufacturing | FR-SALES-003 → FR-MRP-001–006 → FR-MFG-003–005 | Flow | Critical | BRD §8 | Unmet demand feeds planning and generates production/work orders. |
| DEP-004 | Manufacturing → Quality → Warehouse | FR-MFG-003–005 → FR-QLTY-002–004 → FR-WH-003 | Flow | Critical | BRD §8 | Work-in-process/finished goods pass inspection before warehouse put-away. |
| DEP-005 | Sales / Procurement → Finance & Tax | FR-SALES-003–005; FR-PROC-004–005 → FR-FIN-001–003; FR-TAX-001–007 | Flow | Critical | BRD §8 | Customer/supplier invoices post to GL/AP/AR and receive global-tax classification. |
| DEP-006 | Procurement → Supplier Management | FR-PROC-002–004 → FR-SUPM-003, FR-SUPM-005 | Flow | High | BRD §8 | RFQ/RFP and PO activity feed the supplier performance scorecard. |
| DEP-007 | Asset Management → Maintenance & Field Service | FR-AST-001–006 → FR-MFS-001–007 | Flow | Critical | BRD §8 | Installed assets/warranty generate service requests, work orders, spare-parts consumption, and asset history. |
| DEP-008 | Projects → Finance | FR-PROJ-005–006 → FR-FIN-002–003, FR-FIN-006 | Flow | High | BRD §8 | Project time/expense and billing post to Accounts Receivable and Cost Accounting. |
| DEP-009 | All modules → BI / EPM | All module transactions → FR-BI-001–007; FR-EPM-001–007 | Shared | High | BRD §8 | Every transaction streams to dashboards, KPIs, and budget/forecast variance analysis in real time. |
| DEP-010 | All modules → Workflow & Approvals | All modules → FR-WFA-001–007 | Shared | Critical | BRD §8 | Any module can attach shared KIYA Engine approval/escalation logic. |
| DEP-011 | All modules → Audit, Security & Compliance | All modules → FR-PADM-1.8.1–1.8.6; FR-ASC-001–005 | Shared | Critical | BRD §8 | Every create/update/delete and login event is captured in the audit trail. |

**Critical/high dependency count: 11** — 8 Critical and 3 High. Criticality expresses business/flow consistency impact only; it is not a technical-architecture assessment.

## 4. Business Flow Dependency Analysis

| Flow | BRD sequence | Dependency focus before detailed expansion |
| --- | --- | --- |
| Customer-to-Cash | Lead → Opportunity → Enquiry → Quotation → Sales Order → Availability Check → Inventory → MRP / Planning → Production → Quality Check → Warehouse → Dispatch → Invoice → Tax → Payment → Accounting → Profitability → Customer History | DEP-001 through DEP-005, plus SF-003/SF-005/SF-008/SF-011. |
| Procure-to-Pay | Supplier → RFQ / RFP → Supplier Quotation → Purchase Order → Goods Receipt → Quality Check → Inventory → Supplier Invoice → Tax → Payment → Accounting → Supplier Performance | DEP-005, DEP-006, plus SF-003/SF-005/SF-008/SF-011. |
| Asset-to-Service | Asset / Machine → Installation → Warranty → Service Request → Technician Assignment → Spare Parts → Work Order → Maintenance → Service Invoice → Payment → Asset History | DEP-007, plus SF-003/SF-005/SF-008/SF-011. |

## 5. Clarification Dependencies

| Question ID | Related foundation record(s) | Affected modules / flows | Criticality | Why clarification matters / downstream work |
| --- | --- | --- | --- | --- |
| OQ-001 | All SF records | Modules 02–28; all flows | Critical | Detailed sub-module scope is needed before dependent requirements can be finalized. |
| OQ-002 | SF-003, SF-004, SF-013, SF-014 | All modules; all flows | Critical | Fields, validations, and statuses affect shared masters and transactions. |
| OQ-003 | SF-002, SF-005 | All modules; all flows | Critical | Approval conditions/matrices/escalation govern shared workflow behavior. |
| OQ-004 | SF-006 | All modules; all flows | High | Notification triggers and templates affect shared communication behavior. |
| OQ-005 | SF-003, SF-015 | Tax; Customer-to-Cash; Procure-to-Pay | Critical | Country tax coverage/filing behavior affects invoice/tax requirements. |
| OQ-006 | SF-001, SF-003 | HR & Payroll; Tax | High | Payroll/statutory detail affects HR/tax scope. |
| OQ-007 | SF-003, SF-004 | Sales, Inventory, Warehouse; Customer-to-Cash | Critical | Reservation, valuation, shortage, and availability outcomes affect core flow consistency. |
| OQ-008 | SF-003, SF-004 | MRP, Manufacturing; Customer-to-Cash | Critical | Planning/capacity/work-order rules affect demand-to-production flow. |
| OQ-009 | SF-004 | Quality; Customer-to-Cash; Procure-to-Pay | High | Inspection and NCR/CAPA rules affect quality gates. |
| OQ-010 | SF-003, SF-011 | Procurement, Supplier Management; Procure-to-Pay | High | Scorecard measures determine supplier-performance behavior. |
| OQ-011 | SF-003, SF-004 | Asset, Maintenance & Field Service; Asset-to-Service | Critical | Warranty, dispatch, spare-parts, and billing rules affect the full service flow. |
| OQ-012 | SF-012 | Integration & API; all flows | Critical | Counterparties and data-sync behavior are required to specify shared integration scope. |
| OQ-013 | SF-009 | Mobile; all flows | High | Offline scope and synchronization behavior affect mobile requirements. |
| OQ-014 | SF-010, SF-011 | AI, BI; all flows | High | Governance/access/review criteria control shared AI capabilities. |
| OQ-015 | SF-015, SF-002, SF-011 | All modules; all flows | Critical | Measurable NFR targets are needed to assess platform-wide expectations. |

## 6. Master Data Dependency Analysis

| Conceptual master | Supported dependency finding | Classification | Evidence / limitation |
| --- | --- | --- | --- |
| Customer | Customer Master is a platform master; CRM manages accounts/contacts and Customer 360, Sales leads to customer history, and customer invoices post to AR. | BRD-DERIVED | Supported by FR-PADM-1.4.1, CRM/Sales scope, and BRD §8. Exact ownership/field sharing is TBD. |
| Supplier | Supplier Master, Procurement sourcing/PO activity, Supplier Management performance, and supplier invoices/AP occur in the BRD. | BRD-DERIVED | Supported by FR-PADM-1.4.2, Procurement/Supplier Management scope, and BRD §8. Exact data relationships are TBD. |
| Item | Item Master, Sales availability, procurement receipts, inventory, MRP/manufacturing, quality, and warehouse stages are stated. | BRD-DERIVED | Supported by FR-PADM-1.4.3 and BRD flows/§8. Attributes/ownership are TBD. |
| Warehouse / location | Platform Location includes plant/warehouse; Inventory, Warehouse, Sales, Procurement, Manufacturing, and Quality explicitly participate in related flow stages. | BRD-DERIVED | Supported by FR-PADM-1.1.6 and BRD §6/§8. Separate warehouse-master design is not specified. |
| Employee / user | Employee Master and Users/Roles exist; HR manages employees and field service dispatches technicians. | BRD-DERIVED | Supported by FR-PADM-1.2 and 1.4.4, HR/MFS scope. Exact relationship is TBD. |
| Asset | Asset Management and Maintenance & Field Service are explicitly linked; Finance contains Fixed Assets. | BRD-REQUIRED for Asset→Maintenance; BRD-DERIVED for conceptual Finance relationship | BRD §8 and module scopes. Asset/accounting relationship detail is TBD. |

## 7. Requirements That Should Be Analyzed Together

| Group | BRD-supported basis | Primary records |
| --- | --- | --- |
| Customer + CRM + Sales + Finance/Tax + Customer History | Customer-to-Cash and CRM→Sales/Sales→Finance & Tax dependencies | DEP-001, DEP-005, SF-003 |
| Item + Sales + Inventory + Warehouse + MRP + Manufacturing + Quality | Customer-to-Cash stages and explicit Sales/Manufacturing relationships | DEP-002–004, SF-003 |
| Supplier + Procurement + Supplier Management + Finance/Tax | Procure-to-Pay and Procurement→Supplier Management / Finance & Tax | DEP-005–006, SF-003 |
| Company/Branch + Users/Roles + Security | Platform Administration and global RBAC/security requirements | SF-001–003, SF-008 |
| Workflow + approvals + notifications + audit | Shared KIYA Engine/common features/audit dependency | SF-005, SF-006, SF-008, DEP-010–011 |
| Asset + Maintenance & Field Service + spare parts + service invoice/payment | Asset-to-Service and explicit asset-service dependency | DEP-007, SF-003 |
| Projects + time/expense + billing + Finance | Explicit Projects→Finance dependency | DEP-008 |
| Transactions + BI/EPM | All-modules analytical dependency | DEP-009, SF-011 |

## 8. Traceability and Boundary

Every `SF-*` and `DEP-*` record is an analysis identifier that links to cited BRD evidence and Phase 0A requirements. This map does not expand requirements, answer open questions, define fields/statuses/limits, choose technology, or design APIs, UI, data models, or architecture.
