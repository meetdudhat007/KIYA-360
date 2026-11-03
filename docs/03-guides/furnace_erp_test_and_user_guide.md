# KNIT 360 — End-to-End User and Testing Guide
## For Furnace Manufacturing & Repair Business (Indian Market)

---

### Purpose of this Guide
This document is a practical, step-by-step testing manual and user guide designed to help you test and evaluate **KNIT 360** (the ERP platform built for this project) to determine if it meets your business requirements for **Furnace Manufacturing, Sales, and After-Sales Service & Repairs**.

This guide is written in **plain, layman terms**, walking through every click, form field, button, and business rule without assuming technical background. It starts from the very first screen you see when you open the link: **Login to KNIT 360**.

> **How this guide was checked**: on 31 October 2026 every step in Section 3 was run on this system, in this order, through the same server actions the buttons use. That test run was then rolled back, so it left nothing behind. The amounts, messages and names below are what the system actually produced. No code was modified.

---

## 1. System Capability Summary: Does it Fit Your Business?

| Your Business Requirement | Built & Working in KNIT 360 Today? | How It Works in the System | What Is Not Built / Needs Setup |
| :--- | :---: | :--- | :--- |
| **Track Customers & Inquiries (CRM)** | **YES** | Track Leads, Opportunities, Customers, Territory, and Source. | Incoming email sync to CRM is not automated. |
| **Furnace Quotations with GST & Pricing** | **YES** | Quotation with the rate filled from the Price List, discount, GST tax template, and totals. | — |
| **Quotation PDF & Emailing** | **YES** | Print layout with quotation number, date, validity, lines, discount, GST breakup and amount in words. Download as PDF in one click. | The printout does not show HSN codes, the customer's address or GSTIN, or your company name (unless you add a Letter Head). Email goes out through the mail account already set up (see Section 4). |
| **Order without Retyping** | **YES** | One-click button **Create Sales Order** copies items, agreed price and GST template from the Quotation. | — |
| **Inventory & Raw Material Control** | **YES** | Multi-warehouse stock, FIFO (First-In-First-Out) valuation, automatic stock ledger. | Barcode scanning is not built. |
| **Furnace Manufacturing & BOM** | **YES** | Bill of Materials (BOM) for each furnace model. A Work Order lists the materials, uses them up (FIFO) when completed, and puts the finished furnace into stock. | Labour/overhead cost is not added (furnaces are costed at material cost only). |
| **Delivery & Dispatch** | **YES** | One-click **Create Delivery Note**. Records carrier, vehicle, driver and **furnace serial numbers**. | E-Way Bill portal upload (NIC API) is not built. |
| **Automatic Asset Registration** | **YES** | When a serial-numbered furnace is dispatched, it is **registered as an installed Asset** under that customer. | — |
| **Sales Invoicing & Indian GST** | **YES** | One-click **Create Sales Invoice** from the delivery. Applies the GST template (CGST/SGST or IGST rows) and records what the customer owes. | E-Invoice (IRN / QR code) is not built. |
| **Payment Receipt & Tracking** | **YES** | **Payment Entry** records the bank transfer or cheque, allocates it against invoices, and the invoice becomes **Paid**. | — |
| **Installation & Commissioning** | **YES** | The commissioning date is recorded on the furnace's Asset record. A Field Work Order of type *Installation* is available for the installation job. | — |
| **Warranty & AMC Tracking** | **YES** | Commissioning automatically drafts the maker's warranty for the item's warranty months. AMC, CMC and Extended Warranty contracts are also supported. | You tick what each warranty covers (parts, labour, travel). Exclusions such as misuse can be written down, but the system does not apply them. |
| **Breakdown Service & Repair Tracking** | **YES** | Log a Service Request from the furnace → the system shows its warranty cover → schedule an engineer's visit → Field Work Order for the repair. | No phone app for technicians (they use the web page in a mobile browser). |
| **Spare Parts & Consumption on Repairs** | **YES** | The Field Work Order takes spare parts out of a chosen store. **Warranty parts are charged to Warranty Expense; other parts to Cost of Goods Sold.** | Returning faulty parts to the supplier is not automated. |
| **Repair Billing (Service Invoice)** | **YES** | One-click **Raise Service Invoice** on a completed repair. It bills **only the lines marked Billable to Customer**. | — |
| **Scheduled Maintenance (AMC Visits)** | **YES** | Maintenance Schedule holds the visit interval (e.g. every 90 days), creates visit work orders, and moves the next due date on after each visit. | Calendar-based only (no running-hours or meter-based maintenance). |
| **360° Furnace Service History** | **YES** | The furnace's Asset record shows its history: dispatch, commissioning, warranty, every request, visit, repair and parts used, with totals. | — |

---

## 2. Navigating the ERP: Golden Rules

