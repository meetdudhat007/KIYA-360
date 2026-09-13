# KIYA 360 — Module Inventory

All listed requirements are BRD-REQUIRED. Connections appear only where BRD §6/§8 supports them; “Not explicitly specified” means TBD — The BRD does not specify this detail.

## Master Module Table

| # | Module | BRD Scope | BRD Requirements Identified | Business Flow(s) | Connected Modules | Notes |
| --- | --- | --- | ---: | --- | --- | --- |
| 01 | Platform & Administration | BRD-REQUIRED | 50 | All flows | All modules | BRD §7 |
| 02 | CRM | BRD-REQUIRED | 8 | Customer-to-Cash | Sales | BRD §7 |
| 03 | Sales | BRD-REQUIRED | 8 | Customer-to-Cash | CRM; Inventory; Warehouse; MRP & Planning; Manufacturing; Quality; Finance & Accounting; Tax & Statutory Compliance | BRD §7 |
| 04 | Marketing | BRD-REQUIRED | 7 | Not explicitly specified | Not explicitly specified | BRD §7 |
| 05 | Customer Service | BRD-REQUIRED | 7 | TBD — The BRD does not specify a direct module-to-flow mapping. | Not explicitly specified | BRD §7 |
| 06 | Procurement | BRD-REQUIRED | 7 | Procure-to-Pay | Supplier Management; Quality; Inventory; Finance & Accounting; Tax & Statutory Compliance | BRD §7 |
| 07 | Supplier Management | BRD-REQUIRED | 6 | Procure-to-Pay | Procurement | BRD §7 |
| 08 | Inventory | BRD-REQUIRED | 7 | Customer-to-Cash; Procure-to-Pay; Asset-to-Service (spare parts named) | Sales; Procurement; Warehouse; MRP & Planning; Manufacturing; Quality | BRD §7 |
| 09 | Warehouse | BRD-REQUIRED | 7 | Customer-to-Cash | Sales; Inventory; Manufacturing; Quality | BRD §7 |
| 10 | Manufacturing | BRD-REQUIRED | 7 | Customer-to-Cash | MRP & Planning; Quality; Warehouse | BRD §7 |
| 11 | MRP & Planning | BRD-REQUIRED | 7 | Customer-to-Cash | Sales; Manufacturing; Inventory | BRD §7 |
| 12 | Quality | BRD-REQUIRED | 7 | Customer-to-Cash; Procure-to-Pay | Procurement; Manufacturing; Inventory; Warehouse | BRD §7 |
| 13 | Asset Management | BRD-REQUIRED | 7 | Asset-to-Service | Maintenance & Field Service; Finance & Accounting | BRD §7 |
| 14 | Maintenance & Field Service | BRD-REQUIRED | 7 | Asset-to-Service | Asset Management; Inventory | BRD §7 |
| 15 | Logistics & Transportation | BRD-REQUIRED | 7 | Not explicitly specified | Not explicitly specified | BRD §7 |
| 16 | Projects | BRD-REQUIRED | 7 | Not explicitly specified | Finance & Accounting | BRD §7 |
| 17 | Finance & Accounting | BRD-REQUIRED | 7 | Customer-to-Cash; Procure-to-Pay; Asset-to-Service | Sales; Procurement; Tax & Statutory Compliance; Projects | BRD §7 |
| 18 | Tax & Statutory Compliance | BRD-REQUIRED | 7 | Customer-to-Cash; Procure-to-Pay | Sales; Procurement; Finance & Accounting | BRD §7 |
| 19 | HR & Payroll | BRD-REQUIRED | 7 | Not explicitly specified | Not explicitly specified | BRD §7 |
| 20 | E-Commerce | BRD-REQUIRED | 7 | Not explicitly specified | Not explicitly specified | BRD §7 |
| 21 | Document Management | BRD-REQUIRED | 7 | All flows | All modules (key enabler) | BRD §7 |
| 22 | Business Intelligence | BRD-REQUIRED | 7 | All flows | All modules; EPM / Budget / Forecast | BRD §7 |
| 23 | EPM / Budget / Forecast | BRD-REQUIRED | 7 | All flows | All modules; Business Intelligence | BRD §7 |
| 24 | Workflow & Approvals | BRD-REQUIRED | 7 | All flows | All modules | BRD §7 |
| 25 | AI & Automation | BRD-REQUIRED | 7 | All flows | Sales; Inventory; Finance; Maintenance; Service | BRD §7 |
| 26 | Integration & API | BRD-REQUIRED | 7 | All flows | All modules (key enabler) | BRD §7 |
| 27 | Mobile Application | BRD-REQUIRED | 7 | All flows | Sales; Service; BI; Inventory; Workflow & Approvals | BRD §7 |
| 28 | Audit, Security & Compliance | BRD-REQUIRED | 5 | All flows | All modules | BRD §7 |

