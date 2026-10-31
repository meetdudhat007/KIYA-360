# KNIT 360 — User Guide for a Furnace Manufacturing and Repair Business

## Document control

- **Document ID:** `03-guides/09-furnace-business-user-guide`
- **Date:** 28 October 2026
- **For:** a business that makes induction furnaces, sells them in India, and then services and repairs them.
- **Status:** Operating guide for the current build. Every behaviour described is driven by an automated check on the running site `knit360.localhost` (230 checks: 49 structural, 181 runtime, all passing on 28 October 2026). The order-to-invoice and after-sale screens — order, delivery with serial number, invoice, commissioning, warranty, service request, repair job, sign-off, service invoice and furnace history — were also walked through in the browser that day.
- **Example values** are the BRD's own (company *Kelvinotherm Induction LLP*, branch Ahmedabad, item *IF-1500*, HSN *8514*). Use your own.

---

## 1. What the client asked for, and what the system does today

| You want to… | In KNIT 360 today | Not built yet |
| --- | --- | --- |
| Keep every customer and prospect in one place | Leads, Opportunities, Customers, Contacts | — |
| Send a quotation | Quotation with price list, discount and GST template; printable | — |
| Email customers from the system | **New Email** button on every document, once your outgoing mail account is set up (§3.9) | Nothing is emailed automatically on a status change; incoming mail is not read into the CRM |
| Turn the quotation into an order without retyping | **Create Sales Order** on an accepted quotation | — |
| Control stock | Stock per warehouse, valued FIFO, moved only by documents | Batch numbers; barcode scanning |
| Control manufacturing | BOM per furnace model; a Work Order that uses the materials and brings the finished furnaces into stock | Labour and overhead in the furnace's cost; job cards; automatic quality inspection after production |
| Deliver | **Create Delivery Note** from the order, with each furnace's serial number | E-way bill |
| Invoice and get paid | **Create Sales Invoice** from the delivery; part payments; credit notes | E-invoice (IRN) |
| Track every furnace after the sale | Installed-furnace register, warranty and AMC, service requests, engineer visits, repair jobs with spare parts, service invoices, planned maintenance, full furnace history | Mobile app for engineers; SLA timers; customer portal; reminders; return of faulty parts |

---

## 2. What after-sale service tracking covers

This is the after-sales journey your requirements define (BRD §6.3, detailed in requirement document 33), stage by stage, with where each lives in KNIT 360.

| # | Stage | What it means for a furnace business | In KNIT 360 | Built? |
| --- | --- | --- | --- | --- |
| 1 | Installed base | Every furnace you have sold, by serial number, customer and site | **Asset** — created automatically when the furnace is dispatched | Yes |
| 2 | Installation & commissioning | Installing at the customer's plant and handing it over | **Field Work Order** of type *Installation*; the Asset's **Commissioning Date** and **Commissioned / Operational** button | Yes |
| 3 | Warranty & contracts | What is free to the customer, until when: the maker's warranty, an extended warranty, an AMC or a CMC | **Service Contract** — drafted automatically on commissioning | Yes |
| 4 | Service request | The customer calls: "the furnace trips on overload" | **Service Request** — shows at once whether the furnace is covered | Yes |
| 5 | Engineer assignment | Who goes, and when | **Service Dispatch** | Yes (no route planning, no mobile app) |
| 6 | Spare parts | Which parts were used, from which store or van | Parts lines on the **Field Work Order**; stock falls when the job is complete | Yes (no return of faulty parts) |
| 7 | Repair job | Hours, findings, parts, customer's sign-off | **Field Work Order** | Yes |
| 8 | Planned maintenance | AMC visits every so many days | **Maintenance Schedule** — the next due date moves on by itself | Yes (calendar only; not running hours) |
| 9 | Service invoice | Bill what no warranty or contract covers | **Raise Service Invoice** on the job | Yes |
| 10 | Payment | Customer pays the service bill | **Payment Entry** — the same as for any invoice | Yes |
| 11 | Furnace history | Everything that ever happened to one furnace | **Service History** section on the Asset | Yes (no failure-rate measures) |

---

## 3. One-time setup

Do these once, in this order. Your finance person should check 3.1, 3.5 and 3.6.

### 3.1 Company and financial year
1. **Platform → Company → New.** Enter the company name, currency `INR`, and your GSTIN in **Tax Registration Number**. Saving builds your chart of accounts automatically, including two accounts this guide uses: **Service Revenue** (labour and travel you charge on repairs) and **Warranty Expense** (parts you give free under warranty).
2. **Finance → Fiscal Year → New**, covering the dates you will post in. Nothing can be posted on a date outside a fiscal year.

