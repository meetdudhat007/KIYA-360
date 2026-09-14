# KIYA 360 — ERPNext Workflow Reverse Engineering

## Status and boundary

**Phase 0B-1D analysis. Reference material only.** This document describes how the uploaded ERPNext develop tree implements selected ERP workflows. It is not a KIYA business specification, not a platform selection, and not an architecture decision.

- Repository: `references/erpnext-develop/`
- App version: `17.0.0-dev` (`erpnext/__init__.py`)
- License declared: GNU General Public License v3 (`erpnext/hooks.py`)
- Python requirement: `>=3.14` (`pyproject.toml`)
- Modules declared: `erpnext/modules.txt`

KIYA BRD v2.0 remains the business source of truth. ERPNext field names, statuses, and validation rules must not be copied into KIYA requirements unless a later approved CD/architecture decision explicitly says so.

## Evidence standard

| Tag | Meaning |
| --- | --- |
| source-derived | Observed in the cited ERPNext file/symbol |
| inference | Bounded reading of how the code is intended to operate |
| recommendation | Non-binding analysis suggestion for later KIYA work |
| TBD | This repository does not prove the claim |

`ERPNext-REFERENCE` and `ERPNext-SPECIFIC` are analysis labels used only in docs 21–27. They are not KIYA requirement classifications and cannot become `BRD-REQUIRED`.

Frappe Framework is **not** in this repository. Users, roles, DocType engine, `docstatus`, numbering series, attachments, notifications, REST/RPC, and generic cancel/amend mechanics are **outside this repository / Frappe-owned** unless ERPNext extends them. Absence from this tree is not proof that Frappe lacks the capability.

## Shared transaction mechanics (source-derived)

ERPNext transactional documents typically use Frappe `docstatus` 0 Draft / 1 Submitted / 2 Cancelled, then overlay a business `status` computed by `StatusUpdater`.

| Mechanism | Evidence | What it does |
| --- | --- | --- |
| Status overlay | `erpnext/controllers/status_updater.py` `status_map` | Maps Lead, Opportunity, Quotation, SO, PO, DN, PR, Material Request, Pick List, POS, etc. to business statuses from `docstatus`, `per_delivered`, `per_billed`, `per_received`, `per_ordered` |
| Qty/amount against source | same file `StatusUpdater` | Delivery Note updates delivered qty/percent; Sales Invoice updates billed amount/percent; over-delivery/over-billing raises `OverAllowanceError` |
| Source→target mapping | `frappe.model.mapper.get_mapped_doc` used from module `mapper.py` files; helper `erpnext/controllers/mapper.py` `get_qty_already_mapped` | Copies parent/child rows and remaining qty; child link fields such as `so_detail`, `dn_detail`, `po_detail`, `quotation_item` |
| Selling/buying totals & tax | `erpnext/controllers/taxes_and_totals.py`; `accounts_controller.py` | Item taxes, template taxes, grand total; default taxes loaded in Opportunity→Quotation mapper |
| Stock + perpetual inventory GL | `erpnext/controllers/stock_controller.py` `make_sl_entries`, `make_gl_entries` | Stock Ledger Entries; GL when perpetual inventory (or provisional/non-stock/asset PR) is enabled |
| Returns | `erpnext/controllers/sales_and_purchase_return.py` `validate_return`, `make_return_doc` | Negative qty against original submitted document; party/company match |
| Budget | `erpnext/controllers/budget_controller.py` | Budget checks on accounting documents (ERPNext-SPECIFIC vs KIYA EPM) |

Cancellation of submitted stock/accounting documents posts reverse SLE/GL rather than deleting history (`stock_controller.py` `make_gl_entries_on_cancel`; Sales Invoice `on_cancel` → `make_gl_entries_on_cancel`).

---

## Structural inventory (behavior-relevant, not a file dump)

### Accounts