## Detailed Module Inventory

## Module 01 — Platform & Administration

### Purpose

The foundation controlling companies, users, access, master configuration, numbering, notifications, and system-wide settings.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-PADM-1.1.1 | Company Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.1.2 | Branch Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.1.3 | Business Unit | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.1.4 | Department | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.1.5 | Division | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.1.6 | Location | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.1 | User Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.2 | Role Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.3 | Permission Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.4 | Approval Authority | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.5 | User Groups | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.2.6 | Session Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.1 | Login & Authentication | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.2 | IP Restrictions | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.3 | Device Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.4 | Data Encryption | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.5 | Session Security | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.3.6 | Access Control | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.1 | Customer Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.2 | Supplier Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.3 | Item Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.4 | Employee Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.5 | Tax Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.6 | Currency Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.4.7 | UOM Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.1 | System Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.2 | Financial Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.3 | Sales Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.4 | Purchase Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.5 | Inventory Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.6 | Manufacturing Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.5.7 | Service Settings | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.1 | Document Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.2 | Transaction Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.3 | Master Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.4 | Project Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.5 | Service Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.6.6 | Asset Series | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.1 | Email Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.2 | WhatsApp Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.3 | SMS Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.4 | Push Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.5 | In-App Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.7.6 | Notification Templates | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.1 | Login Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.2 | Data Change Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.3 | Transaction Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.4 | Approval Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.5 | API Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PADM-1.8.6 | Report Log | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 02 — CRM

### Purpose

Manages leads through to a unified customer view across the full relationship lifecycle.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-CRM-001 | Leads | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-002 | Opportunities | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-003 | Accounts | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-004 | Contacts | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-005 | Activities | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-006 | Pipeline Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-007 | Campaigns | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CRM-008 | Customer 360 View | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales.

### Business Flow Connections

Customer-to-Cash.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 03 — Sales

### Purpose

Covers enquiry-to-cash: quotations, orders, pricing, dispatch, returns and analytics.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-SALES-001 | Enquiries | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-002 | Quotations | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-003 | Sales Orders | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-004 | Pricing & Discounts | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-005 | Delivery & Dispatch | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-006 | Returns | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-007 | Credit Memos | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SALES-008 | Sales Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

CRM; Inventory; Warehouse; MRP & Planning; Manufacturing; Quality; Finance & Accounting; Tax & Statutory Compliance.

### Business Flow Connections

Customer-to-Cash.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 04 — Marketing

### Purpose

Plans and measures campaigns and lead-generation activity across channels.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-MKT-001 | Campaigns | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-002 | Email Marketing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-003 | Digital Marketing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-004 | Events & Webinars | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-005 | Lead Generation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-006 | Market Analysis | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MKT-007 | Marketing Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Not explicitly specified.

### Business Flow Connections

Not explicitly specified.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 05 — Customer Service

### Purpose

Handles post-sale support cases, tickets and SLA-driven service delivery.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-CSVC-001 | Case Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-002 | Service Tickets | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-003 | Knowledge Base | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-004 | SLA Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-005 | Customer Feedback | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-006 | Escalations | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-CSVC-007 | Service Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Not explicitly specified.

### Business Flow Connections

TBD — The BRD does not specify a direct Customer Service-to-flow mapping.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 06 — Procurement

### Purpose

Runs requisition-to-receipt procurement with competitive sourcing.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-PROC-001 | Purchase Requisition | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-002 | RFQ / RFP | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-003 | Supplier Quotations | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-004 | Purchase Orders | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-005 | Goods Receipt | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-006 | Returns | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROC-007 | Procurement Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Supplier Management; Quality; Inventory; Finance & Accounting; Tax & Statutory Compliance.

### Business Flow Connections

Procure-to-Pay.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 07 — Supplier Management

### Purpose

Maintains supplier master data, classification, evaluation and a supplier self-service portal.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-SUPM-001 | Supplier Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SUPM-002 | Supplier Classification | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SUPM-003 | Supplier Evaluation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SUPM-004 | Contracts | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SUPM-005 | Performance Scorecard | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-SUPM-006 | Supplier Portal | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Procurement.

### Business Flow Connections

Procure-to-Pay.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 08 — Inventory

### Purpose

Tracks stock quantity, batch/serial, transfers, cycle counts and valuation in real time.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-INV-001 | Item Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-002 | Stock Quantity | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-003 | Batch / Serial Tracking | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-004 | Stock Transfers | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-005 | Cycle Counting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-006 | Stock Valuation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INV-007 | Inventory Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Procurement; Warehouse; MRP & Planning; Manufacturing; Quality.

