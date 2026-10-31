# KNIT 360 — Hosted First-User Guide

## Document control

- **Document ID:** `03-guides/08-hosted-first-user-guide`
- **Date:** 17 October 2026
- **Status:** Operational orientation for the current build. It is **not** a production-launch approval.
- **Evidence basis:** The local Frappe site `knit360.localhost`, running Frappe 15.121.1 with `knit360_core`, plus the installed application metadata and source definitions.

## Read this before inviting anyone

This guide is written as though the product has one public address:

```text
https://<your-erp-domain>
```

Replace `<your-erp-domain>` with the canonical address given to users. The verified running environment is local Frappe, not a verified Vercel production deployment. Before sharing a public address, the deployment owner must confirm that authenticated requests to both `/app` and `/knit360` reach the same configured KNIT 360 backend.

The source metadata contains 75 non-child record types. Its live traceability report identifies 15 of the 28 BRD modules as touched and records 71 of 238 requirements as modelled or proven, including 12 proven. It is therefore a working, partial ERP/CRM build—not a claim that every BRD capability is ready.

Do **not** invite external users or process live financial data until the authorization issues found in the code review have been fixed and retested. In particular, lifecycle, finance, and data-list endpoints need permission hardening. Publishing a front end through Vercel does not resolve those server-side risks.

---

## 1. Who does what first

| Person | First responsibility | Do not do yet |
| --- | --- | --- |
| Site owner / administrator | Configure the public address, create named user accounts, set roles, and own backups and recovery. | Share one administrator account with the team. |
| Finance owner | Check company defaults, fiscal year, chart of accounts, tax setup, and opening balances before posting. | Treat a draft as a posted accounting record. |
| Sales owner | Build customer and item masters, then run a small test sale. | Send a quotation or invoice before its data and approval path are checked. |
| Procurement / stores owner | Build supplier, warehouse, and item masters; test one receipt and one issue in a non-production company. | Assume untested warehouse or matching rules meet the business's policy. |
| Every user | Work from their own named account and use the offered business-status actions. | Use the framework's direct Submit/Cancel controls to bypass the business flow. |

There is no verified self-registration journey in this guide. A new person should ask the site owner for a named account and should change the temporary password on first sign-in.

---

## 2. First sign-in

1. Open `https://<your-erp-domain>/app`.
2. Sign in with the account created by the site owner.
3. Change a temporary password immediately.
4. Open the **KNIT 360** workspace from the Desk home page.
5. Use the global search when you know a record name; use the left navigation when learning the product.

There is also a focused sales workspace at:

```text
https://<your-erp-domain>/knit360
```

It is for the first three Customer-to-Cash stages—Leads, Opportunities, and Quotations. Use `/app` for setup, finance, procurement, inventory, service, and HR.

### The rule for every governed document

Use the document's **business-status action** to move it forward. The buttons shown are the legal next moves for its current state. Do not type a status and do not rely on a direct framework Submit or Cancel action. A posted document must be reversed/cancelled through its permitted business-status path; it must not be silently edited.

---

## 3. Set up a new business before live work

Complete this once for each company, in this order. Use a test company first if the team has not rehearsed the process.

1. **Platform → Company** — create the legal entity and its base currency. A new Company automatically creates its chart of accounts, root cost centre, and company-account defaults. Open the Company after saving and verify that those defaults are present.
2. **Platform → Location, Branch, Business Unit, Division, Department, Designation** — create only the organisational records the business actually uses.
3. **Platform → UOM and UOM Conversion** — define the units in which items are bought, stocked, and sold.
4. **Platform → Terms and Conditions, Incoterm** — add the commercial terms you will reference on documents.
5. **Finance → Fiscal Year** — create a fiscal year that covers the dates on the first documents you will post. Do not enter transactions outside a configured fiscal year.
6. **Finance → Account and Cost Center** — review the generated chart before anybody posts. Only leaf accounts receive postings; group accounts are headings.
7. **Tax → Tax Template** — create and review the tax components and their accounting destinations before using tax on an invoice or bill.
8. **Inventory → Item Group, Brand, Item, Price List, Item Price** — create item masters and dated prices before quotation, order, or invoice entry.
9. **CRM → Customer Group, Territory, Customer, Contact** — create the customer master data required by sales.
10. **Supplier Management → Supplier Group, Supplier** — create supplier master data required by procurement.
11. **Warehouse → Warehouse and Bin** — create the physical receiving, storage, and dispatch locations used by stock movements.

### Day-one check

Before processing real work, perform one test with a non-live customer and supplier:

- create one sellable item and one purchase price;
- create a lead, quotation, sales order, delivery note, and sales invoice;
- create a supplier, purchase order, goods receipt, supplier invoice, and payment entry;
- confirm the permitted status actions appear in the expected order; and
- have the finance owner inspect the resulting GL entries and trial balance.

If any step differs from your operating policy, stop and resolve it before live entry.

---

## 4. Daily work: the main connected flows

### 4.1 Customer-to-Cash: prospect to customer invoice