### Rule 1: One Way In
- Everything happens in the **Desk — `http://knit360.localhost:8000/app`**: setup, CRM, sales, inventory, manufacturing, delivery, finance and service. Leads are entered only on the **Lead** form (**CRM** → **Lead** → **Add KNIT 360 Lead**).
- The sidebar on the left lists the areas: KNIT 360 (home), Platform, CRM, Sales, Finance, Tax, Procurement, Inventory, Warehouse, Manufacturing, Asset Management, Maintenance and others.
- The search bar at the top ("Search or type a command", shortcut **Ctrl + G**) opens any screen or record by name.
- On a narrow window, the extra step buttons at the top right (for example **Convert to Customer + Opportunity**, **Lost**) fold into the **⋯** menu next to the main button. Widen the window to see them side by side.

> **Important Hostname Tip**: Always use `http://knit360.localhost:8000`, not `localhost:8000`. The browser keeps a separate sign-in for each address, so being signed in on one does not sign you in on the other.

### Rule 2: How Documents Move (Business Status)
- **You cannot type a document's status** — the **Business Status** box is greyed out.
- Look at the **top right** of a saved document:
  - The dark button is the **next normal step** (e.g. **Initial Contact**, **Qualified**, **Confirmed / Booked**, **Dispatched / In Transit**).
  - Any other step allowed at that moment (e.g. **Lost**, **Cancelled**) appears as a **separate button beside it**.
  - The system only shows steps that are allowed from where the document is now. You cannot confirm an unaccepted quotation or ship an unconfirmed order.

### Rule 3: Save First, Then Press the Status Button
- If you change anything on a form, press **Save** (`Ctrl + S`) **before** pressing a status button. The status button works on the saved copy. Unsaved hours or a typed signature are not seen, and the step will be refused.
- `Ctrl + S` only ever saves. It never moves a document to its next status; only clicking a status button does.

### Rule 4: Never Re-Type
One document creates the next, using the button at the top right:
- **Lead** → **Convert to Customer + Opportunity**
- **Opportunity** → **Raise Quotation**
- **Quotation** → **Create Sales Order**
- **Sales Order** → **Create Delivery Note**
- **Delivery Note** → **Create Sales Invoice**
- **Asset (furnace)** → **Log Service Request**
- **Service Request** → **Schedule Visit** and **Create Work Order**
- **Field Work Order** → **Raise Service Invoice**
- **Maintenance Schedule** → **Create Visit Work Order**

Each button creates the new document, saves it as a draft, and opens it for you.

---

## 3. The Hands-On Test Walkthrough

Follow these exercises in order. Dates in the system are shown and typed as **day-month-year** (e.g. `31-10-2026`).

---

### Step 0: Open the Link and Sign In

1. **Open the link** in your browser: `http://knit360.localhost:8000/app`
2. You see a page titled **Login to KNIT 360**, with:
   - an **Email** box
   - a **Password** box (with **Show** to reveal what you typed)
   - **Forgot Password?**, a dark **Login** button, and **Login with Email Link**
3. **Sign in**:
   - **Email**: type `Administrator` (the box also accepts this user name, not only an email address)
   - **Password**: the administrator password that was set when this system was installed
   - Click **Login**
4. **If nobody knows the administrator password**: it is not written down anywhere in the project. Whoever runs the Docker setup can set a new one by running this in a terminal on that computer (replace `YOUR-NEW-PASSWORD`):
   ```bash
   docker exec -it knit-bench bash -lc "cd /home/frappe/frappe-bench && bench --site knit360.localhost set-admin-password YOUR-NEW-PASSWORD"
   ```
   Then sign in with `Administrator` and the new password.
5. **What you see after signing in**: the **KNIT 360** home screen (`/app/knit-360`).
   - An **At a glance** panel with four figures: **Open Leads**, **Open Opportunities**, **Quotations Awaiting Reply**, **Amount Outstanding**, and charts below them.
   - The **sidebar** of areas on the left.
   - The **search bar** at the top, and a round icon with your initial at the far top right (your settings and **Log out**).
6. **Note the Amount Outstanding figure now.** It adds up unpaid invoices for **every** company on this system, including the demo companies already here. You will compare it in Step 9.
7. **How to open any screen**: either click an area in the sidebar and then the screen's name, or type the screen's name in the search bar (e.g. `Item`) and press Enter. On a list, the dark button at the top right (e.g. **Add KNIT 360 Company**) creates a new record.

---

### Step 1: One-Time Test Company Setup

We will create a test furnace manufacturing company: **"Bharat Induction Furnaces Pvt Ltd"**.