### 3.2 Warehouses
**Warehouse → Warehouse → New**, one for each place stock sits. The flows below ask for:

| The system asks for | Meaning |
| --- | --- |
| **Raw Materials From** (production) | Where the materials for a furnace are taken from |
| **Finished Goods To** (production) | Where finished furnaces go |
| **Ship From Warehouse** (delivery) | Where a furnace leaves from |
| **Spare Parts From** (repairs) | Where an engineer's parts come from — a store, or a van if you set one up as a warehouse |

### 3.3 Items
**Inventory → Item → New.** You need four kinds:

| Kind | Example | Tick / fill |
| --- | --- | --- |
| Furnace models you sell | `IF-1500`, HSN `8514` | **Serial Tracked**; **Standard Warranty (Months)** — your warranty length; **HSN / SAC Code** |
| Materials and bought-out parts that go into a furnace | coils, panels | **HSN / SAC Code** |
| Spare parts used on repairs | thyristors, insulation | **HSN / SAC Code** |
| Service charges | "Labour per hour", "Site visit" | **HSN / SAC Code** (a SAC for services). The price you give it is what you charge |

Then **Inventory → Price List** (a *Selling* list) and **Item Price** for every item you sell or charge for: furnaces, chargeable spare parts, labour, site visit. Either tick **Is Default** on the selling list, or put it in each customer's **Default Price List**.

### 3.4 Recipes (BOM)
**Manufacturing → BOM → New** for each furnace model: **Produced Item**, **Quantity** (how many one recipe makes, usually 1), the **Components** with their quantities, and tick **Is Active**. A work order refuses a BOM that is not active.

### 3.5 GST
**Tax → Tax Template → New**: one row per component (for example CGST and SGST, or IGST), each with its **Rate** and the account it **Posts To**. Your finance person should set these up.

### 3.6 Customers
**CRM → Customer → New**: name, contact details, address. Optional: **Credit Limit** (orders and invoices beyond it are refused) and **On Credit Hold**.

### 3.7 Engineers
Each service engineer needs a user login (the administrator creates it under **User**), because jobs and visits are assigned to users.

### 3.8 Existing furnaces
Furnaces sold before KNIT 360 can be entered by hand: **Asset Management → Asset → New** with the model, serial number, customer, site address and commissioning date.

### 3.9 Email (the owner's task)
The **New Email** button at the bottom of every document sends the document by email, but only after an outgoing mail account has been set up: in **Email Account** enter your mail server details and its password. Only you can enter that password. Until then, nothing can be emailed.

---

## 4. Selling a furnace

1. **Lead.** **CRM → Lead → New**: **Prospect Name**, **Organization Name**, phone, email, **Estimated Requirement** (for example "1 × 1500 kg induction furnace"). Move it with the buttons at the top: **Contacted**, then **Qualified**.
2. **Convert.** On a Qualified lead press **Convert to Customer + Opportunity**. The customer and the opportunity are created for you.
3. **Quotation.** On the opportunity press **Raise Quotation**. Add the lines: item, quantity, rate (filled from your price list if you leave it empty), discount. Choose the GST template. Then **Pending Approval** → **Issued / Sent**. Print it, or email it with **New Email**.
4. **Customer accepts.** Press **Accepted**.
5. **Order.** Press **Create Sales Order**. The order is made with the quotation's lines at the agreed price, discount included. Check it, then press **Confirmed / Booked**. If the customer is over their credit limit or on hold, this is refused.
6. Go back to the quotation and press **Ordered**. (Creating the order does not change the quotation by itself.)

The sales pages at `/knit360` show leads, opportunities and quotations as a board, if you prefer that to the lists. To get back to the main screen, press **KNIT 360 Home** at the top right (on a phone it just says **Home**).

---

## 5. Making the furnace

1. **Manufacturing → Work Order → New.** **Target Item** (the furnace model), **BOM**, **Quantity to Produce**, **Against Sales Order** (optional), **Raw Materials From**, **Finished Goods To**, **Production Date**.
2. **Save.** The **Materials** table fills itself from the BOM: exactly what this order will use.
3. Press **In Process** when work starts. **Stopped** pauses it; **In Process** resumes it.
4. Press **Completed** when the furnaces are made. At that moment:
   - every material leaves **Raw Materials From**, costed by what you paid for it (oldest stock first);
   - the furnaces arrive in **Finished Goods To**, each costed at the materials' total divided by the quantity made;
   - **Material Cost** and **Cost per Unit Produced** show those figures.