- **DocTypes:** Account, Sales Invoice, Purchase Invoice, Payment Entry, Journal Entry, GL Entry, Payment Ledger Entry, Fiscal Year, Cost Center, Budget, POS Opening/Closing, Process Statement of Accounts, Bank Transaction.
- **Child tables:** Sales/Purchase Invoice Item, taxes and charges tables, Payment Entry Reference.
- **Controllers:** `accounts_controller.py`, `taxes_and_totals.py`; `accounts/doctype/sales_invoice/sales_invoice.py`; `payment_entry.py`; `accounts/general_ledger.py`.
- **Lifecycle:** SI `on_submit` / `on_cancel` make/reverse GL (`sales_invoice.py`). Daily `update_invoice_status` (`hooks.py` scheduler).
- **Mappers:** `sales_invoice/mapper.py` `make_delivery_note`; `purchase_invoice/mapper.py` `make_purchase_receipt`; reverse DN/PR→invoice mappers under stock.
- **Tests:** `accounts/doctype/sales_invoice/test_sales_invoice.py`, `purchase_invoice/test_purchase_invoice.py`, `payment_entry` tests.
- **Depends on:** Selling, Buying, Stock, Projects (timesheets), Assets, Regional hooks.

### CRM

- **DocTypes:** Lead, Opportunity, Prospect, Campaign, Email Campaign, Contract, Appointment.
- **Child:** Opportunity Item.
- **Mappers:** `crm/doctype/lead/mapper.py` (`make_customer`, `make_opportunity`, `make_quotation`); `opportunity/mapper.py` (`make_quotation`, `make_request_for_quotation`).
- **Status:** `status_map` Lead: Opportunity / Quotation / Converted / Lost Quotation; Opportunity: Quotation / Converted / Lost / Closed.
- **Tests:** `crm/doctype/opportunity/test_opportunity.py`.
- **Depends on:** Selling (Quotation), Buying (RFQ from opportunity), Setup Customer/Contact (Frappe contacts).

### Selling

- **DocTypes:** Quotation, Sales Order, Installation Note, Product Bundle, Selling Settings.
- **Child:** Quotation Item, Sales Order Item, Packed Item, Sales Team.
- **Mappers:** `selling/doctype/quotation/mapper.py` `make_sales_order`; `sales_order/mapper.py` `make_delivery_note`, `make_sales_invoice`, `make_material_request`.
- **Status:** Quotation Draft/Open/Lost/Partially Ordered/Ordered; SO To Deliver and Bill / To Bill / To Deliver / Completed / Closed / On Hold / To Pay.
- **Tests:** `selling/doctype/sales_order/test_sales_order.py`; `controllers/tests/test_mapper.py`.
- **Depends on:** CRM, Stock, Accounts, Manufacturing (Production Plan import of SOs).

### Buying

- **DocTypes:** Supplier, Request for Quotation, Supplier Quotation, Purchase Order, Buying Settings, Supplier Scorecard (+ Criteria/Variable/Standing/Period).
- **Mappers:** `material_request/mapper.py`; `buying/doctype/supplier_quotation/mapper.py` `make_purchase_order`; `purchase_order/mapper.py` `make_purchase_receipt`, `make_purchase_invoice`.
- **No RFP DocType** in this tree (source-derived: buying doctypes listed above).
- **Scheduler:** `supplier_scorecard.refresh_scorecards` daily (`hooks.py`).
- **Depends on:** Stock (MR, PR), Accounts (PI, Payment), Portal (supplier RFQ response — Frappe web).

### Stock

- **DocTypes:** Item, Warehouse, Bin, Stock Ledger Entry, Stock Entry, Delivery Note, Purchase Receipt, Material Request, Stock Reservation Entry, Serial No, Batch, Serial and Batch Bundle, Pick List, Packing Slip, Delivery Trip, Quality Inspection, Landed Cost Voucher, Stock Settings.
- **Controllers:** `stock_controller.py`; `stock/stock_ledger.py`; `serial_batch_bundle`.
- **Bin meaning (ERPNext-SPECIFIC):** one Bin row per Item+Warehouse with `actual_qty`, `reserved_qty`, `projected_qty` — not a physical bin location (`stock/doctype/bin/bin.py`).
- **Depends on:** Accounts (perpetual inventory), Manufacturing (WO stock entries), Buying/Selling.

