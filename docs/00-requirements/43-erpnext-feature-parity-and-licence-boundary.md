# ERPNext Feature Parity and the Licence Boundary

## Document control

- **Document ID:** `43-erpnext-feature-parity-and-licence-boundary`
- **Date:** 29 September 2026
- **Method:** Metadata inventory taken from a running ERPNext v15 instance
  (`frappe_docker`, `localhost:8080`). Doctype names, modules and flags only.
  No ERPNext source was read, copied or transcribed for this document.
- **Status:** Assessment. Raises `OQ-022`. Takes no build decision.

## 1. The licence position

| | Licence | Consequence |
| --- | --- | --- |
| Frappe Framework | **MIT** | Permissive. KNIT 360 builds on it freely, including commercially, closed-source. |
| ERPNext | **GPL-3.0** | Copyleft. A work derived from it must be GPL-3.0 when distributed. |
| HRMS, Webshop, Insights | **GPL-3.0** | Same. These are where BRD modules 19, 20 and 22 would otherwise come from. |

Two distinctions decide everything here.

**Code versus function.** Copyright protects the expression — the actual source
ERPNext's authors wrote. It does not protect what the software *does*. An
independently written Sales Invoice that behaves like ERPNext's is not a
derivative of it; a copy or a line-by-line translation of
`erpnext/accounts/doctype/sales_invoice/sales_invoice.py` is. Every feature in
the inventory below is therefore reachable — by building it, not by taking it.

**Distribution versus hosting.** GPL-3.0 obligations attach when software is
*conveyed*. Running ERPNext on your own servers and letting customers use it over
a network is not conveying, which is the gap AGPL-3.0 closes and GPL-3.0 does
not. ERPNext is GPL-3.0, not AGPL-3.0. This does not make it safe to build on:
the moment KNIT 360 imports, links to or ships alongside ERPNext, the combined
work is arguably a derivative, and any distribution of it — an on-premise
install, a customer-hosted deployment, a container image handed to a client —
carries GPL-3.0 with it.

Not a lawyer's opinion. Before a commercial launch this belongs in front of one;
`Gate L-01` in `docs/02-architecture/08-phase-1-validation-and-poc-register.md`
already exists for that.

### What the architecture already does about it

The boundary is not a policy to remember, it is enforced:

- `knit360_core` installs on a site where **Frappe is the only app**. The dev
  stack in `infrastructure/docker-compose.dev.yml` exists to prove that.
- No module imports `erpnext` or `hrms`. The single textual match in the
  repository is the sentence in `hooks.py` forbidding it.
- `knit360_core/platform/test_platform_doctypes.py::test_link_targets_are_bare_frappe_safe`
  fails the build if any Link field points at a doctype ERPNext or HRMS owns.

### The working rule for using the running instance

Use `localhost:8080` as a **behavioural reference**: what fields a document
carries, what states it moves through, what a report totals. Write that down as a
KNIT 360 requirement, then implement it. Do not open ERPNext's source and
transcribe from it — that is the one activity that converts a legal build into a
derivative work.

Note for the record: `docs/00-requirements/21-erpnext-workflow-reverse-engineering.md`
and `37-erpnext-source-component-reuse-inventory.md` were written from reading
ERPNext source. As analysis they are facts about a program and unremarkable. The
risk line is downstream — code written by transcribing from them would carry the
same problem as copying the original.

## 2. The inventory

ERPNext v15 as installed exposes **529 doctypes in 21 modules**, of which **248**
are masters or transactions (the rest are child tables and settings singletons).

KNIT 360 has **61 doctypes, 43 of them masters or transactions**.

| | Count |
| --- | ---: |
| ERPNext masters and transactions | 248 |
| Already covered by KNIT 360 | 35 |
| **Missing, and the BRD asks for it** | **171** |
| Missing, and the BRD never asks for it | 42 |

The last row matters. "Every ERPNext feature" is not the same as "every feature
KNIT 360 needs", and 42 of them are scope the BRD never requested:

> POS (5 doctypes), Loyalty Program, Coupon Code, Promotional Scheme, Share
> Transfer / Share Type / Shareholder, Subscription and Subscription Plan,
> Invoice Discounting, Bank Guarantee, Dunning, Cashier Closing, Telephony (4),
> Driver, Vehicle, Sales Partner, Campaign / Email Campaign / Competitor /
> Market Segment / Prospect, Appointment, EDI Code List, South Africa and UAE VAT.

Building those would widen scope without a requirement behind it, which
`AGENTS.md` forbids doing silently. They are listed here so the choice is
explicit rather than accidental.

## 3. The gap, by BRD module

### 17 Finance & Accounting — 58 missing

`Account`, `Account Category`, `Account Closing Balance`, `Accounting Dimension`, `Accounting Dimension Filter`, `Accounting Period`, `Advance Payment Ledger Entry`, `Bank`, `Bank Account`, `Bank Account Balance`, `Bank Account Subtype`, `Bank Account Type`, `Bank Statement Import`, `Bank Statement Import Log`, `Bank Transaction`, `Bank Transaction Rule`, `Bisect Nodes`, `Budget`, `Cheque Print Template`, `Cost Center`, `Cost Center Allocation`, `Exchange Rate Revaluation`, `Finance Book`, `Financial Report Template`, `Fiscal Year`, `GL Entry`, `Item Tax Template`, `Journal Entry`, `Journal Entry Template`, `Ledger Health`, `Ledger Merge`, `Mode of Payment`, `Monthly Distribution`, `Party Link`, `Payment Gateway Account`, `Payment Ledger Entry`, `Payment Order`, `Payment Request`, `Payment Term`, `Payment Terms Template`, `Period Closing Voucher`, `Pricing Rule`, `Process Deferred Accounting`, `Process Payment Reconciliation`, `Process Payment Reconciliation Log`, `Process Period Closing Voucher`, `Process Statement Of Accounts`, `Purchase Taxes and Charges Template`, `Repost Accounting Ledger`, `Repost Payment Ledger`, `Sales Invoice`, `Sales Taxes and Charges Template`, `Shipping Rule`, `Tax Category`, `Tax Rule`, `Tax Withholding Category`, `Tax Withholding Group`, `Unreconcile Payment`

### 08 Inventory / 09 Warehouse — 30 missing

`Batch`, `Customs Tariff Number`, `Delivery Trip`, `Inventory Dimension`, `Item Alternative`, `Item Attribute`, `Item Lead Time`, `Item Manufacturer`, `Item Price`, `Landed Cost Voucher`, `Manufacturer`, `Packing Slip`, `Pick List`, `Price List`, `Putaway Rule`, `Quality Inspection Parameter`, `Quality Inspection Parameter Group`, `Repost Item Valuation`, `Serial No`, `Serial and Batch Bundle`, `Shipment`, `Shipment Parcel Template`, `Stock Closing Balance`, `Stock Closing Entry`, `Stock Entry`, `Stock Entry Type`, `Stock Ledger Entry`, `Stock Reconciliation`, `UOM Category`, `Warehouse Type`

### 01 Platform & Administration — 20 missing

`Authorization Rule`, `Brand`, `Currency Exchange`, `Customer Group`, `Designation`, `Email Digest`, `Employee`, `Employee Group`, `Holiday List`, `Incoterm`, `Item Group`, `Party Type`, `Quotation Lost Reason`, `Sales Person`, `Supplier Group`, `Terms and Conditions`, `Territory`, `Transaction Deletion Record`, `UOM`, `UOM Conversion Factor`

### 10 Manufacturing / 11 MRP — 16 missing

`BOM Creator`, `BOM Update Log`, `Blanket Order`, `Downtime Entry`, `Master Production Schedule`, `Operation`, `Plant Floor`, `Routing`, `Sales Forecast`, `Workstation`, `Workstation Operating Component`, `Workstation Type`, `Subcontracting BOM`, `Subcontracting Inward Order`, `Subcontracting Order`, `Subcontracting Receipt`

### 13 Asset Management — 12 missing

`Asset Activity`, `Asset Capitalization`, `Asset Category`, `Asset Depreciation Schedule`, `Asset Maintenance`, `Asset Maintenance Log`, `Asset Maintenance Team`, `Asset Movement`, `Asset Repair`, `Asset Shift Allocation`, `Asset Shift Factor`, `Asset Value Adjustment`