5. If any material is short, **Completed** is refused and nothing moves. Receive the material (Goods Receipt) and try again.

**Cancelled** after completion puts the materials back and takes the furnaces out, but is refused once any of those furnaces has been dispatched.

Today the furnace's cost is its materials only. Labour and factory overhead are not added to it (decision `DEC-040`).

---

## 6. Delivering, invoicing and getting paid

### 6.1 Delivery
1. On the confirmed sales order press **Create Delivery Note** and choose the **Ship From Warehouse**. The delivery note is made for whatever the order still has to send.
2. Open the item line (the small edit icon at the end of the row) and type the furnace's serial number in **Serial Numbers**: one per line, as many as the quantity.
3. Fill carrier, vehicle and driver if you wish, save, and press **Dispatched / In Transit**. At that moment:
   - the furnace leaves stock and its cost is charged to Cost of Goods Sold;
   - **each furnace is registered as an Asset** for this customer, with its serial number, ready for warranty and service.
4. Press **Delivered** when it arrives.

The system refuses: sending more than the order still has outstanding; a serial-tracked furnace without its serial numbers; a serial number already delivered before.

### 6.2 Invoice
1. On the dispatched delivery note press **Create Sales Invoice**. The invoice is made with the delivered quantities at the order's prices.
2. Check the GST template, then **Pending Approval** → **Posted / Unpaid**. Posting is when the customer owes you. Print or email it.

### 6.3 Payment
**Finance → Payment Entry → New**: **Direction** = Receive, **Party Type** = KNIT 360 Customer, **Party** = the customer, **Amount**, **Bank Account**, and in **Allocations** the invoice it pays. Press **Pending Bank Authorization**, then **Disbursed / Cleared** when the money is in the bank. The invoice moves to **Partly Paid** or **Paid** by itself. Money paid beyond the invoice is held as an advance for the customer.

Finally move the sales order to **Delivered** and **Closed**.

---

## 7. Installation, commissioning and warranty

1. Open the furnace: **Asset Management → Asset** (or from the delivery note). Fill the **Installation Site Address** and **Site Contact Person**.
2. If you track the installation as a job, create a **Field Work Order** with **Work Type** = *Installation* for this asset (see §8.3 for how a job works).
3. Enter the **Commissioning Date** (it may not be before the dispatch date), save, and press **Commissioned / Operational**.
4. The system drafts the maker's warranty for the item's **Standard Warranty (Months)**, starting on the commissioning date, and tells you so. Open it (the **Connections** area of the Asset lists it), tick what it covers — **Parts Covered**, **Labour Covered**, **Travel Covered** — note any **Exclusions**, and press **Active / In Coverage**. **Until you do, it covers nothing.**

**AMC, CMC or extended warranty:** **Maintenance → Service Contract → New**, choose the asset and the **Contract Type**, the start and end dates, tick what it covers, and press **Active / In Coverage**.

A contract whose end date has passed is moved to **Expired** by a nightly job. Cover never depends on that job — it is always judged from the contract's dates — but the job only runs where the site's scheduler process runs. The current local setup starts the web server only, so there the administrator runs it by hand: `bench --site knit360.localhost execute knit360_core.maintenance.entitlement.expire_contracts`.

---

## 8. When a customer calls with a problem

### 8.1 Log the request
On the furnace (Asset) press **Log Service Request** and type what the customer says is wrong. The request opens with the customer filled in and, worked out by the system, the **Warranty / Contract Cover** on the day they called, for example *"Standard Warranty to 27-10-2027: parts"*, or *"Not covered"*.

A request against a furnace that belongs to a different customer, or one that is decommissioned or scrapped, is refused.

Press **Triaged** once you have understood the problem.

### 8.2 Send an engineer
On the request press **Schedule Visit**. Choose the **Assigned Technician** and **Scheduled Appointment**, then move it **Assigned** → **Dispatched / En Route** → **On Site** → **Work Started** as the visit happens. **Reassigned** and **Rescheduled** are there when plans change. On the request, press **Dispatched / Scheduled**.

### 8.3 Do the job
On the request press **Create Work Order**. On the Field Work Order:

1. **Parts and Charges** — one line for each thing used or charged:
   - **Spare Part** — a part taken from stock;
   - **Labour** — your labour item, quantity = hours;
   - **Travel** — your site-visit item.