### Manufacturing

- **DocTypes:** BOM, BOM Item/Operation, Routing, Operation, Workstation, Production Plan, Work Order, Job Card, Master Production Schedule, Sales Forecast, Manufacturing Settings, Downtime Entry.
- **Services:** `production_plan/services/work_order_planning.py`, `sales_order_planning.py`, `reservation.py`; `work_order/services/reservation.py`.
- **Mappers:** `work_order/mapper.py`; Production Plan `make_work_order`.
- **Depends on:** Stock (Stock Entry, SRE), Quality Inspection (Job Card / Stock Entry references), Sales Order.

### Quality Management vs Quality Inspection

- **quality_management:** Quality Goal, Procedure, Review, Meeting, Feedback, Action, **Non Conformance** (`status` Open/Resolved/Cancelled; corrective/preventive text — `non_conformance.json`).
- **Quality Inspection** lives under **Stock**, not Quality Management (`stock/doctype/quality_inspection/`). Types Incoming / Outgoing / In Process; status Accepted / Rejected / Cancelled; `reference_type` includes PR, PI, DN, SI, Stock Entry, Job Card, Subcontracting Receipt.

These two areas are weakly linked in this tree (inference): QI reject does not automatically create Non Conformance in the QI class header inspected.

### Assets / Maintenance / Support / Projects

- **Assets:** Asset (`get_status`: Draft, Work In Progress, Submitted, Partially/Fully Depreciated, Scrapped, Cancelled; maintenance overlay In Maintenance / Out of Order — `assets/doctype/asset/asset.py`), Asset Depreciation Schedule, Asset Repair, Asset Maintenance Log, Asset Movement, Asset Capitalization.
- **Maintenance module:** Maintenance Schedule, Maintenance Visit (not manufacturing Work Order).
- **Support:** Issue (SLA via `service_level_agreement` hooked on all validates), Warranty Claim (`status` Open/Closed/Work In Progress/Cancelled; `warranty_amc_status`).
- **Projects:** Project, Task, Timesheet; `timesheet.py` `make_sales_invoice` bills remaining billable hours.

### Setup

Company, Branch, Department, Employee (master only in this app), Customer Group, Supplier Group, Item Group, Territory, Sales Person, UOM, Currency Exchange, Global Defaults, Authorization Rule, Transaction Deletion Record. **Currency** as a DocType is Frappe-owned (outside this repo). Customer lives in ERPNext selling/setup depending on version; Supplier in buying.

### Regional

Present: United States, UAE, Italy, South Africa, Turkey, Australia; reports IRS 1099, UAE VAT 201, VAT audit, electronic invoice register (Italy).

**India GST/e-invoice/e-way bill are not implemented in this tree.** Patch `erpnext/patches/v14_0/remove_india_localisation.py` deletes GST DocTypes and tells operators to install **India Compliance**. Depreciation notes “Overwritten via India Compliance app” (`assets/doctype/asset/depreciation.py`).

### Portal, Telephony, EDI, Integrations, Utilities, Subcontracting

- **Portal:** `portal/utils.py`, website filter/attribute doctypes; supplier/customer web flows use Frappe website (outside repo for engine).
- **Telephony:** Call Log (code-only module mapped to ERPNext Integrations in `hooks.py`).
- **EDI:** Code List / Common Code (`hooks.py` code_only_modules).
- **ERPNext Integrations:** Plaid, etc. (`hooks.py` hourly Plaid sync).
- **Utilities:** bulk transaction retry; Video.
- **Subcontracting:** Subcontracting Order/Receipt; `subcontracting_controller.py`; tests in `controllers/tests/test_subcontracting_controller.py`.

