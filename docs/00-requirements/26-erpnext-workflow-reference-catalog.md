# KIYA 360 — ERPNext Workflow Reference Catalog

## 1. Status, Purpose, and Engineering Context

- **Document ID:** 26-erpnext-workflow-reference-catalog
- **Phase:** Phase 0B-1D — ERPNext Workflow Reverse Engineering & KIYA Alignment
- **Status:** Complete / Engineering Reference Catalog
- **Authoritative Business Source:** `source/KIYA360_BRD.pdf` (v2.0, 13 September 2026)
- **Technical Evidence Base:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md` (ERPNext v17.0.0-dev)
- **Controlling Guidelines:** `AGENTS.md`, `.kiya/AI-DECISIONS.md`

### Engineering Purpose
This document provides an engineering-grade reference catalog of the core transactional workflows identified in ERPNext during Document 21 analysis. 
- It documents **how a mature, production-proven ERP engine handles transaction lifecycles, quantity propagation, inventory movements, double-entry accounting effects, cancellations, and validations**.
- It is designed as an architectural and technical reference for later engineering phases when designing KIYA transaction controllers, state machines, and data mappers.
- It **does NOT copy raw source code**, but summarizes exact behavioral contracts, controllers, link fields, and tests.

---

## 2. Global Mechanics and Architectural Patterns

Before detailing individual workflows, five pervasive architectural patterns observed in the ERPNext develop codebase are cataloged:

### 2.1 Dual-Status Architecture
ERPNext combines two distinct status mechanisms:
1. **Frappe `docstatus`:** Document-level state managed by the framework:
   - `0`: Draft (editable, no ledger side-effects).
   - `1`: Submitted (immutable transaction, ledger side-effects posted).
   - `2`: Cancelled (voided, reverse ledger entries posted).
2. **Business `status`:** Managed by `erpnext/controllers/status_updater.py` via `status_map`. Dynamically computed based on `docstatus` and percentage-based completion metrics (`per_delivered`, `per_billed`, `per_received`, `per_ordered`).

### 2.2 Traceable Source-to-Target Mapping (`get_mapped_doc`)
- Cross-document creation uses `frappe.model.mapper.get_mapped_doc`.
- Parent and child rows are copied using explicit field mapping dictionaries.
- Target child rows retain explicit foreign-key references to source child rows (e.g., `so_detail` on Delivery Note Item links to `Sales Order Item.name`).
- Double-mapping prevention: `erpnext/controllers/mapper.py` (`get_qty_already_mapped`) prevents duplicate document creation from unsaved client sessions.

### 2.3 Immutable Ledgers and Reversal Accounting
- ERPNext strictly avoids deleting submitted transactional records.
- Stock movements create immutable `Stock Ledger Entry` (SLE) records.
- Financial transactions create immutable `GL Entry` records.
- **Cancellation:** Setting `docstatus = 2` on a submitted document triggers `make_reverse_gl_entries()` and reverse SLE postings, preserving complete financial and audit history.
- **Returns:** Handled via distinct return documents (`is_return = 1`) referencing the original document (`return_against`), posting negative quantities and values.

---

## 3. Detailed Transactional Workflow Catalog

---

### EWF-01: Commercial Sales Quoting & Order Commitment
- **Workflow ID:** `EWF-01`
- **Workflow Name:** Opportunity → Quotation → Sales Order
- **Relevant ERPNext Modules:** CRM, Selling, Setup
- **Starting Document:** `Opportunity` (`crm/doctype/opportunity/`)
- **Intermediate Documents:** `Quotation` (`selling/doctype/quotation/`)
- **Ending Document:** `Sales Order` (`selling/doctype/sales_order/`)
- **Trigger Mechanisms:** Whitelisted mapper methods: `make_quotation` in `opportunity/mapper.py`, `make_sales_order` in `quotation/mapper.py`.
- **Preconditions:**
  - Opportunity exists and has party details.
  - For Quotation → Sales Order: Quotation must be submitted (`docstatus == 1`) and `valid_till` date must not be expired (unless overridden by Selling Settings `allow_sales_order_creation_for_expired_quotation`).
- **Quantity & Value Propagation:**
  - Child items copied from `Opportunity Item` to `Quotation Item` to `Sales Order Item`.
  - Child link field: `prevdoc_docname` and `quotation_item`.
  - Quotation tracks ordered percentage via `get_ordered_items` and remaining qty.
- **Lifecycle & Status Evolution:**
  - Quotation status: `Draft` → `Open` → `Partially Ordered` → `Ordered` (or `Lost` / `Expired`).
  - Sales Order status: `Draft` → `To Deliver and Bill` (or `To Deliver` / `To Bill`).
- **Financial & Stock Impacts:** None at this stage. (No SLE or GL entries posted).
- **Cancellation & Reversal:**
  - Cancelling Sales Order unwinds `ordered_qty` on Quotation, reverting status from `Ordered` back to `Open`.
- **Relevant Unit Tests:** `crm/doctype/opportunity/test_opportunity.py`, `selling/doctype/sales_order/test_sales_order.py`, `controllers/tests/test_mapper.py`.
- **KIYA Relevance:** Provides proven mechanics for C2C stages 2–5.
- **Critical Limitations:** **No Enquiry document.** ERPNext maps `Opportunity.name` into `Quotation.enq_no`. Lead can also bypass Opportunity and map directly to Quotation.

---

### EWF-02: Sales Order Fulfillment & Inventory Reservation
- **Workflow ID:** `EWF-02`
- **Workflow Name:** Sales Order → Stock Reservation → Delivery Note
- **Relevant ERPNext Modules:** Selling, Stock
- **Starting Document:** `Sales Order` (`selling/doctype/sales_order/`)
- **Intermediate Documents:** `Stock Reservation Entry` (optional), `Pick List` (optional), `Packing Slip`
- **Ending Document:** `Delivery Note` (`stock/doctype/delivery_note/`)
- **Trigger Mechanisms:** `make_delivery_note` in `sales_order/mapper.py`, `create_stock_reservation_entries` in `stock_reservation_entry.py`.
- **Preconditions:**
  - Sales Order must be submitted (`docstatus == 1`).
  - Remaining undelivered quantity must be greater than zero (`delivered_qty < qty`).
  - Warehouse must be specified on each deliverable item row.
- **Quantity & Value Propagation:**
  - Child rows link via `dn_detail` and `so_detail`.
  - Delivery Note updates `delivered_qty` and `per_delivered` on Sales Order Item.
  - Over-delivery checked against `over_delivery_receipt_allowance`; throws `OverAllowanceError` if exceeded.
- **Stock Movement & Valuation:**
  - Submitting Delivery Note triggers `stock_controller.py:make_sl_entries()`.
  - Generates outward `Stock Ledger Entry` (SLE) records reducing `Bin.actual_qty`.
  - If serialized/batched, requires `Serial and Batch Bundle`.
  - Stock Reservation Entry status updates from `Reserved` to `Delivered`.
- **Financial Impact:**
  - If perpetual inventory is enabled, DN submission creates `GL Entry` debiting Cost of Goods Sold (COGS) and crediting Stock In Hand account.
- **Cancellation & Reversal:**
  - Cancelling DN cancels associated SLEs, reverses COGS/Stock GL entries, and decrements `delivered_qty` on the Sales Order.
- **Relevant Unit Tests:** `stock/doctype/delivery_note/test_delivery_note.py`, `stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py`.
- **KIYA Relevance:** Maps to C2C stages 6, 7, 11, 12.
- **Critical Limitations:** Stock Reservation is decoupled and optional; `Bin` does not manage physical aisle/rack coordinates.

---

### EWF-03: Commercial Sales Invoicing & Accounts Receivable
- **Workflow ID:** `EWF-03`
- **Workflow Name:** Delivery Note → Sales Invoice
- **Relevant ERPNext Modules:** Stock, Accounts
- **Starting Document:** `Delivery Note` (`stock/doctype/delivery_note/`) [or Sales Order]
- **Intermediate Documents:** Sales Taxes and Charges calculation (`taxes_and_totals.py`)
- **Ending Document:** `Sales Invoice` (`accounts/doctype/sales_invoice/`)
- **Trigger Mechanisms:** `make_sales_invoice` in `delivery_note/mapper.py` or `sales_order/mapper.py`.
- **Preconditions:**
  - Source Delivery Note submitted (`docstatus == 1`).
  - Remaining unbilled quantity must exist (`billed_amt < grand_total`).
- **Quantity & Value Propagation:**
  - Invoice items link to DN items via `dn_detail` and SO items via `so_detail`.
  - Sales Invoice submission updates `billed_qty` and `per_billed` on source DN and SO.
- **Financial Impact:**
  - Submitting Sales Invoice triggers `accounts/doctype/sales_invoice/sales_invoice.py:make_gl_entries()`.
  - Generates `GL Entry` debiting Customer Account (Debtors) and crediting Income / Tax / Charge accounts.
  - Creates `Payment Ledger Entry` (PLE) tracking outstanding invoice balance.
- **Stock Impact:**
  - None if billed from Delivery Note.
  - *Exception:* If `update_stock` flag is checked on Sales Invoice (direct billing), SI itself generates outward SLEs and COGS GL entries.
- **Cancellation & Reversal:**
  - Cancelling Sales Invoice reverses GL entries, voids PLE entries, and unwinds `per_billed` metrics on DN/SO.
- **Relevant Unit Tests:** `accounts/doctype/sales_invoice/test_sales_invoice.py`, `controllers/tests/test_item_close_billing.py`.
- **KIYA Relevance:** Maps to C2C stages 13, 14, 16.
- **Critical Limitations:** ERPNext allows direct `Sales Order → Sales Invoice` bypassing delivery note (`skip_delivery_note`), which conflicts with KIYA's core sequential C2C flow.

---

### EWF-04: AR Payment Collection & Cash Application
- **Workflow ID:** `EWF-04`
- **Workflow Name:** Sales Invoice → Payment Entry
- **Relevant ERPNext Modules:** Accounts
- **Starting Document:** `Sales Invoice` (`accounts/doctype/sales_invoice/`)
- **Intermediate Documents:** `Payment Entry Reference` (child table)
- **Ending Document:** `Payment Entry` (`accounts/doctype/payment_entry/`)
- **Trigger Mechanisms:** `make_payment_entry` in `accounts_controller.py`.
- **Preconditions:**
  - Sales Invoice submitted with outstanding amount > 0.
- **Quantity & Value Propagation:**
  - Allocates payment amount against specific invoice references.
  - Computes write-offs, deductions, and exchange rate gain/loss.
- **Financial Impact:**
  - Submitting Payment Entry generates `GL Entry` debiting Bank/Cash account and crediting Customer Account (Debtors).
  - Updates outstanding amount on Sales Invoice via `Payment Ledger Entry` reconciliation.
  - Scheduler daily job (`update_invoice_status`) recalculates invoice payment status (`Paid`, `Partly Paid`, `Overdue`).
- **Cancellation & Reversal:**
  - Cancelling Payment Entry reverses bank/debtor GL entries and restores outstanding balance on Sales Invoice.
- **Relevant Unit Tests:** `accounts/doctype/payment_entry/test_payment_entry.py`.
- **KIYA Relevance:** Maps to C2C stage 15.
- **Critical Limitations:** Pure financial settlement; does not automatically trigger customer satisfaction or after-sales surveys.

---

### EWF-05: Sourcing & Purchase Order Commitment
- **Workflow ID:** `EWF-05`
- **Workflow Name:** Material Request → RFQ → Supplier Quotation → Purchase Order
- **Relevant ERPNext Modules:** Stock, Buying
- **Starting Document:** `Material Request` (`stock/doctype/material_request/`)
- **Intermediate Documents:** `Request for Quotation` (`buying/doctype/request_for_quotation/`), `Supplier Quotation` (`buying/doctype/supplier_quotation/`)
- **Ending Document:** `Purchase Order` (`buying/doctype/purchase_order/`)
- **Trigger Mechanisms:** `make_rfq` from Material Request; `make_supplier_quotation` from RFQ; `make_purchase_order` from Supplier Quotation.
- **Preconditions:**
  - Material Request submitted with purpose `Purchase`.
  - Active vendor list attached to RFQ.
- **Quantity & Value Propagation:**
  - Material Request updates `indented_qty` on `Bin`.
  - PO submission increments `ordered_qty` on `Bin` and updates `per_ordered` on Material Request.
  - Links: `material_request_item` and `supplier_quotation_item`.
- **Financial & Stock Impacts:** None at this stage. Budget validation checked via `budget_controller.py`.
- **Cancellation & Reversal:**
  - Cancelling PO decrements `ordered_qty` on Bin and re-opens Material Request/Supplier Quotation.
- **Relevant Unit Tests:** `buying/doctype/purchase_order/test_purchase_order.py`, `buying/report/supplier_quotation_comparison/test_supplier_quotation_comparison.py`.
- **KIYA Relevance:** Maps to P2P stages 1–4.
- **Critical Limitations:** **No RFP DocType exists.** RFQ cannot manage complex multi-attribute technical/commercial sealed bids.

---

### EWF-06: Goods Receipt & Quality Gating
- **Workflow ID:** `EWF-06`
- **Workflow Name:** Purchase Order → Quality Inspection → Purchase Receipt
- **Relevant ERPNext Modules:** Buying, Stock
- **Starting Document:** `Purchase Order` (`buying/doctype/purchase_order/`)
- **Intermediate Documents:** `Quality Inspection` (`stock/doctype/quality_inspection/`)
- **Ending Document:** `Purchase Receipt` (`stock/doctype/purchase_receipt/`)
- **Trigger Mechanisms:** `make_purchase_receipt` in `purchase_order/mapper.py`.
- **Preconditions:**
  - PO submitted with remaining unreceived quantity.
  - If Item has `inspection_required_before_purchase`, Quality Inspection must be submitted and Accepted prior to PR submission.
- **Stock Movement & Valuation:**
  - Submitting Purchase Receipt triggers `stock_controller.py:make_sl_entries()`.
  - Generates inward SLE increasing `Bin.actual_qty`.
  - Assigns serial numbers and batch bundles via `Serial and Batch Bundle`.
  - Rejected stock routed to designated `rejected_warehouse`.
- **Financial Impact:**
  - Submitting PR creates provisional accounting `GL Entry`: debits Stock In Hand (or Stock Received But Not Billed) and credits Stock Received But Not Billed accrual account.
- **Cancellation & Reversal:**
  - Cancelling PR cancels inward SLE, reverses stock accrual GL entries, and restores `per_received` on PO.
- **Relevant Unit Tests:** `stock/doctype/purchase_receipt/test_purchase_receipt.py`.
- **KIYA Relevance:** Maps to P2P stages 5, 6, 7.
- **Critical Limitations:** Quality Inspection rejection puts stock into rejected warehouse, but does NOT automatically generate a formal Non-Conformance (NCR) record.

---

### EWF-07: 3-Way Match AP Invoicing & Disbursement
- **Workflow ID:** `EWF-07`
- **Workflow Name:** Purchase Receipt → Purchase Invoice → Payment Entry
- **Relevant ERPNext Modules:** Stock, Accounts
- **Starting Document:** `Purchase Receipt` (`stock/doctype/purchase_receipt/`) [or PO]
- **Intermediate Documents:** `Purchase Invoice` (`accounts/doctype/purchase_invoice/`)
- **Ending Document:** `Payment Entry` (`accounts/doctype/payment_entry/`)
- **Trigger Mechanisms:** `make_purchase_invoice` from PR; `make_payment_entry` from PI.
- **Preconditions:**
  - Purchase Receipt submitted.
  - 3-way matching validation: Invoiced quantity and rate checked against PR (`pr_detail`) and PO (`po_detail`).
- **Financial Impact:**
  - Submitting Purchase Invoice clears provisional Stock Received But Not Billed accrual and books real Accounts Payable (Creditors) liability and tax accounts.
  - Submitting Payment Entry debits Creditors and credits Bank account.
- **Cancellation & Reversal:**
  - Reverse GL entries posted for both Invoice and Payment cancellation.
- **Relevant Unit Tests:** `accounts/doctype/purchase_invoice/test_purchase_invoice.py`.
- **KIYA Relevance:** Maps to P2P stages 8–11.
- **Critical Limitations:** India GST Input Tax Credit (ITC) reconciliation is absent in the analyzed tree.

---

### EWF-08: Manufacturing Demand Explosion & Planning
- **Workflow ID:** `EWF-08`
- **Workflow Name:** Sales Demand → Production Plan → Work Order
- **Relevant ERPNext Modules:** Selling, Manufacturing
- **Starting Document:** `Sales Order` (or `Sales Forecast`)
- **Intermediate Documents:** `Production Plan` (`manufacturing/doctype/production_plan/`)
- **Ending Document:** `Work Order` (`manufacturing/doctype/work_order/`), `Material Request`
- **Trigger Mechanisms:** Production Plan queries unreserved Sales Orders; calls `make_work_order` via `production_plan/services/work_order_planning.py`.
- **Preconditions:**
  - Valid, active `BOM` must exist for each planned manufactured item.
- **Planning Explosion:**
  - Production Plan explodes multi-level BOMs.
  - Computes raw material shortages against `Bin.projected_qty`.
  - Generates Purchase Material Requests for shortages and Work Orders for sub-assemblies/assemblies.
  - Optional reservation: creates `Stock Reservation Entry` for raw materials.
- **Relevant Unit Tests:** `manufacturing/doctype/production_plan/test_production_plan.py`.
- **KIYA Relevance:** Maps to C2C stage 8.
- **Critical Limitations:** Production Plan is a basic unconstrained planning engine; lacks finite capacity scheduling, bottleneck scheduling, and dynamic lead-time simulation.

---

### EWF-09: Discrete Shop Floor Execution & FG Receipt
- **Workflow ID:** `EWF-09`
- **Workflow Name:** BOM → Work Order → Stock Entry → Job Card → Finished Goods
- **Relevant ERPNext Modules:** Manufacturing, Stock
- **Starting Document:** `BOM` (`manufacturing/doctype/bom/`)
- **Intermediate Documents:** `Work Order`, `Stock Entry` (Material Transfer for Manufacture), `Job Card`
- **Ending Document:** `Stock Entry` (Manufacture)
- **Trigger Mechanisms:** Work Order submission creates Job Cards and transfers raw materials. Job Cards track actual labor.
- **Stock Movement & Valuation:**
  - Stage 1: Stock Entry (Material Transfer) moves raw materials from stores to WIP warehouse.
  - Stage 2: Job Cards track operation time, workstation cost, and operator.
  - Stage 3: Stock Entry (Manufacture) consumes WIP materials and produces Finished Goods into target warehouse.
  - SLEs post raw material reduction and FG inventory addition.
  - GL entries post WIP transfer and manufacturing cost capitalization.
- **Relevant Unit Tests:** `manufacturing/doctype/work_order/test_work_order.py`, `manufacturing/doctype/job_card/test_job_card.py`.
- **KIYA Relevance:** Maps to C2C stages 9, 10.
- **Critical Limitations:** Direct operator interfaces and machine IoT data capture are not part of core ERPNext.

---

### EWF-10: Capital Asset Acquisition & Depreciation
- **Workflow ID:** `EWF-10`
- **Workflow Name:** Purchase Receipt → Asset → Depreciation Schedule → GL Posting
- **Relevant ERPNext Modules:** Buying, Assets, Accounts
- **Starting Document:** `Purchase Receipt` (with fixed asset item)
- **Intermediate Documents:** `Asset` (`assets/doctype/asset/`), `Asset Depreciation Schedule`
- **Ending Document:** `Journal Entry` (Monthly Depreciation GL)
- **Trigger Mechanisms:** `buying_controller.make_asset` generates Asset; submission calculates depreciation schedule; scheduler hook executes daily depreciation posting.
- **Financial Impact:**
  - Monthly scheduler job (`post_depreciation_entries`) debits Depreciation Expense and credits Accumulated Depreciation accounts.
  - Scrapping or sale creates Asset Disposal GL entries.
- **Relevant Unit Tests:** `assets/doctype/asset/test_asset.py`.
- **KIYA Relevance:** Maps to internal asset management (FR-AST-001–006).
- **Critical Limitations:** ERPNext `Asset` is strictly for company-owned capitalized property. Customer-owned equipment is completely unrepresented in this module.

---

### EWF-11: Customer Warranty & Equipment Servicing
- **Workflow ID:** `EWF-11`
- **Workflow Name:** Customer Incident → Warranty Claim → Maintenance Visit
- **Relevant ERPNext Modules:** Support, Maintenance
- **Starting Document:** `Warranty Claim` (`support/doctype/warranty_claim/`)
- **Intermediate Documents:** `Maintenance Visit` (`maintenance/doctype/maintenance_visit/`)
- **Ending Document:** `Sales Invoice` (optional service billing)
- **Trigger Mechanisms:** Customer files warranty claim against serialized item; support agent schedules Maintenance Visit.
- **Preconditions:**
  - Serial No must have valid warranty dates or active maintenance schedule.
- **Execution & Status:**
  - Maintenance Visit logs engineer, visit date, checklist, and inspected serial numbers.
  - Claim status updates from `Open` to `Work In Progress` to `Closed`.
- **Relevant Unit Tests:** `support/doctype/warranty_claim/test_warranty_claim.py`.
- **KIYA Relevance:** Maps to A2S stages 3, 4, 8, 9.
- **Critical Limitations:** Completely lacks mobile GPS tracking, technician route dispatching, and truck-stock spare parts consumption. "Work Order" is not used here due to naming collision with manufacturing.

---

### EWF-12: Professional Services Billing
- **Workflow ID:** `EWF-12`
- **Workflow Name:** Project → Task → Timesheet → Sales Invoice
- **Relevant ERPNext Modules:** Projects, Accounts
- **Starting Document:** `Project` (`projects/doctype/project/`)
- **Intermediate Documents:** `Task`, `Timesheet` (`projects/doctype/timesheet/`)
- **Ending Document:** `Sales Invoice`
- **Trigger Mechanisms:** `timesheet.py:make_sales_invoice()`.
- **Preconditions:**
  - Timesheet submitted with `is_billable == 1` and unbilled hours > 0.
- **Financial Impact:**
  - Sales Invoice created with line items representing billable task hours, multiplying hours by billing rate.
  - SI submission records revenue against project cost center.
- **Relevant Unit Tests:** `projects/doctype/timesheet/test_timesheet.py`.
- **KIYA Relevance:** Maps to supporting workflow 4.1.
- **Critical Limitations:** Focuses on pure time-and-materials billing; milestone-based progress billing requires manual invoice configuration.

---

## 4. Summary Matrix of ERPNext Workflows

| ID | Workflow Name | Starting Doc | Ending Doc | Stock Impact | Financial Impact | Cancellation Handling | Reuse Quality |
|---|---|---|---|---|---|---|---|
| **EWF-01** | Sales Quoting & Order | Opportunity | Sales Order | None | None | Status unwind | High / Core |
| **EWF-02** | Fulfillment & Reservation | Sales Order | Delivery Note | Outward SLE | COGS/Stock GL | Reverse SLE/GL | High / Core |
| **EWF-03** | Commercial Invoicing | Delivery Note | Sales Invoice | None (unless direct) | AR / Income GL | Reverse GL | High / Core |
| **EWF-04** | AR Payment Collection | Sales Invoice | Payment Entry | None | Bank/AR GL | Reverse GL | High / Core |
| **EWF-05** | Purchasing & Sourcing | Material Request | Purchase Order | Bin indented/ordered | Budget check | Unwind Bin qty | High / Core |
| **EWF-06** | Receiving & QI Gate | Purchase Order | Purchase Receipt | Inward SLE | Stock Accrual GL | Reverse SLE/GL | High / Core |
| **EWF-07** | 3-Way Match Invoicing | Purchase Receipt | Purchase Invoice | None | AP / Accrual GL | Reverse GL | High / Core |
| **EWF-08** | MRP & Demand Planning | Sales Order | Work Order | Bin planned | None | Cancel WO | Medium / Adapt |
| **EWF-09** | Shop Floor Discrete Mfg | BOM | Finished Goods | WIP / FG SLE | Mfg Cost GL | Reverse SLE/GL | High / Core |
| **EWF-10** | Asset Depreciation | Purchase Receipt | Monthly Depr GL | None | Depr Expense GL | Reverse GL | High / Core |
| **EWF-11** | Customer Equipment Svc | Warranty Claim | Maintenance Visit | None | None | Cancel Visit | Low / Ref Only |
| **EWF-12** | Services Project Billing | Project | Sales Invoice | None | Project Rev GL | Reverse GL | High / Core |

---

## 5. Document Metadata & Traceability

- **Created:** 14 September 2026
- **Baseline Document Reference:** `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`, `22-erpnext-kiya-workflow-alignment-matrix.md`
- **Output Artifacts:** Feeds directly into `docs/00-requirements/27-erpnext-analysis-review.md`.