### Business Flow Connections

Customer-to-Cash; Procure-to-Pay; Asset-to-Service (spare parts named).

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 09 — Warehouse

### Purpose

Manages warehouse layout, inbound/outbound flow and pick-pack-ship execution.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-WH-001 | Warehouse Setup | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-002 | Bin Locations | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-003 | Inbound Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-004 | Outbound Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-005 | Picking & Packing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-006 | Warehouse Transfers | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WH-007 | WMS Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Inventory; Manufacturing; Quality.

### Business Flow Connections

Customer-to-Cash.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 10 — Manufacturing

### Purpose

Manages BOM, routing, work orders and shop-floor production execution and costing.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-MFG-001 | BOM Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-002 | Routing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-003 | Work Orders | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-004 | Production Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-005 | Shop Floor Execution | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-006 | Costing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFG-007 | By-Products / Co-products | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

MRP & Planning; Quality; Warehouse.

### Business Flow Connections

Customer-to-Cash.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 11 — MRP & Planning

### Purpose

Balances demand, material requirements, capacity and supply across production.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-MRP-001 | Demand Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-002 | Material Requirements | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-003 | Capacity Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-004 | Production Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-005 | Supply Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-006 | Schedule Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MRP-007 | MRP Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Manufacturing; Inventory.

### Business Flow Connections

Customer-to-Cash.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 12 — Quality

### Purpose

Enforces inspection and quality control from incoming goods through final inspection, with NCR/CAPA.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-QLTY-001 | Quality Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-002 | Incoming Inspection | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-003 | In-Process Inspection | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-004 | Final Inspection | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-005 | Quality Control | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-006 | NCR / CAPA | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-QLTY-007 | Quality Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Procurement; Manufacturing; Inventory; Warehouse.

### Business Flow Connections

Customer-to-Cash; Procure-to-Pay.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 13 — Asset Management

### Purpose

Tracks fixed assets from classification through depreciation and end-of-life.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-AST-001 | Asset Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-002 | Asset Classification | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-003 | Asset Tracking | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-004 | Asset Depreciation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-005 | Asset Valuation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-006 | Asset Lifecycle | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AST-007 | Asset Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Maintenance & Field Service; Finance & Accounting.

### Business Flow Connections

Asset-to-Service.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 14 — Maintenance & Field Service

### Purpose

Plans preventive/breakdown maintenance and dispatches field service technicians.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-MFS-001 | Maintenance Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-002 | Work Orders | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-003 | Preventive Maintenance | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-004 | Breakdown Maintenance | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-005 | Spare Parts Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-006 | Service Contracts | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MFS-007 | Field Service | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Asset Management; Inventory.

### Business Flow Connections

Asset-to-Service.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 15 — Logistics & Transportation

### Purpose

Plans freight, shipments and carriers with end-to-end tracking and delivery confirmation.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-LOG-001 | Logistics Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-002 | Freight Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-003 | Shipment Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-004 | Carrier Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-005 | Tracking & Tracing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-006 | Delivery Confirmation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-LOG-007 | Logistics Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Not explicitly specified.

### Business Flow Connections

Not explicitly specified.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 16 — Projects

### Purpose

Plans, budgets, executes and bills projects with resource and time tracking.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-PROJ-001 | Project Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-002 | Project Budgeting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-003 | Project Execution | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-004 | Resource Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-005 | Time & Expense | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-006 | Project Billing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-PROJ-007 | Project Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Finance & Accounting.

### Business Flow Connections

Not explicitly specified.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 17 — Finance & Accounting

### Purpose

Core financials — general ledger, payables/receivables, cash, fixed assets and reporting.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-FIN-001 | General Ledger | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-002 | Accounts Payable | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-003 | Accounts Receivable | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-004 | Cash & Bank | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-005 | Fixed Assets | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-006 | Cost Accounting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-FIN-007 | Financial Reporting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Procurement; Tax & Statutory Compliance; Projects.

### Business Flow Connections

Customer-to-Cash; Procure-to-Pay; Asset-to-Service.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 18 — Tax & Statutory Compliance

### Purpose

Applies a global tax engine and country-specific rules across GST/VAT, withholding tax, e-invoicing and statutory filing.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-TAX-001 | Global Tax Engine | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-002 | Country Tax Rules | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-003 | GST / VAT / Sales Tax | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-004 | Withholding Tax | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-005 | E-Invoicing / E-Way Bill | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-006 | Tax Returns | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-TAX-007 | Statutory Reports | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Procurement; Finance & Accounting.

### Business Flow Connections

Customer-to-Cash; Procure-to-Pay.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 19 — HR & Payroll