2. **Spare Parts From** — the store or van the parts came from.
3. **Save.** The **Cover** column fills itself on every line: *Warranty Covered*, *Contract Covered* or *Billable to Customer*. It is judged on the day the customer reported the fault.
4. **In Progress** when the engineer starts. **Pending Parts / On Hold** if waiting for a part.
5. Enter **Actual Labour Hours**, **Travel Hours** and **Findings / Action Notes**.
6. Press **Work Complete**. The spare parts leave stock. Their cost goes to **Warranty Expense** if the warranty covered them, otherwise to Cost of Goods Sold. **Parts Cost** shows the total.
7. Enter **Customer Signature** (who signed for the work, e.g. "R. Shah, plant manager") and press **Customer Signed Off**.

The system refuses **Work Complete** without labour hours or with a part that is not in stock, and **Customer Signed Off** without a signatory. On the request, press **Work In Progress** and later **Resolved**.

### 8.4 Bill the job
On the completed job press **Raise Service Invoice**. A draft Sales Invoice is made with **only the Billable to Customer lines**, priced from your price list. Labour and travel are credited to **Service Revenue**. Check it, choose the GST template, and post it as in §6.2. Payment is the same as §6.3.

It is refused if every line is covered, or if a billable item has no selling price — give it a price and try again. If the job must be cancelled, cancel its invoice first.

Finally: job **Closed**, request **Closed**.

**If the warranty should not apply** — for example the damage was caused by misuse — the rules for that are your own policy and are not built. Correct the draft service invoice before posting it.

---

## 9. Planned maintenance (AMC visits)

1. **Maintenance → Maintenance Schedule → New**: the asset, the service contract, **Interval (Days)** (for example 90), **Next Visit Due**, and **Maintenance Tasks / Checklist**.
2. Filter the schedule list on **Next Visit Due** to see what is due.
3. On the schedule press **Create Visit Work Order**. The job is created as *Preventive Maintenance* with your checklist copied into its procedure. Complete it as in §8.3.
4. When the job reaches **Work Complete**, the schedule's **Last Visit** becomes that day and **Next Visit Due** moves on by the interval. Cancelling the visit puts the dates back.

---

## 10. A furnace's whole history

Open the furnace (Asset). The **Service History** section shows, newest first: delivery, commissioning and status changes, warranty and contracts, every service request with the cover at the time, visits, repair jobs with the parts used, and service invoices — each with a link. Above it: number of service requests, breakdown repairs, planned visits, labour hours, cost of parts used, how much of that was under warranty, and how much has been billed. The **Connections** area lists the same documents by type.

---

## 11. Messages you may see, and what to do

| Message (start of) | Why | What to do |
| --- | --- | --- |
| "An order is made from an accepted quotation" | The quotation is not Accepted | Press **Accepted** first |
| "Already on order as SO-…" / "Already billed on …" | It was done once already | Open the document named |
| "… can go now, not …" | Sending more than the order has left | Reduce the quantity |
| "… is tracked by serial number, so dispatching … needs … serial numbers" | Serial numbers missing | Open the line and type them, one per line |
| "… has already been delivered as AST-…" | That serial number is already registered | Check the serial number |
| "… holds … of … and this issues …" | Not enough stock in that warehouse | Receive the stock, or choose another warehouse |
| "Enter the commissioning date first" | Commissioning without a date | Fill **Commissioning Date**, save, press again |
| "… belongs to …, not …" | Request against another customer's furnace | Use the owner's name |
| "Record the hours spent on the job…" | Completing a job with no hours | Fill **Actual Labour Hours** |
| "Record who signed for the work…" | Signing off without a signatory | Fill **Customer Signature** |
| "give … a selling price…" | A billable item has no price | Add an **Item Price** |
| "This job is billed on SINV-…" | Cancelling a billed job | Cancel the invoice first |
| "… is not marked Is Active" | Using an old recipe | Tick **Is Active** on the right BOM |

---

## 12. Not built yet, and decisions only you can make

**Not built:** mobile app for engineers; automatic emails, WhatsApp or SMS on status changes; SLA response timers and escalation; customer self-service portal; return of faulty parts to stock or supplier; meter-based maintenance (running hours); route planning; labour and overhead in the furnace's cost; job cards; batch numbers; e-invoice and e-way bill; separate roles — every record type is open to one role, System Manager, so a user who can use one screen can use all of them.

**Decisions only you can make** (recorded as open questions):

| Decision | Where it is recorded |
| --- | --- |
| What your warranty covers (parts, labour, travel), for how long, and what voids it | `OQ-011` |
| Who must approve what, at what value | `OQ-003` |
| Which events send a message, to whom, by which channel | `OQ-004` |
| Your mail server and its password (§3.9) | — |

The decisions behind what this guide describes are `DEC-039` to `DEC-043` in `.kiya/AI-DECISIONS.md`.