### Tests and patches

Tests sit beside DocTypes (`test_*.py`) and under `erpnext/controllers/tests/`. `erpnext/patches.txt` plus versioned `erpnext/patches/` document model evolution (India localisation removal is the most KIYA-relevant patch). Tests demonstrate intended behavior; they are not proof of zero defects.

---

## Workflow reverse engineering

Each workflow uses KIYA relevance pointers to docs 22–23. ERPNext names are not KIYA names.

### WF-01 Lead → Opportunity → Quotation → Sales Order

| Aspect | ERPNext behavior (source-derived) |
| --- | --- |
| Starting entity | Lead (`crm/doctype/lead/`) |
| Trigger | User mapping (whitelisted `make_*`); not an automatic pipeline engine |
| Preconditions | Lead exists; Quotation→SO blocked if `valid_till` expired unless Selling Settings `allow_sales_order_creation_for_expired_quotation` (`quotation/mapper.py`) |
| Documents created | Customer (`lead/mapper.py` `make_customer`); Opportunity (`make_opportunity`); Quotation from Lead or Opportunity; Sales Order from Quotation (`make_sales_order`); optional Customer from quotation party |
| Important fields | Opportunity `opportunity_from`/`party_name`; Quotation `quotation_to`, `enq_no` mapped from Opportunity.name; child `prevdoc_docname`; SO `quotation_item` remaining qty |
| Status | Lead/Opportunity/Quotation maps in `status_updater.py` |
| Validation | Quotation expiry; remaining stock_qty vs already ordered (`get_ordered_items` + `get_qty_already_mapped`) |
| Linked records | Opportunity Item → Quotation Item; Quotation Item → Sales Order Item |
| Qty propagation | Partial order: Quotation Partially Ordered vs Ordered |
| Inventory | None until later reservation/delivery |
| Accounting/tax | Quotation mapper loads Sales Taxes and Charges Template and `calculate_taxes_and_totals` |
| Cancellation | Frappe cancel of submitted Quotation/SO; status Cancelled; cannot treat as KIYA cancel policy (TBD OQ-002) |
| Downstream | SO can create DN, SI, Material Request, feed Production Plan |
| Reports | Selling analytics reports (module reports; not enumerated) |
| Tests | `controllers/tests/test_mapper.py`; `crm/doctype/opportunity/test_opportunity.py`; `selling/doctype/sales_order/test_sales_order.py` |
| ERPNext-SPECIFIC | Direct Lead→Quotation skip; `enq_no` is Opportunity name, **not** a KIYA Enquiry document; no separate Enquiry DocType |
| KIYA relevance | C2C Lead→Opportunity→Enquiry→Quotation→SO — see 22. Coverage Partial. OQ-001/002 |

### WF-02 Sales Order → stock/reservation → Delivery

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | Submitted Sales Order |
| Trigger | `sales_order/mapper.py` `make_delivery_note`; optional Stock Reservation Entry from SO; optional Pick List |
| Preconditions | `docstatus==1`; remaining qty vs `delivered_qty`; warehouse on item; not skip_delivery_note for delivery path |
| Documents | Delivery Note; Stock Reservation Entry; Pick List; packing/trip optional (`Packing Slip`, `Delivery Trip`) |
| Fields | SO Item `warehouse`, `delivered_qty`; DN `against_sales_order`, `so_detail`; SRE voucher link |
| Status | SO `per_delivered` drives To Deliver / To Deliver and Bill / Completed |
| Validation | Over-delivery allowance (`StatusUpdater` OverAllowanceError); stock availability depends on Stock Settings / SRE |
| Inventory | DN submit: SLE via `stock_controller`; Bin actual_qty decreases; SRE status Reserved → Delivered (`stock_reservation_entry.py` `update_status`) |
| Accounting | Perpetual inventory GL on DN if enabled |
| Tax | Selling taxes on DN if configured; often billed on SI |
| Cancellation | DN cancel reverses SLE/GL and reduces delivered_qty on SO |
| Tests | `test_sales_order.py`; `stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py`; `stock/doctype/delivery_note` tests |
| ERPNext-SPECIFIC | Reservation is optional DocType SRE, not implied by SO submit; Bin is not a location |
| KIYA | Availability Check / Inventory / Dispatch — OQ-007. Partial |