### Purpose

Manages the employee lifecycle from master data through attendance, payroll and performance.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-HR-001 | Employee Master | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-002 | Organization Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-003 | Attendance & Leave | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-004 | Payroll Processing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-005 | Benefits Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-006 | Performance Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-HR-007 | HR Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Not explicitly specified.

### Business Flow Connections

Not explicitly specified.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 20 — E-Commerce

### Purpose

Runs an online storefront with catalog, cart, checkout and customer self-service.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-ECOM-001 | Online Store | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-002 | Product Catalog | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-003 | Shopping Cart | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-004 | Order Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-005 | Payment Gateway | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-006 | Promotions | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ECOM-007 | Customer Portal | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Not explicitly specified.

### Business Flow Connections

Not explicitly specified.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 21 — Document Management

### Purpose

Centralises document capture, versioning, sharing and e-signature across the platform.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-DOCM-001 | Document Capture | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-002 | Document Storage | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-003 | Version Control | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-004 | Document Sharing | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-005 | Access Control | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-006 | Document Workflow | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-DOCM-007 | Digital Signatures | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules (key enabler).

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 22 — Business Intelligence

### Purpose

Delivers dashboards, KPIs, ad-hoc and predictive analytics on top of every module's data.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-BI-001 | Dashboards | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-002 | Reports | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-003 | KPI Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-004 | Data Visualization | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-005 | Ad-hoc Analysis | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-006 | Predictive Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-BI-007 | BI Mobile App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules; EPM / Budget / Forecast.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 23 — EPM / Budget / Forecast

### Purpose

Supports enterprise performance management: budgeting, forecasting and scenario/variance analysis.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-EPM-001 | Budgeting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-002 | Forecasting | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-003 | Financial Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-004 | Scenario Planning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-005 | Consolidation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-006 | Variance Analysis | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-EPM-007 | EPM Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules; Business Intelligence.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 24 — Workflow & Approvals

### Purpose

A no-code workflow/approval engine used across every module (KIYA Engine).

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-WFA-001 | Workflow Builder | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-002 | Approval Matrix | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-003 | Escalation Rules | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-004 | Delegation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-005 | Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-006 | Audit Trail | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-WFA-007 | Mobile Approvals | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 25 — AI & Automation

### Purpose

Embeds AI insights, predictive analytics, RPA bots and a conversational assistant across the suite.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-AIAU-001 | AI Insights | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-002 | Predictive Analytics | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-003 | Process Automation | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-004 | RPA Bots | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-005 | AI Chat Assistant | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-006 | Anomaly Detection | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-AIAU-007 | Machine Learning | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Inventory; Finance; Maintenance; Service.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 26 — Integration & API

### Purpose

Connects KIYA 360 to third-party systems via managed APIs, webhooks and middleware.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-INTG-001 | API Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-002 | System Integration | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-003 | Data Sync | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-004 | Webhooks | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-005 | Third Party Apps | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-006 | Middleware | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-INTG-007 | Integration Monitoring | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules (key enabler).

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 27 — Mobile Application

### Purpose

Native apps mirroring Sales, Service, Dashboard and Inventory workflows with offline sync.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-MOB-001 | Sales App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-002 | Service App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-003 | Dashboard App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-004 | Offline Sync App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-005 | Inventory App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-006 | Push Notifications | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-MOB-007 | Approvals App | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

Sales; Service; BI; Inventory; Workflow & Approvals.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module 28 — Audit, Security & Compliance

### Purpose

Governs policy, access, data security and risk across the whole platform.

### Scope Classification

BRD-REQUIRED — included in BRD §3.1.

### Functional Requirements

| Requirement ID | Requirement | Classification | BRD Detail | Open Detail |
| --- | --- | --- | --- | --- |
| FR-ASC-001 | Policy Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ASC-002 | Access Control | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ASC-003 | Data Security | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ASC-004 | Risk Management | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |
| FR-ASC-005 | Security Monitoring | BRD-REQUIRED | BRD §7 | TBD — The BRD does not specify this detail. |

### Sub-modules

The preceding BRD capability list is the supported sub-module inventory; no further sub-modules are asserted.

### Connected Modules

All modules.

### Business Flow Connections

All flows.

### Open Questions

See [Open Questions](06-open-questions.md); detailed rules, fields, states, permissions, and exceptions are TBD unless stated by the BRD.

## Module Completeness Check

| Check | Result |
| --- | --- |
| Total BRD modules identified | 28 |
| Expected/current BRD module count | 28 |
| Missing modules | None |
| Unexpected modules | None |
| Requirement IDs checked | Yes |
| Cross-module links checked | Yes |