1. **Create Company**:
   - In the sidebar, click **Platform** → **Company** → **Add KNIT 360 Company**.
   - Fill in:
     - **Company Name**: `Bharat Induction Furnaces Pvt Ltd`
     - **Default Currency**: `INR`
     - **Tax Registration Number**: `24ABCDE1234F1Z5` (an example Gujarat GSTIN for practice — use the real one in live use)
     - **Country**: `India`
     - **Abbreviation**: `BIF` (if left empty the system makes `BIFPL` from the initials). It is added to the end of every account name, e.g. `Bank Account - BIF`.
     - Leave all the **Default ... Account** boxes empty. They fill themselves in.
   - Click **Save** (`Ctrl + S`).
   - *What the ERP did*: it created the company's chart of accounts — **43 accounts** (23 you can post to, the rest are headings), including **Service Revenue - BIF** and **Warranty Expense - BIF**, a cost centre called **Main**, and filled in every default account on the company.
2. **Check the Fiscal Year (do not create it)**:
   - Go to **Finance** → **Fiscal Year**. The year **`2026-2027`** (01-04-2026 to 31-03-2027) **already exists** on this system and covers all companies.
   - Do not create it again: the system refuses a second year with the same name.
3. **Create Warehouses**:
   - Go to **Warehouse** → **Warehouse** → **Add KNIT 360 Warehouse**.
   - Create 4 warehouses, each with **Company** = `Bharat Induction Furnaces Pvt Ltd`:
     1. `Raw Material Store - BIF` (where coils, panels, hydraulic cylinders sit)
     2. `Finished Goods Store - BIF` (where assembled furnaces wait for dispatch)
     3. `Service Spares Store - BIF` (where repair spare parts sit)
     4. `Service Van 01 - BIF` (engineer vehicle stock)
   - Keep the `- BIF` ending: warehouse names must be unique across the whole system, and the demo company already has a `Finished Goods Store`.
4. **Create Items**:
   - Go to **Inventory** → **Item** → **Add KNIT 360 Item**. The units (`Nos`, `Set`, `Hour`) and categories already exist; pick them from the list.
   - **Item Code cannot be changed after saving.** Type it exactly as below.

   | Item Code | Item Name | Category | Stock UOM | HSN / SAC Code | Serial Tracked | Standard Warranty (Months) |
   | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
   | `FURNACE-1000KG` | 1000 kg Medium Frequency Induction Melting Furnace | Finished Goods | Nos | `8514` | **TICK** | `12` |
   | `RM-COIL-1000` | Induction Coil | Raw Materials | Nos | `8514` | — | — |
   | `RM-PANEL-500KW` | Power Thyristor Panel 500 kW | Raw Materials | Set | `8504` | — | — |
   | `SP-CABLE-W` | Water-Cooled Cable | Components | Nos | `8544` | — | — |
   | `SRV-LABOUR-HR` | Technician Labour Charge | Services | Hour | `998719` | — | — |
   | `SRV-SITE-VISIT` | Site Visit Charge | Services | Nos | `998719` | — | — |

   - The HSN / SAC codes are examples for practice. Confirm the real codes with your accountant.
5. **Selling Prices**:
   - **Inventory** → **Price List**: `Standard Selling` **already exists** (Currency INR, Applies To Selling, Is Default ticked). Nothing to create.
   - Go to **Inventory** → **Item Price** → **Add KNIT 360 Item Price**. One record per row below, each with **Price List** = `Standard Selling` and **UOM** = the item's unit:

   | Item | UOM | Rate |
   | :--- | :--- | ---: |
   | `FURNACE-1000KG` | Nos | `1800000` (₹ 18,00,000) |
   | `SP-CABLE-W` | Nos | `25000` |
   | `SRV-LABOUR-HR` | Hour | `1500` |
   | `SRV-SITE-VISIT` | Nos | `5000` |

6. **GST Tax Template**:
   - Go to **Tax** → **Tax Template** → **Add KNIT 360 Tax Template**:
   - **Template Name**: `GST 18% Intra-State`
   - **Company**: `Bharat Induction Furnaces Pvt Ltd`
   - In the **Taxes** table, add two rows:
     - Row 1: **Component** `CGST 9%` | **Rate** `9`
     - Row 2: **Component** `SGST 9%` | **Rate** `9`
   - Leave **Posts To** empty — the tax then goes to `Output Tax Payable - BIF`.
   - **Save**.
   - Note: the demo company has a template called `GST 18% (Intra-State)` (with brackets). Always pick **yours**, the one without brackets.

---

### Step 2: Build the Furnace Recipe (BOM)

To manufacture a furnace, the ERP needs to know what parts go into it.

1. Go to **Manufacturing** → **BOM** → **Add KNIT 360 BOM**.
2. Fill in:
   - **Produced Item**: `FURNACE-1000KG`
   - **Quantity**: `1`
   - **Company**: `Bharat Induction Furnaces Pvt Ltd`
   - **Is Active**: **TICK** (a work order refuses an inactive BOM)
3. In the **Components** table, add what is needed to make 1 furnace:
   - Row 1: **Item Code** `RM-COIL-1000` | **Quantity** `1`
   - Row 2: **Item Code** `RM-PANEL-500KW` | **Quantity** `1`