### WF-03 Delivery → Sales Invoice

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | Submitted Delivery Note |
| Trigger | `delivery_note/mapper.py` `make_sales_invoice`; also SO `make_sales_invoice` can skip DN (`skip_delivery_note`) |
| Documents | Sales Invoice with `dn_detail` / against DN |
| Status | DN To Bill / Partially Billed / Completed via `per_billed` |
| Qty | Billed qty/amount against DN/SO |
| Inventory | Usually none additional (already issued on DN); update_stock invoices can issue stock from SI instead |
| Accounting | SI `on_submit` `make_gl_entries` (`sales_invoice.py`) |
| Cancellation | SI cancel reverses GL; billed percents unwind |
| Tests | sales_invoice and delivery_note tests; `controllers/tests/test_item_close_billing.py` |
| KIYA | Dispatch → Invoice. Partial. Update-stock-on-invoice is ERPNext-SPECIFIC vs BRD warehouse-then-invoice sequence |

### WF-04 Sales Invoice → accounting → Payment

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | Submitted Sales Invoice |
| Trigger | Payment Entry against outstanding; advances also exist (`advance_payment_status` on SO) |
| Documents | Payment Entry; Payment Ledger Entry; GL Entry |
| Status | Invoice status updated daily `accounts_controller.update_invoice_status` |
| Accounting | Debit party / credit bank or cash; outstanding reduced |
| Tax | Tax already on invoice GL; payment generally does not recompute tax (inference from PE vs SI split) |
| Cancellation | Payment cancel reverses PE GL and restores outstanding |
| Tests | `payment_entry` tests; SI tests for outstanding |
| KIYA | Invoice → Tax → Payment → Accounting. Tax engine completeness is not this workflow — see Regional/India gap. OQ-005 |

### WF-05 Material Request → RFQ → Supplier Quotation → Purchase Order

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | Material Request (`stock/doctype/material_request/`) types Purchase / Manufacture / Transfer / Issue / Subcontracting / Customer Provided |
| Trigger | `material_request/mapper.py` `make_purchase_order` and RFQ mappers; RFQ `RequestforQuotation` (`buying/doctype/request_for_quotation/`) |
| Documents | RFQ (+ supplier child table); Supplier Quotation; Purchase Order (`supplier_quotation/mapper.py` `make_purchase_order`) |
| Status | MR Pending / Partially Ordered / Ordered / Received per `status_map`; SQ Draft/Submitted/Partially Ordered/Ordered |
| Inventory | MR updates `indented_qty` on Bin via stock hooks; PO updates `ordered_qty` |
| Accounting | None until receipt/invoice |
| ERPNext-SPECIFIC | **No RFP document.** RFQ is price-request oriented with supplier emails/PDF (`request_for_quotation.py`) |
| Tests | buying RFQ/SQ/PO tests; `buying/report/supplier_quotation_comparison/test_supplier_quotation_comparison.py` |
| KIYA | FR-PROC-001/002/003/004. RFP Absent-in-repo. OQ-001 |

### WF-06 Purchase Order → Purchase Receipt

| Aspect | ERPNext behavior |
| --- | --- |
| Trigger | `purchase_order/mapper.py` `make_purchase_receipt` |
| Status | PO `per_received` To Receive / To Receive and Bill / Completed |
| Inventory | PR submit SLE inward; Bin actual_qty; optional QI gate (`stock_controller` `make_quality_inspections`) |
| Accounting | Perpetual inventory / provisional accounting on PR (`stock_controller.make_gl_entries`) |
| Tests | `stock/doctype/purchase_receipt/test_purchase_receipt.py` |
| KIYA | PO → Goods Receipt. Partial. OQ-007/009 |