1. Create a **Lead** in CRM or on `/knit360`.
2. Use the offered actions to progress the lead (for example, contact and qualification).
3. Convert the qualified lead. The conversion creates the linked Customer and Opportunity.
4. Complete the Opportunity data and progress it through its offered actions.
5. Create a **Quotation** from the Opportunity.
6. Enter quotation lines. Enter the item, quantity, rate, and discount where applicable; calculated values such as line amount are not entered manually.
7. Move the Quotation through its offered approval/sending/acceptance actions.
8. Create the **Sales Order** and use its status actions to confirm, fulfil, deliver, close, hold, or cancel it as appropriate.
9. Create a **Delivery Note** for dispatch. Its business-status path controls the stock effect; do not alter stock by editing a historical ledger row.
10. Create a **Sales Invoice** and move it to its permitted posted state. This creates the receivable and GL effect.
11. Record and allocate a **Payment Entry** only after the finance owner confirms the payer, bank/cash account, amount, and target invoice. Its clearance/disbursement action posts the cash effect and refreshes settlement.
12. Use a **Credit Note** for a customer-side reduction/return and a **Debit Note** for a supplier-side reduction/return. Do not overwrite a posted invoice or bill to simulate a return.

### 4.2 Procure-to-Pay: supplier to payment

1. Create or approve the **Supplier**.
2. Use a **Sourcing Project** when supplier discovery/evaluation is required.
3. Raise a **Purchase Requisition** for an internal requirement.
4. Create a **Request for Quotation**, then record received **Supplier Quotations**.
5. Create and approve the **Purchase Order**.
6. At the gate/receiving point, create a **Goods Receipt**. Use its status buttons for received, inspection, acceptance, rejection, or cancellation. The selected lifecycle result determines whether stock is posted.
7. Record the **Quality Inspection** and, when required, a **Non Conformance Report**.
8. Complete the **Putaway Task** to record movement into the nominated bin/warehouse location.
9. Create the **Supplier Invoice**, reference the receipt when applicable, and use the matched/approved state only after the finance owner checks the bill.
10. Create a **Payment Entry** in the appropriate direction and progress it through bank authorization and clearance. Review the supplier invoice's resulting outstanding amount and status.
11. Periodically create a **Supplier Scorecard** only from reviewed period data; publish or archive it through its permitted actions.

### 4.3 Inventory, warehouse, planning, manufacturing, and quality

| Need | Where to work | Safe use |
| --- | --- | --- |
| Maintain product definitions | Inventory → Item, Item Group, Brand | Keep one canonical item per sellable/buyable product; do not create near-duplicate codes. |
| Maintain prices | Inventory → Price List, Item Price | Date and review prices before use; document lines retain the price used. |
| View stock evidence | Inventory → Stock Ledger Entry | Treat this as an auditable movement record, not an editable stock counter. |
| Reserve stock | Inventory → Stock Reservation | Use only after confirming the related demand document and warehouse. |
| Receive/dispatch locations | Warehouse → Warehouse, Bin | Define physical locations before receipts or dispatches. |
| Direct a putaway | Warehouse → Putaway Task | Complete the task only when the physical movement is complete. |
| Plan material | MRP → Material Plan | Use as planning input; validate purchasing/manufacturing consequences with the responsible owner. |
| Define production structure | Manufacturing → BOM | Review every component and quantity before using it in a work order. |
| Run production | Manufacturing → Work Order | Progress only through the offered status actions. |
| Inspect quality | Quality → Inspection Template, Quality Inspection, Non Conformance Report | Record the evidence and outcome; use NCR for non-conforming results. |

### 4.4 Finance, tax, and controls

| Task | Record | How to use it |
| --- | --- | --- |
| Create a controlled manual adjustment | Journal Entry | Keep it balanced; use its business-status path to post or cancel. |
| Review accounting activity | GL Entry and Trial Balance | GL Entry is evidence of postings; use Trial Balance to check total debits equal total credits. |
| Bill a customer | Sales Invoice | Post through the permitted business-status action; review outstanding amount after payments or credit notes. |
| Record supplier liability | Supplier Invoice | Match/review it before approval and payment. |
| Receive/pay money | Payment Entry | Confirm party, direction, paid/received account, allocations, and bank authorization before clearing. |
| Manage settlement terms | Payment Term, Payment Terms Template, Mode of Payment | Set these up before they are reused on live documents. |
| Return/adjust commercial value | Credit Note, Debit Note | Use the note against the correct party and original document where applicable. |
| Apply tax | Tax Template | Verify components and mapped accounts with the finance/tax owner before go-live. |

### 4.5 Assets and service work

1. Register an **Asset** and progress it through its operational status (registered, commissioned, under maintenance, decommissioned, or scrapped) using available actions.
2. Create a **Service Contract** for an agreed coverage period.
3. Log a **Service Request** when work is requested.
4. Create and perform the **Field Work Order**.
5. Use **Service Dispatch** to assign, dispatch, reassign, reschedule, and record on-site/work-start status.
6. Use **Maintenance Schedule** for planned maintenance activity.

### 4.6 HR leave administration