4. Click **Save**. It gets a number like `BOM-2026-0001`.

---

### Step 3: Put Initial Stock In (Goods Receipt)

A Goods Receipt brings everything into **one** warehouse, so you need **two** receipts: raw materials into the Raw Material Store, and the spare cables into the Service Spares Store (the repair in Step 10 takes its parts from there).

**Receipt 1 — Raw materials**
1. Go to **Procurement** → **Goods Receipt** → **Add KNIT 360 Goods Receipt**.
2. Fill in:
   - **Company**: `Bharat Induction Furnaces Pvt Ltd`
   - **Receiving Warehouse / Bay**: `Raw Material Store - BIF`
   - **Items** table:
     - **Item Code** `RM-COIL-1000` | **Arrived Qty** `2` | **Rate** `350000`
     - **Item Code** `RM-PANEL-500KW` | **Arrived Qty** `2` | **Rate** `450000`
3. Click **Save**.
4. Move it along with the buttons at the top right: **Received in Bay** → **Pending Inspection** → **Accepted & Staged**.
   - The stock arrives at **Received in Bay**. The books show **Stock In Hand - BIF** debited and **Stock Received But Not Billed - BIF** credited.

**Receipt 2 — Spare cables**
5. Make another Goods Receipt the same way:
   - **Receiving Warehouse / Bay**: `Service Spares Store - BIF`
   - **Items**: **Item Code** `SP-CABLE-W` | **Arrived Qty** `5` | **Rate** `15000`
   - **Save** → **Received in Bay** → **Pending Inspection** → **Accepted & Staged**.

6. **Check stock**: go to **Inventory** → **Stock Ledger Entry**. You will see each item received into its warehouse at its purchase rate.

---

### Step 4: CRM — From Customer Enquiry to Lead & Opportunity

> **Before salespeople use leads (admin, once per person):** give each salesperson a login with the role **Sales User** (a sales head: **Sales Manager**), not System Manager — a System Manager sees every lead. Then open their **Employee** record, set **Linked User** to that login and **Reports To** to their manager. A salesperson sees only leads they created or were given; their manager can read their leads but not change them.

Now a prospective foundry client calls wanting a furnace.

1. Go to **CRM** → **Lead** → **Add KNIT 360 Lead**:
   - **Organization Information**:
     - **Organization Name**: `Sardar Foundry Works LLP` (required)
     - **Company**: `Bharat Induction Furnaces Pvt Ltd` (required)
     - **Lead Source**: e.g. `Referral`
   - **Contact Details** (at least one person is required; click **+ Add New Contact** under the last person for more people at the same organization, now or later, and **Remove** to take one out):
     - **Person Name** `Rajesh Patel`, **Designation** `Plant Head`, **Department** `Production`
     - **Email** `rajesh@sardarfoundry.in`, **Phone** `+91 98250 11223`
     - A contact you added but left completely empty is ignored when you save.
   - **Assignment** → **Assigned To**: pick the salesperson who handles this lead. They can open and change it; the people they report to can open it to read. Under **Others With Access**, click **+ Add Person**, pick the employee from the dropdown and choose **Read Only** or **Read & Write**; **Remove** takes them off again. **Who Can Open This Lead** on the right shows everyone and why. (If you leave Assigned To empty while signed in as a salesperson, the lead is assigned to you.)
   - **Estimated Requirement**: `One 1000 kg induction furnace with commissioning`
   - Click **Save**.
   - Each person is now also in **CRM** → **Contact**, under the organization's name. After conversion they appear on the **Customer** page, under **Contacts**.
   - The small outline **ⓘ** next to a field's name explains the field: hover over it, or tap it on a phone.
   - In the lead list, **Organization Name** is the first column, followed by **Person Name**, **Designation**, **Phone**, **Email** and **Department**. Each of these cells lists every person on the lead in the same order (for example `Rajesh Patel, Anil Shah`); a `-` stands for a person who has no value there. How many columns fit depends on your screen width. To choose your own columns, switch the list to **Report** view (the view menu at the top). There you can add or hide any column, and your choice is saved for you only. A System Manager can also set the columns everyone sees in the lead list: click **List Settings**, the button beside **Add KNIT 360 Lead**, tick or drag the fields, and **Save**. The gear button next to it holds the list's permission settings. To find leads, use the bar above the list. Type any word into **Search leads by any word**: an organization, a person's name, part of a phone number or email, a city, a requirement or a salesperson's name. Only leads containing every word you type are listed, in any order (for example `steel meera`). Next to it, pick from the **Business Status**, **Stage Detail** or **Assigned To** dropdowns; the blank at the top of each means any. For anything else, such as dates, use the **Filter** button after them. The **x** clears the search, the dropdowns and the Filter button together.