### WF-07 Purchase Receipt → Purchase Invoice → Payment

| Aspect | ERPNext behavior |
| --- | --- |
| Trigger | `purchase_receipt/mapper.py` `make_purchase_invoice`; PO can also `make_purchase_invoice` |
| Accounting | PI `on_submit` GL; Payment Entry against supplier outstanding |
| Tax | Purchase taxes templates; regional UAE hooks on PI validate (`hooks.py`) |
| Returns | `is_return` PR/PI via `sales_and_purchase_return.py` |
| Tests | `accounts/doctype/purchase_invoice/test_purchase_invoice.py` |
| KIYA | GR → Supplier Invoice → Tax → Payment. Partial. OQ-005 |

### WF-08 Sales demand → Production Plan → Work Order

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | Production Plan Sales Order child (`production_plan.py` `validate_sales_orders` uses `sales_order_query`) |
| Trigger | User creates Production Plan; `make_work_order` / `work_order_planning.py` |
| Also | `manufacturing/report/material_requirements_planning_report/` can `make_work_orders` / `make_purchase_orders`; Master Production Schedule; Sales Forecast DocTypes exist |
| Status | Production Plan and Work Order have their own status fields (not all in `status_map`) |
| Inventory | Planned qty on Bin; optional SRE from production plan reservation service |
| ERPNext-SPECIFIC | Production Plan is a planning document, not a full APS; capacity via Workstation hours is limited vs KIYA FR-MRP-003 |
| Tests | `manufacturing/doctype/production_plan/test_production_plan.py` |
| KIYA | MRP / Planning. Partial. OQ-008 |

### WF-09 BOM → Work Order → transfer/consumption → Job Card → FG

| Aspect | ERPNext behavior |
| --- | --- |
| Starting | BOM (`manufacturing/doctype/bom/`) with BOM Item, BOM Operation |
| Documents | Work Order; Stock Entry (Material Transfer for Manufacture / Manufacture); Job Card (+ time logs, items) |
| Inventory | Consume RM and receive FG via Stock Entry SLE; WO qty produced/consumed |
| Accounting | Manufacturing stock valuation GL if perpetual |
| Cancellation | Cancel SE then WO; reverse SLE |
| Tests | work_order and job_card tests; stock entry manufacturing tests |
| KIYA | Production / shop floor. Partial. FR-MFG-005 detail TBD |

### WF-10 Manufacturing → Quality Inspection

| Aspect | ERPNext behavior |
| --- | --- |
| QI `reference_type` includes Stock Entry, Job Card (`quality_inspection.py` types) |
| Inspection type In Process when reference is Job Card |
| Template from Item `quality_inspection_template` |
| Status Accepted / Rejected / Cancelled; `on_discard` sets Cancelled |
| Stock controller can require/create QI for incoming/outgoing purposes (`QI_INCOMING_PURPOSES`, `QI_OUTGOING_PURPOSES`) |
| Tests | quality_inspection tests under stock |
| KIYA | Quality Check in C2C. Partial. OQ-009 |

### WF-11 Quality rejection / non-conformance

| Aspect | ERPNext behavior |
| --- | --- |
| QI Rejected is a status on Quality Inspection |
| Non Conformance is a **separate Quality Management DocType** with Open/Resolved/Cancelled and free-text CAPA fields — not a stock-gate state machine |
| Quality Action / Quality Review exist; daily `quality_review.review` (`hooks.py`) |
| **No source-derived automatic QI-Rejected → Non Conformance mapper was found in the QI module header** — TBD if a client script elsewhere links them |
| KIYA | FR-QLTY-006 NCR/CAPA. Analogous at best. OQ-009 |

### WF-12 Item → Warehouse → Bin → Stock Ledger