1. Maintain **Employee**, **Department**, **Designation**, **Holiday List**, **Leave Type**, and **Leave Period** first.
2. Create a **Leave Allocation** and move it to Allocated to establish the employee's available leave balance.
3. Create a **Leave Application** and progress it through Pending Approval to Approved, Rejected, or Cancelled as appropriate.
4. Use **Leave Ledger Entry** as the derived audit record of allocation and consumption; do not edit it as a substitute for correcting the source document.

---

## 5. Feature directory: every implemented record type

This is a navigation catalogue, not a claim that each record type completes every BRD requirement.

| Area | Available records | Primary use |
| --- | --- | --- |
| Platform | Company, Location, Branch, Business Unit, Division, Department, Designation, Employee, UOM, UOM Conversion, Incoterm, Terms and Conditions | Organisation, people, units, and commercial setup. |
| CRM | Lead, Opportunity, Customer, Contact, Customer Group, Territory | Customer master data and sales pipeline. |
| Sales | Enquiry, Quotation, Sales Order, Delivery Note | Customer request, pricing, commitment, and dispatch. |
| Finance | Account, Cost Center, Fiscal Year, Journal Entry, GL Entry, Sales Invoice, Supplier Invoice, Payment Entry, Payment Term, Payment Terms Template, Mode of Payment, Credit Note, Debit Note | Chart, accounting periods, ledgers, receivables, payables, payments, and adjustments. |
| Tax | Tax Template | Reusable tax components for documents. |
| Procurement | Purchase Requisition, Request for Quotation, Supplier Quotation, Purchase Order, Goods Receipt | Requirement through receipt. |
| Supplier Management | Supplier, Supplier Group, Supplier Scorecard, Sourcing Project | Supplier master, qualification, and performance. |
| Inventory | Item, Item Group, Brand, Price List, Item Price, Stock Reservation | Product master, pricing, and reservations. |
| Warehouse | Warehouse, Bin, Putaway Task | Physical storage structure and putaway activity. |
| MRP | Material Plan | Material planning. |
| Manufacturing | BOM, Work Order | Product structure and production work. |
| Quality | Inspection Template, Quality Inspection, Non Conformance Report | Planned checks, inspection results, and non-conformance recording. |
| Asset Management | Asset | Operational installed-base/asset record. |
| Maintenance | Service Request, Field Work Order, Service Contract, Service Dispatch, Maintenance Schedule | Service and maintenance activity. |
| HR | Holiday List, Leave Type, Leave Period, Leave Allocation, Leave Application, Leave Ledger Entry | Leave setup, approval, and ledger. |
| Business Status | Business Status Log | Read-only history of status transitions. |
| Search / Stock | Search Index, Stock Ledger Entry | Framework-backed findability and derived stock-movement evidence. |

The following BRD areas currently have no corresponding modelled functionality in the live traceability report: Marketing, Customer Service, Logistics & Transportation, Projects, E-Commerce, Document Management, Business Intelligence, EPM/Budget/Forecast, Workflow & Approvals, AI & Automation, Integration & API, Mobile Application, and Audit/Security/Compliance. Do not promise these capabilities to users as present product features.

---

## 6. A safe first-week rollout

| Day | Objective | Exit condition |
| --- | --- | --- |
| 1 | Access and masters | Every user has a named account; company, fiscal year, units, customers, suppliers, items, and warehouses exist. |
| 2 | Sales rehearsal | A non-live lead becomes a quotation, order, delivery, invoice, and payment with a finance-owner review. |
| 3 | Procurement rehearsal | A non-live requisition reaches purchase order, receipt, quality/putaway, supplier invoice, and payment. |
| 4 | Finance review | Finance owner reconciles the test GL entries and confirms the trial balance. |
| 5 | Controlled pilot | Process a small, reversible set of live documents; review exceptions at the end of the day. |

Do not migrate historical data or open every module to every user during the first week. First prove the business's actual sales, procurement, and finance scenarios in a controlled pilot.

---

## 7. When to stop and ask for help

Stop the transaction and ask the process owner or administrator when:

- a required customer, supplier, item, account, warehouse, or fiscal year does not exist;
- the next business-status action is not the action the team expects;
- a document is already posted and someone wants to change its commercial or accounting effect;
- an invoice, bill, credit note, payment, or journal entry does not reconcile as expected;
- a tax configuration or account mapping is uncertain; or
- a user needs access outside their assigned responsibility.

For a genuine software fault, capture the document name, current status, action attempted, timestamp, and the exact error message. Do not work around it by editing ledger or audit records directly.

---

## 8. Go-live gate for the deployment owner

Before calling the public URL a production ERP, record evidence for all of the following:

- a canonical production address and tested login/session path;
- user provisioning, role design, least-privilege permission tests, and removal of the current authorization findings;
- backup, restore, monitoring, error-alerting, and incident ownership;
- finance-owner approval of chart, fiscal years, tax templates, payment setup, and opening balances;
- a rehearsal of C2C and P2P with the business's own documents; and
- confirmation of the exact scope communicated to users, including the BRD areas that are not implemented.

Until those checks are complete, describe the product as a controlled pilot—not as a fully deployed ERP.
