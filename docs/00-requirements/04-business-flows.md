# KIYA 360 — Business Flows

All flow sequences below are transcribed from BRD §6. Requirement-to-flow links are recorded in the traceability document.

## Customer-to-Cash

| Aspect | BRD-supported analysis |
| --- | --- |
| Purpose | Sales flow from lead through customer history. |
| Starting point | Lead |
| Major stages | Lead → Opportunity → Enquiry → Quotation → Sales Order → Availability Check → Inventory → MRP / Planning → Production → Quality Check → Warehouse → Dispatch → Invoice → Tax → Payment → Accounting → Profitability → Customer History |
| Ending point | Customer History |
| Modules involved | CRM, Sales, Inventory, MRP & Planning, Manufacturing, Quality, Warehouse, Finance & Accounting, Tax & Statutory Compliance, Business Intelligence; shared enablers apply. |
| Cross-module dependencies | CRM → Sales; Sales → Inventory/Warehouse; Sales → MRP/Planning → Manufacturing; Manufacturing → Quality → Warehouse; Sales → Finance & Tax; all modules → BI/EPM, Workflow, Audit/Security. |
| TBD | Reservation timing, shortage handling, profitability calculation, and transaction/status rules are not specified. |

## Procure-to-Pay

| Aspect | BRD-supported analysis |
| --- | --- |
| Purpose | Supplier flow from sourcing through supplier performance. |
| Starting point | Supplier |
| Major stages | Supplier → RFQ / RFP → Supplier Quotation → Purchase Order → Goods Receipt → Quality Check → Inventory → Supplier Invoice → Tax → Payment → Accounting → Supplier Performance |
| Ending point | Supplier Performance |
| Modules involved | Supplier Management, Procurement, Quality, Inventory, Finance & Accounting, Tax & Statutory Compliance, Business Intelligence; shared enablers apply. |
| Cross-module dependencies | Procurement → Supplier Management; Sales/Procurement → Finance & Tax; all modules → BI/EPM, Workflow, Audit/Security. |
| TBD | Supplier selection, matching rules, returns treatment, payment approvals, and scorecard calculation are not specified. |

## Asset-to-Service

| Aspect | BRD-supported analysis |
| --- | --- |
| Purpose | After-sales flow from installed asset through service history. |
| Starting point | Asset / Machine |
| Major stages | Asset / Machine → Installation → Warranty → Service Request → Technician Assignment → Spare Parts → Work Order → Maintenance → Service Invoice → Payment → Asset History |
| Ending point | Asset History |
| Modules involved | Asset Management and Maintenance & Field Service are explicitly connected. Inventory (spare parts) and Finance & Accounting (service invoice/payment) are BRD-DERIVED from the named flow stages. Customer Service is not mapped to this flow because the BRD does not explicitly state that link; shared enablers apply. |
| Cross-module dependencies | Asset Management → Maintenance & Field Service; all modules → BI/EPM, Workflow, Audit/Security. |
| TBD | Installation recording, warranty rules, dispatch sequencing, spare-parts valuation, and service invoice/payment rules are not specified. |

## Shared Enablers

Workflow & Approvals, Document Management, AI & Automation, Integration & API, Mobile Application, and Audit & Security are identified by BRD §6.4 as key enablers for all flows. The BRD does not specify their flow-specific configuration; that detail is TBD.