| Aspect | ERPNext behavior |
| --- | --- |
| Item master `stock/doctype/item/item.json` |
| Warehouse `stock/doctype/warehouse/` |
| Bin: qty cache per item+warehouse (`bin.py` `recalculate_values` from last SLE) |
| SLE: immutable-style ledger rows created on submit of stock vouchers |
| Valuation methods including Standard Cost special-case in Bin |
| Reports | Stock Balance, Stock Ledger reports under stock |
| Tests | bin/stock ledger tests; `controllers/tests/test_stock_controller.py` |
| ERPNext-SPECIFIC vs KIYA FR-WH-002 | **Bin ≠ bin location.** Warehouse hierarchy is ERPNext warehouses, not KIYA WMS bins |
| KIYA | Inventory/Warehouse. Partial. OQ-007 |

### WF-13 Stock Reservation

| Aspect | ERPNext behavior |
| --- | --- |
| DocType Stock Reservation Entry; statuses Draft path via docstatus; Reserved / Partially Reserved / Partially Delivered / Delivered / Closed / Cancelled (`update_status`) |
| Created from SO, Production Plan, Work Order reservation services |
| Updates Bin `reserved_stock` / reserved qty fields |
| Tests | `test_stock_reservation_entry.py` (large suite including delivery consumption) |
| KIYA | Reservation rules TBD OQ-007. Useful ERPNext-REFERENCE for a reservation document pattern; do not copy qty math as KIYA rule |

### WF-14 Serial / Batch traceability

| Aspect | ERPNext behavior |
| --- | --- |
| Serial No, Batch, Serial and Batch Bundle; `stock_controller.make_bundle_using_old_serial_batch_fields` |
| Delivery/PR/SE require bundles when item is serialized/batched |
| Returns create bundles (`sales_and_purchase_return.py`) |
| Serial maintenance status scheduler `serial_no.update_maintenance_status` |
| KIYA | FR-INV-003. Partial/strong reference for traceability mechanics |

### WF-15 Asset lifecycle

| Aspect | ERPNext behavior |
| --- | --- |
| Asset created from item/PR (`buying_controller.make_asset`) |
| `asset.py` `get_status` / `set_status`; cancel blocked if already In Maintenance/Out of Order or not in depreciable submitted states |
| Daily `post_depreciation_entries`, `make_post_gl_entry`, `update_maintenance_status` |
| Sale via asset mapper `make_sales_invoice` |
| Tests | `assets/doctype/asset` tests |
| KIYA | Asset master/lifecycle/depreciation. Partial. Installation/warranty rules OQ-011 |

### WF-16 Asset maintenance / repair

| Aspect | ERPNext behavior |
| --- | --- |
| Asset Repair with optional Purchase Invoice child (`asset_repair.py` `validate_purchase_invoices`); tests in `test_asset_repair.py` |
| Asset Maintenance Log status updater daily |
| Maintenance Schedule / Maintenance Visit in **maintenance** module (customer equipment service visits, often from Warranty Claim) |
| Manufacturing **Work Order** is not this maintenance work order |
| KIYA | FR-MFS-001–005. Analogous naming collision on “Work Order”. OQ-011 |

### WF-17 Support Issue / Warranty

| Aspect | ERPNext behavior |
| --- | --- |
| Issue: SLA `service_level_agreement.apply` on all DocType validate (`hooks.py`); `test_issue.py` covers Open/Replied/Closed and agreement_status |
| Warranty Claim: customer complaint against serial/item; cancel blocked if Maintenance Visit exists (`warranty_claim.py` `on_cancel`) |
| Auto-close tickets daily |
| ERPNext-SPECIFIC | Issue is helpdesk-like; not proven equivalent to KIYA Case/Ticket/Field Service |
| DEC-010 | Do not map this to Asset-to-Service as Customer Service |
| KIYA | Customer Service module analogous; warranty named in Asset-to-Service as well — dual use TBD. OQ-011 |

### WF-18 Project → Task → Timesheet → accounting