### 16 Projects — 9 missing

`Activity Cost`, `Activity Type`, `Project`, `Project Template`, `Project Type`, `Project Update`, `Task`, `Task Type`, `Timesheet`

### 12 Quality — 7 missing

`Quality Action`, `Quality Feedback`, `Quality Feedback Template`, `Quality Goal`, `Quality Meeting`, `Quality Procedure`, `Quality Review`

### 03 Sales — 5 missing

`Delivery Schedule Item`, `Industry Type`, `Installation Note`, `Party Specific Item`, `Product Bundle`

### 02 CRM — 4 missing

`Contract Template`, `Opportunity Lost Reason`, `Opportunity Type`, `Sales Stage`

### 05 Customer Service — 4 missing

`Issue Priority`, `Issue Type`, `Service Level Agreement`, `Warranty Claim`

### 06 Procurement / 07 Supplier Management — 4 missing

`Supplier Scorecard Criteria`, `Supplier Scorecard Period`, `Supplier Scorecard Standing`, `Supplier Scorecard Variable`

### 18 Tax & Statutory Compliance — 2 missing

`Import Supplier Invoice`, `Lower Deduction Certificate`

## 4. BRD modules ERPNext cannot supply at all

Parity with ERPNext still leaves these unbuilt, because ERPNext does not contain
them. Where a Frappe app exists it is also GPL-3.0, so it is a reference at best,
never a dependency.

| BRD module | In ERPNext? |
| --- | --- |
| 04 Marketing | Campaign / Email Campaign only, and both are outside the BRD's stated scope |
| 15 Logistics & Transportation | `Shipment` and `Delivery Trip` only; no TMS, carrier rating or route optimisation |
| 19 HR & Payroll | No — separate **HRMS** app, GPL-3.0 |
| 20 E-Commerce | No — separate **Webshop** app, GPL-3.0 |
| 21 Document Management | No |
| 22 Business Intelligence | No — separate **Insights** app, GPL-3.0 |
| 23 EPM / Budget / Forecast | `Budget` only |
| 24 Workflow & Approvals | Frappe core (MIT) — and `CD-006` already rejects it in favour of the business-status adapter |
| 25 AI & Automation | No |
| 26 Integration & API | Frappe core (MIT) |
| 27 Mobile Application | No |
| 28 Audit, Security & Compliance | Frappe core (MIT), partially |

## 5. `OQ-022` — What parity target does KNIT 360 commit to? (OPEN)

"Every ERPNext feature" is 213 doctypes, of which 42 have no requirement behind
them. Three targets are distinguishable and the choice has not been made:

| Target | Scope | Note |
| --- | --- | --- |
| **A — BRD parity** | The 171 that a BRD module asks for | Delivers the product the BRD describes. Does not match ERPNext feature-for-feature. |
| **B — Demonstrable parity** | The subset a buyer would actually compare | Smaller than A, needs a named comparison list. |
| **C — Full parity** | All 213 | Includes POS, loyalty, share registry, telephony. Widens scope past the BRD. |

Recommended sequencing under any of them, because the dependency order is not
negotiable:

1. **Finance & Accounting core** — `Account`, `Fiscal Year`, `Cost Center`,
   `GL Entry`, `Journal Entry`, `Sales Invoice`, `Purchase Invoice`, `Payment
   Entry`. Everything downstream posts here, and `CD-002`'s docstatus adapter
   already assumes a ledger exists to post to.
2. **Stock ledger** — `Stock Ledger Entry`, `Stock Entry`, `Batch`, `Serial No`,
   `Stock Reconciliation`. `KNIT 360 Delivery Note` currently has no real stock
   effect behind it.
3. **Masters** — `UOM`, `Item Group`, `Price List`, `Item Price`, `Territory`,
   `Customer Group`, `Supplier Group`. These unblock `FR-SALES-004` pricing,
   which is presently TBD and why quotation lines are priced by hand.
4. Then the module-by-module remainder.

Nothing in this document authorises a build. It sizes one.