2. **Move the Lead along** — one stage at a time, with the dark button at the top right:
   - **New Lead** → **Initial Contact** → **Requirement Pending** → **Requirement Received** → **Qualified**.
   - At Requirement Received you can instead choose **Potential Customer** (qualified, not ready yet); it becomes **Qualified** later.
   - **Not Qualified** or **Lost** ends a lead at any stage.
   - At Initial Contact, Requirement Pending and Requirement Received, **Stage Detail** (under Business Status) records the step reached, e.g. *WhatsApp Sent*, *Courtesy Call* or *Requirement Confirmed*. Pick it and **Save**. It offers only the current stage's steps and empties when the stage moves on.
   - **Tasks** (at the bottom of a saved lead, beside **Activity**) are your own reminders for this lead: pick a **Type** (Call, Meeting, Email or Other), a **Date** and **Time**, write a **Description**, and click **Add Task**. The lead lists only its own tasks, and only yours: nobody else, your manager included, sees them. Tick a task when it is done; click its text to change or delete it. At the task's time the bell at the top right shows a reminder that opens the lead.
   - On the **CRM** page, **My Tasks** shows your tasks for today across all your leads, each with its time and the organization and lead number, which open the lead. To see another day, past or future, click the date and pick it from the calendar; **Today** comes back.
   - In **Comments**, pick a **Type** beside the heading (Call, Meeting, Email or Other) when the comment reports on one, e.g. what was said on a call. Activity shows the type in bold above the text, with the date and time. Leave the type blank for a plain comment.
   - Each contact person has their own **Address**; the lead's own **Address** is a single line.
3. **Convert to Customer**:
   - On the Qualified lead, click the button **Convert to Customer + Opportunity** at the top right.
   - *Result*: the ERP creates linked records and opens the Opportunity:
     - Customer **`Sardar Foundry Works LLP`** (named after the Organization Name), with the first person's email and phone
     - A **Contact** (`CON-2026-…`, under **CRM** → **Contact**) for every person on the lead, with their designation, department, email and phone. The first is marked **Is Primary Contact** if the customer had no primary contact yet. A person the customer already has a contact of the same name for is not added twice.
     - Opportunity `OPP-2026-…`
   - The lead becomes **Converted**.

---

### Step 5: Create, Print/PDF & Send the Quotation

1. On the Opportunity, click **Raise Quotation** at the top right. The Quotation opens with the **Customer**, **Company** and **Price List** (`Standard Selling`) filled in.
2. In the **Items** table, add a row:
   - **Item Code**: type `FURNACE-1000KG` exactly (this box has no drop-down list)
   - **Quantity**: `1`
   - **Unit Rate**: leave empty
3. **Tax Template**: select `GST 18% Intra-State`.
4. Click **Save**.
   - *Notice*: **Unit Rate** fills in as `₹ 18,00,000` from the price list. **Net Total** = `₹ 18,00,000`, **Total Taxes** = `₹ 3,24,000`, **Grand Total** = `₹ 21,24,000`.