| Aspect | ERPNext behavior |
| --- | --- |
| Task overdue daily; project billing reminder/status (`hooks.py`) |
| Timesheet `make_sales_invoice` requires remaining billable hours; appends SI `timesheets` child |
| Cost center/project on accounting documents (ERPNext dimension pattern) |
| Tests | projects/timesheet tests |
| KIYA | FR-PROJ-005/006; DEP-008. Partial. OQ-001 |

### WF-19 Supplier scorecard

| Aspect | ERPNext behavior |
| --- | --- |
| Supplier Scorecard + Variables/Criteria/Standings/Period |
| Daily `refresh_scorecards` |
| Tests | `buying/doctype/supplier_scorecard_variable/test_supplier_scorecard_variable.py` |
| Variables are ERPNext-defined formulas (source-derived in variable module) — **not** KIYA scorecard measures |
| KIYA | FR-SUPM-003/005. Analogous. OQ-010 |

### WF-20 Tax / accounting interaction

| Aspect | ERPNext behavior |
| --- | --- |
| Item and template taxes via `taxes_and_totals.py` on selling/buying controllers |
| GL tax accounts on SI/PI submit |
| Regional: Italy e-invoice XML utils on SI submit/cancel; UAE VAT on PI; US IRS 1099 report |
| India GST **removed** from this app (`remove_india_localisation.py`) |
| KIYA | FR-TAX-001–007. Partial for generic tax tables; India statutory **Absent-in-repo**. OQ-005 |

### WF-21 Cancellation and reversal

| Aspect | ERPNext behavior |
| --- | --- |
| Submitted docs: `docstatus=2`; reverse GL (`make_reverse_gl_entries`) and reverse SLE |
| Returns are separate documents (`is_return`) not the same as cancel |
| Cannot cancel Asset in some statuses; Warranty Claim cannot cancel with open visits |
| Period closing / accounting period validate on save (`hooks.py`) |
| Transaction Deletion Record for bulk delete of **draft/cancelled** data (setup), not business reverse |
| Tests | cancel cases throughout SI/PR/DN/SO tests |
| KIYA | FR-PADM common cancel — rules TBD OQ-002/003 |

### WF-22 Document status / lifecycle

| Aspect | ERPNext behavior |
| --- | --- |
| Dual model: Frappe docstatus + ERPNext `status` string |
| Closed/On Hold/Stopped are explicit status writes, not always docstatus |
| Daily expiry: quotation/supplier quotation `set_expired_status`; contracts; issues |
| KIYA | Must not assume this dual model (ERPNext-SPECIFIC). OQ-002 |

### WF-23 Cross-document references and mapping

| Aspect | ERPNext behavior |
| --- | --- |
| `get_mapped_doc` field_map + child postprocess remaining qty |
| Typical link fields: `prevdoc_docname`, `so_detail`, `dn_detail`, `po_detail`, `pr_detail`, `against_sales_order`, `return_against` |
| `get_qty_already_mapped` prevents double-map from unsaved target |
| Tests | `controllers/tests/test_mapper.py` |
| KIYA | Useful ERPNext-REFERENCE for traceable source/target qty; KIYA link semantics TBD |

---

## Scheduler / jobs that encode business behavior

From `erpnext/hooks.py` `scheduler_events` (source-derived): BOM cost resume; stock repost; project reminders; appointment expiry; Plaid; issue auto-close; opportunity auto-close; invoice status; fiscal year; task overdue; serial maintenance; **supplier scorecard refresh**; company monthly sales cache; asset maintenance/depreciation GL; quotation expiry; quality review; SLA check; email campaign; reorder; subscription process; deferred accounting monthly.

These jobs are ERPNext product operations, not KIYA NFR proof (SF-015 remains TBD).

## What this document does not do

- It does not approve Frappe/ERPNext for KIYA.
- It does not invent KIYA statuses, tax, payroll, or approval matrices.
- It does not claim HR/Payroll, India GST, native mobile offline, AI, or EPM exist in this repository.