5. **Move the Quotation along**: click **Pending Approval**, then **Issued / Sent**. Once it is Issued / Sent, the figures are locked.
6. **Print / PDF**:
   - Click the **printer icon** in the top bar of the form.
   - The **Quotation** print layout shows: QUOTATION and its number, **To** (the customer's name), date, **Valid until** (if you filled **Valid Till**), opportunity and price list; the lines with Qty, Unit, Rate, Disc % and Amount; **Net total**, **CGST 9% at 9%** `₹ 1,62,000`, **SGST 9% at 9%** `₹ 1,62,000`, **Quoted total** `₹ 21,24,000`; and the amount in words.
   - Click **PDF** at the top of the print screen to download it.
7. **Sending it by email**:
   - At the bottom of the form, use **New Email**. Mail goes out through the outgoing mail account already set up on this system (see Section 4). Send one to yourself first to check it arrives.
   - Or download the PDF and attach it in your usual email.

---

### Step 6: Customer Accepts → Create the Sales Order

1. The customer calls and approves the quote.
2. Open the Quotation → click **Accepted**.
3. Click **Create Sales Order**.
4. The **Sales Order** opens, already saved as a draft:
   - The furnace, the agreed rate `₹ 18,00,000`, the GST template and the totals (`₹ 21,24,000`) are copied across. Nothing to re-type.
5. Confirm the order: click **Confirmed / Booked**.
   - *What the ERP did*: it checked the customer's credit limit and hold (none are set for this customer, so it passes) and booked the order.
6. Go back to the Quotation and click **Ordered** to complete the quotation trail. (Creating the order does not change the quotation by itself.)

---

### Step 7: Manufacturing the Furnace (Work Order & Stock Consumption)

The order is booked; now the factory floor makes the furnace.

1. Go to **Manufacturing** → **Work Order** → **Add KNIT 360 Work Order**.
2. Fill in:
   - **Target Item**: `FURNACE-1000KG`
   - **BOM**: the BOM from Step 2
   - **Quantity to Produce**: `1`
   - **Company**: `Bharat Induction Furnaces Pvt Ltd`
   - **Raw Materials From**: `Raw Material Store - BIF`
   - **Finished Goods To**: `Finished Goods Store - BIF`
   - **Against Sales Order**: your Sales Order (optional, links the two)
3. Click **Save**.
   - *Observe*: the **Materials** table fills in from the BOM: `RM-COIL-1000` × 1 and `RM-PANEL-500KW` × 1. The cost columns stay empty until completion.
4. When manufacturing starts: click **In Process**.
5. When furnace assembly is finished: click **Completed**.
   - *What happens*:
     - `1 RM-COIL-1000` (₹ 3,50,000) and `1 RM-PANEL-500KW` (₹ 4,50,000) leave `Raw Material Store - BIF`.
     - `1 FURNACE-1000KG` arrives in `Finished Goods Store - BIF`.
     - **Material Cost** and **Cost per Unit Produced** show `₹ 8,00,000`.
     - If any material had been short, completion would have been refused and nothing would have moved.

---

### Step 8: Product Delivery & Automatic Installed Asset Registration

1. Open your Sales Order (**Sales** → **Sales Order**, or search its number).
2. Click **Create Delivery Note**.
3. A small window asks for **Ship From Warehouse** → choose `Finished Goods Store - BIF` → confirm. The Delivery Note opens with the furnace line already on it.
4. Fill in **Carrier Details**, **Vehicle Number** (e.g. `GJ-01-AB-1234`) and **Driver Details**.
5. **Enter the Serial Number**:
   - In the **Items** table, click the **edit icon** at the right end of the furnace row.
   - In **Serial Numbers**, type `BIF-2026-SN-101`.
   - Close the row and click **Save**.
6. **Dispatch the Furnace**: click **Dispatched / In Transit**.
   - *At this moment*:
     - The furnace leaves `Finished Goods Store - BIF`, and its `₹ 8,00,000` cost is posted: **Cost of Goods Sold - BIF** debited, **Stock In Hand - BIF** credited.
     - **A new Asset record is created automatically** (Asset Management):
       - Number `AST-2026-…`, name `1000 kg Medium Frequency Induction Melting Furnace`
       - Serial Number `BIF-2026-SN-101`
       - Customer `Sardar Foundry Works LLP`
       - Linked to this Delivery Note and Sales Order, status **Registered**
7. When the truck reaches the customer's site: click **Delivered**.
8. *Optional tidy-up*: the Sales Order's status does not move by itself. You can move it on: **In Fulfillment** → **Delivered** → **Closed**.

---

### Step 9: Sales Invoicing & Payment Settlement

1. On the dispatched **Delivery Note**, click **Create Sales Invoice**.
2. The Sales Invoice opens as a draft:
   - 1 × `FURNACE-1000KG` at `₹ 18,00,000`, with the **Tax Template** `GST 18% Intra-State` already filled in from the order. **Grand Total** `₹ 21,24,000`.
3. Post it: click **Pending Approval** → **Posted / Unpaid**.
   - *What hits the books* (see it under **Finance** → **GL Entry** → **Filter** → **Voucher No** = the invoice number):
     - **Debtors - BIF** debited `₹ 21,24,000` (what the customer owes)
     - **Sales - BIF** credited `₹ 18,00,000`
     - **Output Tax Payable - BIF** credited `₹ 1,62,000` twice (CGST and SGST)
   - Click the **printer icon** → **PDF** for the invoice copy. It shows the invoice date, sales order, delivery note, lines, GST rows and total.
4. **Receive Payment from the Customer**:
   - Go to **Finance** → **Payment Entry** → **Add KNIT 360 Payment Entry**.
   - Fill in:
     - **Direction**: `Receive`
     - **Party Type**: `KNIT 360 Customer`
     - **Party**: `Sardar Foundry Works LLP`
     - **Company**: `Bharat Induction Furnaces Pvt Ltd`
     - **Payment Date**: today
     - **Amount**: `2124000`
     - **Payment Mode**: `Bank Transfer`
     - **Bank Account**: `Bank Account - BIF`
     - **Allocations** table, one row:
       - **Against Document Type**: `KNIT 360 Sales Invoice`
       - **Against Document**: your invoice number
       - **Allocated Amount**: `2124000`
   - Click **Save**.
   - Move it along: **Pending Bank Authorization** → **Disbursed / Cleared**.
   - The books show **Bank Account - BIF** debited and **Debtors - BIF** credited `₹ 21,24,000`.
5. **Check the Result**:
   - Open the Sales Invoice: its status is now **Paid** and **Outstanding Amount** is `₹ 0`.
   - On the KNIT 360 home screen (`/app/knit-360`), **Amount Outstanding** is back to the figure you noted in Step 0. It covers every company, so it only reaches ₹ 0 if no other company has unpaid invoices.

---

### Step 10: After-Sales Service, Commissioning, Repairs & Full History

#### 10.1 Commissioning & Warranty Activation
1. Go to **Asset Management** → **Asset** → open the furnace with Serial Number `BIF-2026-SN-101`.
2. Fill in:
   - **Installation Site Address**: `Plot 45, GIDC Industrial Estate, Naroda, Ahmedabad`
   - **Site Contact Person**: `Mr. Rajesh Patel, Plant Head`
   - **Commissioning Date**: today (it may not be earlier than the dispatch date)
   - Click **Save**.
3. Click **Commissioned / Operational**.
4. *What the ERP did*: a short note pops up saying it **drafted the 12-month warranty** `SC-2026-…` from the commissioning date, and asking you to tick what it covers. The warranty runs to the day before the same date next year (commissioned 31-10-2026 → ends 30-10-2027).
5. Open the warranty (the Asset's **Connections**, or **Maintenance** → **Service Contract**). It is **Contract Type** `Standard Warranty`, status **Draft**:
   - **Parts Covered**: **TICK**
   - **Labour Covered**: leave unticked (labour is billable in this test)
   - **Travel Covered**: leave unticked
   - Click **Save**, then **Active / In Coverage**.

---

#### 10.2 When the Customer Calls with a Breakdown
The customer calls: *"The furnace water-cooled cable is leaking and tripping the power supply."*

1. Open the furnace's Asset record.
2. Click **Log Service Request**. A small window asks **"What does the customer say is wrong?"**:
   - Type `Water-cooled cable rupture; furnace tripping on earth fault` and confirm.
   - The Service Request opens, already saved, with the customer filled in.
   - **Warranty / Contract Cover** shows: **`Standard Warranty to 30-10-2027: parts`** (your end date), and **Covering Contract** shows the warranty.
3. Click **Triaged**.
4. **Send an engineer**:
   - Click **Schedule Visit**. A **Service Dispatch** opens.
   - **Assigned Technician**: a user of this system (for the test, `Administrator`). **Scheduled Appointment**: date and time. **Save**.
   - Move the visit along: **Assigned** → **Dispatched / En Route** → **On Site** → **Work Started**.
5. Go back to the Service Request and click **Dispatched / Scheduled**. (Its status does not move by itself when you schedule the visit.)

---

#### 10.3 The Repair Job (Field Work Order) with Spare Parts
1. On the Service Request, click **Create Work Order**.
2. A **Field Work Order** opens with **Work Type** `Breakdown Repair`, the **Asset** and the **Service Request** filled in.
   - **Spare Parts From**: `Service Spares Store - BIF`
3. In the **Parts and Charges** table, add what was used:
   - Row 1: **Type** `Spare Part` | **Item** `SP-CABLE-W` | **Quantity** `1`
   - Row 2: **Type** `Labour` | **Item** `SRV-LABOUR-HR` | **Quantity** `4` (4 hours)
   - Row 3: **Type** `Travel` | **Item** `SRV-SITE-VISIT` | **Quantity** `1`
4. Click **Save**.
   - The ERP checks the warranty that was in force on the day the fault was reported, and fills the **Cover** column:
     - `SP-CABLE-W` → **Warranty Covered**
     - `SRV-LABOUR-HR` → **Billable to Customer**
     - `SRV-SITE-VISIT` → **Billable to Customer**
   - **Under Warranty** is ticked and **Covering Contract** shows the warranty.
5. Start the work: click **In Progress**. On the Service Request, click **Work In Progress**.
6. Finish the work:
   - Fill in **Actual Labour Hours** `4` and **Findings / Action Notes** `Replaced ruptured water-cooled cable with new assembly. Pressure tested to 4 bar. Normal operation verified.`
   - Click **Save** first, then click **Work Complete**.
   - If you press Work Complete without hours, it is refused: *"Record the hours spent on the job before marking the work complete."*
   - *Stock movement*: 1 `SP-CABLE-W` leaves `Service Spares Store - BIF` (5 → 4 left).
   - *Accounting*: **Parts Cost** shows `₹ 15,000` (the cable's purchase cost, not its ₹ 25,000 selling price). Because it is under warranty, **Warranty Expense - BIF** is debited `₹ 15,000` and **Stock In Hand - BIF** credited. Nothing is charged to the customer for it.
7. Customer sign-off:
   - In **Customer Signature**, type `Rajesh Patel, Sardar Foundry` → **Save** → click **Customer Signed Off**.
   - Without a signature it is refused: *"Record who signed for the work on the customer's side first."*

---

#### 10.4 Bill Only What Is Not Covered (Service Invoice)
1. On the Field Work Order, click **Raise Service Invoice** (available once the job is Work Complete).
2. A draft **Sales Invoice** opens with **only the billable lines**:
   - `SRV-LABOUR-HR` 4 × `₹ 1,500` = `₹ 6,000`
   - `SRV-SITE-VISIT` 1 × `₹ 5,000` = `₹ 5,000`
   - Both credited to **Service Revenue - BIF**. **Net Total** `₹ 11,000`.
   - *The warranty cable is not on the bill.*
3. The tax template is **not** filled in on a service invoice. Select **Tax Template** `GST 18% Intra-State` → **Save**. Total Taxes `₹ 1,980`, **Grand Total** `₹ 12,980`.
4. Click **Pending Approval** → **Posted / Unpaid**.
5. The customer pays `₹ 12,980` with a **Payment Entry**, exactly as in Step 9.
6. Close everything:
   - Field Work Order → **Closed**.
   - Service Request → **Resolved** → **Closed**. (A request cannot jump straight to Closed. It must go Triaged → Dispatched / Scheduled → Work In Progress → Resolved → Closed.)

---

#### 10.5 Planned Maintenance (AMC Visits)
1. Go to **Maintenance** → **Maintenance Schedule** → **Add KNIT 360 Maintenance Schedule**.
2. Fill in:
   - **Asset**: the furnace
   - **Service Contract**: the warranty (or the AMC, when you have one)
   - **Company**: `Bharat Induction Furnaces Pvt Ltd`
   - **Interval (Days)**: `90`
   - **Maintenance Tasks / Checklist**: `Check hydraulic pressure, inspect coil refractory lining, test water conductivity`
   - **Next Visit Due** starts empty. Type the first due date if you have one.
   - **Save**.
3. When a visit is due, click **Create Visit Work Order**. A Field Work Order opens with **Work Type** `Preventive Maintenance`, and the checklist is copied into **Standard Operating Procedures**.
4. Click **In Progress** → fill in **Actual Labour Hours** (e.g. `2`) → **Save** → **Work Complete**.
5. Open the Maintenance Schedule again: **Last Visit** shows the visit's work date, and **Next Visit Due** has moved on by 90 days (a visit on 31-10-2026 → next due 29-01-2027).

---

#### 10.6 The Furnace's Lifetime History
Open the furnace's Asset record and scroll to **Service History**:
- Every event, newest first: delivery (with the Delivery Note), becoming Commissioned / Operational, the Standard Warranty and its dates, the service request with its cover, the scheduled visit and engineer, the breakdown repair with notes and parts used, the preventive visit, and the service invoice.
- Totals for this test: **1** service request, **1** breakdown repair, **1** preventive visit, **6** labour hours, parts cost **₹ 15,000**, of which warranty parts **₹ 15,000**, and **₹ 12,980** billed (only posted service invoices are counted).

---

## 4. Honest Gap Assessment: What Is Not Built Yet?

These are not yet built, or have limits. Here is how your team should handle them today:

1. **Email Sending**:
   - An outgoing mail account is set up on this system (`omchaudhari2627@gmail.com`, through Gmail), so **New Email** can send. Its delivery was not tested in this run — send one to yourself first.
   - Fallback: download the **PDF** and attach it to your usual Outlook or Gmail message.
2. **Printouts**:
   - The quotation and invoice printouts do not show HSN codes, your GSTIN, or the customer's address or GSTIN. Your company name only appears if a **Letter Head** is added. Check them against what your accountant needs on a GST tax invoice before sending them to real customers.
3. **Labour & Overhead Cost Absorption in Manufacturing**:
   - Work Orders cost the furnace from raw material purchase prices (FIFO) only. Factory electricity and wages are not added to the furnace's stock value.
4. **NIC E-Way Bill & E-Invoice (IRN) Portal Sync**:
   - The ERP calculates the GST amounts, but there is no direct connection to the government NIC portal. Copy the figures into the GST / E-Way portal manually.
5. **Mobile App for Field Engineers**:
   - There is no app-store app. Service engineers use the web address in their phone's browser.
6. **Statuses that do not move by themselves**:
   - A Sales Order stays **Confirmed / Booked** after delivery, and a Service Request does not follow its visit or work order. Move them on with their buttons, as shown in Steps 8 and 10.

---

## 5. Summary & Recommendation

For a **Furnace Manufacturing & Repair business**, KNIT 360 covers the full chain tested above:
- No re-typing along Enquiry → Quotation → Order → Delivery → Invoice. Each document is made from the last with one button.
- Stock stays correct: the BOM lists the materials, completing production uses them up at FIFO cost, and nothing moves if anything is short.
- Every dispatched furnace is tracked by serial number. Each repair line is marked warranty-covered or billable, and only billable lines reach the customer's invoice.

Start at **Step 0**: open `http://knit360.localhost:8000/app` and sign in, then follow Section 3 in order.
