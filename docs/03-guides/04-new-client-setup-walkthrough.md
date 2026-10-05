# KNIT 360 — Setting Up a New Client, From Zero

## Document control

- **Document ID:** `03-guides/04-new-client-setup-walkthrough`
- **Date:** 5 October 2026
- **Status:** Operational walkthrough. Every field named here was read from the
  running system's own definitions before being written down.
- **Audience:** You, setting the system up and learning it. Not a client handout.
- **Practice company:** **Sunrise Steel Works** — a made-up business, used so that
  every value in this document is concrete rather than a placeholder.

**The rule for this document:** if a field is not listed in a step, it does not
exist on that screen. If a value is marked *leave blank*, that is a real
instruction, not an omission.

---

## 0. Before you touch the keyboard

### 0.1 The client you are setting this up for

They run the business on paper. A quotation is handwritten or typed into Word. An
order is a phone call written in a diary. Stock is counted by walking into the
store. The books are a cash book and a ledger, kept by hand or by an accountant
once a month.

That matters more than it sounds. Someone who has used Tally or Excel already
knows what a "master" is. This client does not. The single most useful thing you
can tell them on day one is this:

> **You enter a thing once, and then you point at it.** You type "MS Sheet
> 1.2 mm" one time, ever. After that, every quotation, order and invoice
> *points at* that one record. That is the whole idea. It is why the system can
> add up your sales by item, and why a spelling mistake cannot create a second
> product that nobody notices for a year.

### 0.2 What this system will and will not do for them on day one

Be straight about this before setup, not after.

| They do this on paper today | After setup |
| --- | --- |
| Write down enquiries and follow-ups | **In the system.** Works properly. |
| Make quotations | **In the system.** It calculates totals and discounts. But see §9 — you cannot print it yet. |
| Track orders | **In the system.** Works properly. |
| Raise invoices | **In the system.** It posts to the ledger correctly. |
| Know who owes them money | **In the system.** Works properly. |
| Record money received | **Still on paper.** See §9. |
| Track stock quantities | **Still on paper.** See §9. |
| File GST returns | **Still with their accountant.** See §9. |
| Payroll | **Still on paper.** Not built. |

A client who is told this upfront will trust the parts that do work. A client who
discovers it in month two will not.

### 0.3 Decide these with the client before you start

Four answers you need in hand. Everything else can be changed later; these are
awkward to change once there is data.

| | Question | For Sunrise Steel Works |
| --- | --- | --- |
| 1 | What is the exact legal name of the business? | Sunrise Steel Works |
| 2 | What are their financial year dates? | 1 April 2026 – 31 March 2027 |
| 3 | What units do they measure and sell in? | Nos, Set, Kg, Metre, Hour |
| 4 | How do they group what they sell? | Raw Material, Finished Goods, Consumables, Services |

---

## 1. Getting in

### 1.1 The address

Open **`http://knit360.localhost:8000`**

Use the name, not `localhost:8000`. A browser stores a sign-in against the host
name and ignores the port number, so if anything else is running on `localhost`
the two will log each other out.

### 1.2 First sign-in

You will see a sign-in box with the KNIT 360 name and mark above it.

| Field | Value |
| --- | --- |
| Email | `Administrator` |
| Password | The administrator password set when the site was created |

> The administrator password is **not recorded anywhere in this repository.**
> Whoever created the site has it. If nobody does, it can be reset from the
> command line, and that is the only way.

### 1.3 Change the password immediately

Top right → the circle with a letter in it → **My Settings** → set a new
password → **Update**.

### 1.4 Create a user for each person

**Search bar → type `User` → New**

For Sunrise Steel Works, three people:

| First Name | Email | Role |
| --- | --- | --- |
| Anita | `anita@sunriseoffice.example` | System Manager |
| Ramesh | `ramesh@sunriseoffice.example` | System Manager |
| Sunil | `sunil@sunriseoffice.example` | System Manager |

### 1.5 Read this before you give anyone a login

> **Everyone who uses KNIT 360 today must be a System Manager.** All 65 record
> types grant access to that one role and no other. There is no "Sales User" or
> "Accounts User".
>
> System Manager is the most powerful role in the system. It can change
> settings, delete records, and remove other users.
>
> **So: you cannot currently let a salesperson enter leads without also giving
> them the power to delete the company's accounts.** This was verified directly
> against the permissions table, not assumed.
>
> For a real client this is not acceptable beyond a pilot. It is listed as work
> to do in the handover document. For a practice setup it is fine.

### 1.6 The two front doors

| | Address | Use it for |
| --- | --- | --- |
| **The simple screen** | `/knit360` | Day-to-day sales work. Three stages. Works on a phone. |
| **The full system** | `/app` | Everything else — setup, finance, purchasing, stock. |

**All setup below happens in the full system (`/app`).**

### 1.7 How to find any screen

Two ways, and the second is faster once you know the names:

1. **Sidebar** — the areas down the left: CRM, Sales, Finance, and so on.
2. **Search bar** — top of the screen, or `Ctrl+G`. Type the record name
   ("Item", "Customer", "Fiscal Year") and press Enter.

To create something new, open its list and press **+ Add** (or **New**).

---

## 2. Setup — do these in this order

The order is not a preference. Later steps point at earlier ones, and a field
cannot point at something that does not exist yet.

---

### Step 1 — Fiscal Year

**Finance → Ledger → Fiscal Year → New**

Do this first. Nothing can post to the books without a financial year that
covers the posting date.

| Field | Value | Note |
| --- | --- | --- |
| Year Name | `2026-2027` | REQUIRED |
| Year Start Date | `01-04-2026` | REQUIRED |
| Year End Date | `31-03-2027` | REQUIRED |
| Is Closed | *unticked* | Tick only after the year is finished and audited |

**Save.**

> Years must not overlap. The system refuses an overlapping year, because a
> posting date has to fall in exactly one of them.

---

### Step 2 — Company

**Platform → Company → New**

| Field | Value | Note |
| --- | --- | --- |
| Company Name | `Sunrise Steel Works` | REQUIRED. The exact legal name. |
| Business Type | `Manufacturing` | Free text |
| Legal Entity | `Partnership` | Free text |
| Default Currency | `INR` | REQUIRED. Pick from the list. |
| Tax Registration Number | `27AAAAA0000A1Z5` | **A made-up number for practice. Replace with the client's real GSTIN.** |
| Country | `India` | Pick from the list |
| Fiscal Year Start Date | `01-04-2026` | |
| Fiscal Year End Date | `31-03-2027` | |
| Abbreviation | `SSW` | Short code. Appears on every account name. |

**Leave all eight account fields blank** — Default Receivable, Default Payable,
Default Income, Default Expense, Default Cash, Default Bank, Round Off, Default
Cost Center. They fill themselves in.

**Save.**

#### What just happened

Saving a company builds its entire chart of accounts automatically: **40
accounts under 5 headings**, a cost centre called **Main**, and all eight
defaults above filled in and pointing at the right accounts.

Go back into the company record and look — the account fields are now populated.

> This is new. Until this was fixed, creating a company through this screen
> produced **no accounts at all**, and you could not raise an invoice. If you
> are reading an older copy of a guide that tells you to run a command here,
> that copy is out of date.

#### The accounts you now have

Worth showing the client, because these are the names they will see on every
transaction. **Finance → Ledger → Account.**

```
Assets
  Current Assets
    Accounts Receivable  →  Debtors              ← who owes you
    Bank Accounts        →  Bank Account
    Cash In Hand         →  Cash
    Stock Assets         →  Stock In Hand
    Tax Assets           →  Input Tax Credit
  Fixed Assets
    Plant and Machinery
    Accumulated Depreciation

Liabilities
  Current Liabilities
    Accounts Payable     →  Creditors            ← who you owe
    Duties and Taxes     →  Output Tax Payable
    Stock Liabilities    →  Stock Received But Not Billed

Equity
  Share Capital
  Retained Earnings

Income
  Direct Income          →  Sales, Service Revenue
  Indirect Income        →  Other Income

Expenses
  Cost of Goods Sold
  Direct Expenses        →  Freight and Forwarding
  Indirect Expenses      →  Administrative Expenses, Depreciation, Round Off
```

Account names end in `- SSW`, the abbreviation. That is so a second company can
also have an account called Debtors without the two being confused.

**Indented names in bold above are headings.** You cannot post to a heading —
the system refuses — because a heading's balance has to stay exactly the sum of
what sits under it.

---

### Step 3 — Price Lists

**Inventory → Price List → New.** Two of them.

| Field | Selling list | Buying list |
| --- | --- | --- |
| Price List Name | `Standard Selling` | `Standard Buying` |
| Currency | `INR` | `INR` |
| Applies To | `Selling` | `Buying` |
| Is Default | *ticked* | *ticked* |
| Disabled | *unticked* | *unticked* |

One is what you charge. The other is what you pay.

---

### Step 4 — Units of measure

**Platform → UOM → New.** Five of them.

| UOM Name | Symbol | Category | Must Be Whole Number |
| --- | --- | --- | --- |
| `Nos` | `Nos` | Quantity | **ticked** |
| `Set` | `Set` | Quantity | **ticked** |
| `Kg` | `kg` | Weight | unticked |
| `Metre` | `m` | Length | unticked |
| `Hour` | `hr` | Time | unticked |

> "Must Be Whole Number" is ticked for chairs and sets because you cannot sell
> half a chair. It is unticked for Kg and Metre because 2.5 kg is a real
> quantity.

---

### Step 5 — Item Groups

**Inventory → Item Group → New.** A parent, then four children.

First the parent:

| Field | Value |
| --- | --- |
| Item Group Name | `All Item Groups` |
| Parent | *leave blank* |
| Is Group | **ticked** |

Then four, each with **Parent = `All Item Groups`** and **Is Group unticked**:

| Item Group Name | Description |
| --- | --- |
| `Raw Material` | Steel sheet, tube, fasteners |
| `Finished Goods` | Chairs, tables, racks ready to sell |
| `Consumables` | Paint, welding rods, packing |
| `Services` | Installation and site work |

---

### Step 6 — Brand

**Inventory → Brand → New**

| Field | Value |
| --- | --- |
| Brand | `Sunrise` |
| Description | `House brand` |

---

### Step 7 — Items

**Inventory → Item → New.** Six of them.

| Item Code | Item Name | Category | Stock UOM | Brand | Is Sales Item | Is Purchase Item |
| --- | --- | --- | --- | --- | --- | --- |
| `FG-CHAIR-01` | Office Chair, Steel Frame | Finished Goods | Nos | Sunrise | **tick** | untick |
| `FG-TABLE-01` | Office Table 4x2 ft | Finished Goods | Nos | Sunrise | **tick** | untick |
| `FG-RACK-01` | Storage Rack, 5 Shelf | Finished Goods | Nos | Sunrise | **tick** | untick |
| `RM-SHEET-01` | MS Sheet 1.2 mm | Raw Material | Kg | *blank* | untick | **tick** |
| `RM-TUBE-01` | MS Square Tube 25 mm | Raw Material | Metre | *blank* | untick | **tick** |
| `SV-INSTALL-01` | On-site Installation | Services | Hour | *blank* | **tick** | untick |

Other fields on each item:

| Field | What to put |
| --- | --- |
| HSN / SAC Code | **Leave blank for now.** This is a tax classification code and it affects the client's GST return. Get it from their accountant — do not guess it, and do not let me guess it either. |
| Batch Tracked / Serial Tracked | *unticked* — stock tracking is not built yet (§9) |
| Safety Stock | `0` |
| Valuation Method | `FIFO` |
| Description | Optional. Useful on a quotation. |
| Disabled | unticked |

> **Item Code is the name of the record and cannot be changed afterwards.** Agree
> a pattern with the client before entering the first one. The pattern above —
> `FG-` for finished goods, `RM-` for raw material, `SV-` for services — costs
> nothing now and sorts the list sensibly forever.

---

### Step 8 — Item Prices

**Inventory → Item Price → New.** One row per item per list.

Selling prices, all with **Price List = `Standard Selling`** and **Valid From =
`01-04-2026`**:

| Item | UOM | Rate |
| --- | --- | --- |
| `FG-CHAIR-01` | Nos | `2400` |
| `FG-TABLE-01` | Nos | `5800` |
| `FG-RACK-01` | Nos | `7200` |
| `SV-INSTALL-01` | Hour | `450` |

Buying prices, all with **Price List = `Standard Buying`**:

| Item | UOM | Rate |
| --- | --- | --- |
| `RM-SHEET-01` | Kg | `68` |
| `RM-TUBE-01` | Metre | `92` |

Leave **Currency** and **Valid Upto** blank. Currency fills itself in.

> Honest note: these prices are **stored but not yet read**. When you make a
> quotation you still type the rate by hand. Having the prices here is still
> worth doing — it is the agreed price list, and wiring the documents to read
> from it is a small piece of work listed in the handover.

---

### Step 9 — Territories

**CRM → Territory → New.** Parent first.

| Field | Value |
| --- | --- |
| Territory Name | `All Territories` |
| Parent | *leave blank* |
| Is Group | **ticked** |

Then four, each **Parent = `All Territories`**, **Is Group unticked**:

`Pune` · `Mumbai` · `Rest of Maharashtra` · `Outside Maharashtra`

> Keep it to how the client actually thinks about their map. If they say "local
> and outstation", use those two words. The system does not care; the salesperson
> does.

---

### Step 10 — Customer Groups

**CRM → Customer Group → New.** Parent first.

| Field | Value |
| --- | --- |
| Customer Group | `All Customer Groups` |
| Parent | *blank* · **Is Group ticked** · Default Price List *blank* |

Then four, each **Parent = `All Customer Groups`**, **Is Group unticked**,
**Default Price List = `Standard Selling`**:

`Corporate Office` · `Dealer` · `Government` · `Walk-in`

---

### Step 11 — Supplier Groups

**Supplier Management → Supplier Group → New.** Parent first.

| Field | Value |
| --- | --- |
| Supplier Group | `All Supplier Groups` · **Is Group ticked** · Parent blank |

Then four, each **Parent = `All Supplier Groups`**, **Is Group unticked**:

`Steel Supplier` · `Hardware Supplier` · `Job Work` · `Services`

---

### Step 12 — Warehouses

**Warehouse → Warehouse → New.** Three.

| Warehouse Name | Company | Parent Warehouse | Location |
| --- | --- | --- | --- |
| `Main Store` | Sunrise Steel Works | *blank* | *blank* |
| `Finished Goods Store` | Sunrise Steel Works | *blank* | *blank* |
| `Rejection Store` | Sunrise Steel Works | *blank* | *blank* |

> These are names only today. They hold no quantities, because stock movement is
> not built (§9). Create them anyway — documents point at them, and when stock
> is built the names will already be right.

---

### Step 13 — Tax Templates

**Tax → Tax Template → New.** Two.

**Template 1 — sales inside Maharashtra**

| Field | Value |
| --- | --- |
| Template Name | `GST 18% Within State` |
| Company | Sunrise Steel Works |
| Place of Supply | `Maharashtra` |

In the **Taxes** table, two rows:

| Component | Rate |
| --- | --- |
| `CGST` | `9` |
| `SGST` | `9` |

**Template 2 — sales outside Maharashtra**

| Field | Value |
| --- | --- |
| Template Name | `GST 18% Inter State` |
| Company | Sunrise Steel Works |
| Place of Supply | `Outside Maharashtra` |

Taxes table, one row:

| Component | Rate |
| --- | --- |
| `IGST` | `18` |

> **Confirm the rate with the client's accountant before going live.** 18% is
> used here as a worked example so the arithmetic in §3 is checkable. The rate
> that applies to their goods is a tax question, not a software one.
>
> **And read §9 before trusting the tax figure in the books.** The system
> calculates tax correctly on the document, but posts it to the Round Off
> account rather than to Output Tax Payable, because the tax template has no
> field yet to say which account it belongs to. That is a known, visible
> placeholder.

---

### Step 14 — Payment Terms

**Finance → Payment Term → New.** Four.

| Term Name | Credit Days | Invoice Portion | Description |
| --- | --- | --- | --- |
| `Advance` | `0` | `100` | Payment before dispatch |
| `Net 15` | `15` | `100` | Due 15 days from invoice |
| `Net 30` | `30` | `100` | Due 30 days from invoice |
| `Net 45` | `45` | `100` | Due 45 days from invoice |

---

### Step 15 — Payment Terms Template

**Finance → Payment Terms Template → New**

| Field | Value |
| --- | --- |
| Template Name | `50% Advance, Balance 30 Days` |

In the **Terms** table, two rows:

| Payment Term | Credit Days | Invoice Portion |
| --- | --- | --- |
| `Advance` | `0` | `50` |
| `Net 30` | `30` | `50` |

The two portions must add to 100.

---

### Step 16 — Modes of Payment

**Finance → Mode of Payment → New.** Four.

| Mode Name | Payment Type | Default Account |
| --- | --- | --- |
| `Cash` | `Cash` | `Cash - SSW` |
| `Bank Transfer` | `Bank` | `Bank Account - SSW` |
| `UPI` | `Bank` | `Bank Account - SSW` |
| `Cheque` | `Bank` | `Bank Account - SSW` |

Leave **Disabled** unticked on all four.

---

### Step 17 — Terms and Conditions

**Platform → Terms and Conditions → New**

| Field | Value |
| --- | --- |
| Title | `Standard Sales Terms` |
| Applies To | `Selling` |
| Terms | See below |
| Disabled | unticked |

```
1. Prices are in Indian Rupees and exclude GST unless stated.
2. This quotation is valid for 30 days from its date.
3. Payment: 50% advance with order, balance within 30 days of invoice.
4. Delivery: 2 to 3 weeks from receipt of confirmed order and advance.
5. Goods remain our property until paid for in full.
6. Installation is charged separately unless included as a line above.
```

> This is sample wording for practice. Have the client's own terms reviewed by
> whoever advises them before it goes to a real customer.

---

### Step 18 — Customers

**CRM → Customer → New.** Four.

| Customer Name | Company | Customer Type | Territory | Customer Group | Default Price List |
| --- | --- | --- | --- | --- | --- |
| `Pinnacle Offices Pvt Ltd` | Sunrise Steel Works | `Company` | Pune | Corporate Office | Standard Selling |
| `Deshmukh Furniture Mart` | Sunrise Steel Works | `Company` | Mumbai | Dealer | Standard Selling |
| `Zilla Parishad Satara` | Sunrise Steel Works | `Government` | Rest of Maharashtra | Government | Standard Selling |
| `Gupta Interiors` | Sunrise Steel Works | `Company` | Outside Maharashtra | Dealer | Standard Selling |

Contact details, same four rows in order:

| Default Currency | Email | Phone | Address |
| --- | --- | --- | --- |
| INR | `purchase@pinnacleoffices.example` | `020 2555 0101` | `3rd Floor, Shivaji Nagar, Pune 411005` |
| INR | `orders@deshmukhmart.example` | `022 2555 0202` | `Shop 14, Lamington Road, Mumbai 400007` |
| INR | `store@zpsatara.example` | `02162 555 303` | `Collectorate Campus, Satara 415001` |
| INR | `info@guptainteriors.example` | `079 2555 0404` | `Prahlad Nagar, Ahmedabad 380015` |

> **Customer Name is the record's name and cannot be changed later.** Use the
> exact name that goes on the invoice.

---

### Step 19 — Contacts

**CRM → Contact → New.** One per customer, so there is a person to call.

| Contact Name | Customer | Is Primary | Email | Phone | Designation |
| --- | --- | --- | --- | --- | --- |
| `Anil Deshpande` | Pinnacle Offices Pvt Ltd | **tick** | `anil@pinnacleoffices.example` | `98200 11111` | Admin Manager |
| `Suresh Deshmukh` | Deshmukh Furniture Mart | **tick** | `suresh@deshmukhmart.example` | `98200 22222` | Proprietor |
| `Vaishali Pawar` | Zilla Parishad Satara | **tick** | `vaishali@zpsatara.example` | `98200 33333` | Store Officer |
| `Mehul Gupta` | Gupta Interiors | **tick** | `mehul@guptainteriors.example` | `98200 44444` | Partner |

---

### Step 20 — Suppliers

**Supplier Management → Supplier → New.** Three.

| Legal Vendor Name | Company | Supplier Group | Classification |
| --- | --- | --- | --- |
| `Maharashtra Steel Traders` | Sunrise Steel Works | Steel Supplier | `Raw Material` |
| `Shree Hardware and Fittings` | Sunrise Steel Works | Hardware Supplier | `Components` |
| `Krishna Powder Coating` | Sunrise Steel Works | Job Work | `Processing` |

Same three rows in order:

| Trade Name | Default Currency | Contact Person | Phone | Email | Standard Payment Terms |
| --- | --- | --- | --- | --- | --- |
| MST | INR | `Kiran Jadhav` | `020 2555 1001` | `sales@mstraders.example` | Net 30 |
| Shree Hardware | INR | `Pravin Shah` | `020 2555 1002` | `orders@shreehardware.example` | Net 15 |
| Krishna Coating | INR | `Dilip More` | `020 2555 1003` | `works@krishnacoat.example` | Net 15 |

**Business Status** is read-only and starts at `Prospect / Draft`. You change it
with the buttons at the top right of the saved record, never by typing.

A supplier cannot jump straight to approved. Press, in order:

`Prospect / Draft` → **Under Compliance Review** → **Approved / Active**

Do that for all three, or they cannot be used on a purchase order.

> This two-step path is deliberate. It is the point at which somebody is meant
> to have checked the supplier's registration and bank details. The system will
> not let you skip it.

Bank fields — Account Number, IFSC, SWIFT, IBAN — leave blank for practice.

---

### Step 21 — Opening balances

The client has money in the bank and in the cash box on the day they start. Tell
the system, or the books start from zero and nothing will reconcile.

**Finance → Ledger → Journal Entry → New**

| Field | Value |
| --- | --- |
| Posting Date | `01-04-2026` |
| Company | Sunrise Steel Works |
| Entry Type | `Opening Entry` |
| Reference Number | *blank* |
| Reference Date | *blank* |
| User Remark | `Opening balances as at 1 April 2026` |

**Accounts** table, three rows:

| Account | Debit | Credit |
| --- | --- | --- |
| `Bank Account - SSW` | `300000` | `0` |
| `Cash - SSW` | `25000` | `0` |
| `Share Capital - SSW` | `0` | `325000` |

Leave Party Type, Party, Cost Center, Reference Type and Reference Name blank.

**Total Debit** and **Total Credit** fill in by themselves. Both must read
`325000`. If they do not match, the system refuses to save — that is the whole
point of double entry.

**Save**, then press **Posted**.

> Debits must equal credits exactly. If the client's real figures do not
> balance, the difference is something you have not listed yet — a loan, stock
> on hand, money owed to them. Find it; do not force it.

---

## 3. Your first sale, end to end

Nine documents, one deal. Do this once yourself before showing anybody.

**The deal:** Anil Deshpande at Pinnacle Offices wants 20 chairs and 4 tables.

### 3.1 The lead

**CRM → Lead → New**

| Field | Value |
| --- | --- |
| Prospect Name | `Anil Deshpande` |
| Organization Name | `Pinnacle Offices Pvt Ltd` |
| Lead Source | `Referral` |
| Company | Sunrise Steel Works |
| Assigned Territory | Pune |
| Email | `anil@pinnacleoffices.example` |
| Phone | `98200 11111` |
| Address | `3rd Floor, Shivaji Nagar, Pune 411005` |
| Estimated Requirement | `20 chairs and 4 tables for a new office floor` |

**Business Status** is read-only and reads `New`. **Converted Customer** and
**Converted Opportunity** are also read-only and fill themselves in later.

**Save.** It is named `LEAD-2026-0001`.

> **Where the buttons are.** Once a record is saved, its available moves appear
> as buttons at the **top right** of the screen. They are the only way to change
> a Business Status — the field itself is read-only on every record in the
> system. The buttons change as the record moves, because they are generated
> from what is legal right now rather than from a fixed list.

### 3.2 Move it along

On the saved record, the only buttons offered are **Contacted**,
**Disqualified** and **Lost**.

Press **Contacted**, then **Qualified**.

> Notice what is *not* offered: Converted. You cannot convert a lead you have
> not qualified. Not because somebody remembers to check — because the button
> is not there.
>
> Once it *is* Qualified, you will see **Convert to Customer + Opportunity** and
> not a plain "Converted". That is on purpose. Marking a lead converted and
> actually converting it are different things, and only one of them creates the
> customer. The screen offers the one that does the work.

### 3.3 Convert

Press **Convert to Customer + Opportunity**.

Two records appear at once: a **Customer** and an **Opportunity**. The lead's
two read-only fields now point at them.

> If a customer of that name already exists, it is reused rather than
> duplicated. That is why Pinnacle Offices does not appear twice — you created
> it in Step 18.

### 3.4 The opportunity

Open it. **CRM → Opportunity**

| Field | Value |
| --- | --- |
| Opportunity Title | *already filled* |
| Customer | *already filled* |
| Company | *already filled* |
| Source Lead | *read-only, already filled* |
| Expected Closing Date | `30-11-2026` |
| Currency | `INR` |
| Estimated Deal Value | `85000` |
| Sales Stage | `Qualification` |
| Win Probability | `60` |

**Save.** Then press **In Negotiation**, then **Proposal Sent**.

### 3.5 The quotation

Press **Raise Quotation** on the opportunity. The screen takes you straight to
the new quotation with the customer and the link back already filled in.

| Field | Value |
| --- | --- |
| Customer | Pinnacle Offices Pvt Ltd |
| Enquiry | *blank* |
| Opportunity | *already filled if created from the opportunity* |
| Company | Sunrise Steel Works |
| Currency | `INR` |
| Price List | Standard Selling |
| Valid Till | `30-11-2026` |
| Tax Template | `GST 18% Within State` |
| Payment Terms | `50% advance with order, balance within 30 days` |

**Items** table, two rows:

| Item Code | Description | Quantity | UOM | Unit Rate | Discount % |
| --- | --- | --- | --- | --- | --- |
| `FG-CHAIR-01` | Office Chair, Steel Frame | `20` | Nos | `2400` | `0` |
| `FG-TABLE-01` | Office Table 4x2 ft | `4` | Nos | `5800` | `0` |

**Do not type anything into Amount, Net Total, Total Taxes or Grand Total.**
They are calculated and the system will not let you.

**Save.** Check the arithmetic:

```
Chairs    20 × 2,400  =  48,000
Tables     4 × 5,800  =  23,200
                         ──────
Net Total                71,200
GST 18%                  12,816
                         ──────
Grand Total              84,016
```

#### Try breaking it

Worth doing once, so you understand what the system guarantees.

- Put `150` in Discount %. It refuses: a discount over 100 would mean paying the
  customer.
- Try to type `99999` into Grand Total. The field will not accept it. A total
  you can type is a total that can disagree with its own lines.

**Then press Pending Approval, then Issued / Sent.**

The lines are now frozen. To change the price, raise a new quotation.

### 3.6 The order

Customer says yes. On the quotation press **Accepted**.

**Sales → Sales Order → New**

| Field | Value |
| --- | --- |
| Customer | Pinnacle Offices Pvt Ltd |
| Quotation | `QTN-2026-0001` |
| Company | Sunrise Steel Works |
| Customer PO Number | `PO/PIN/2026/114` |
| Customer PO Date | `05-10-2026` |
| Currency | `INR` |
| Tax Template | `GST 18% Within State` |
| Billing Address | `3rd Floor, Shivaji Nagar, Pune 411005` |
| Shipping Address | *same* |
| Payment Terms | `50% advance, balance 30 days` |

**Items** table — the same two lines. The rate column here is called **Agreed
Rate**:

| Item Code | Quantity | UOM | Agreed Rate | Delivery Date |
| --- | --- | --- | --- | --- |
| `FG-CHAIR-01` | `20` | Nos | `2400` | `25-10-2026` |
| `FG-TABLE-01` | `4` | Nos | `5800` | `25-10-2026` |

**Save**, then press **Confirmed / Booked**.

### 3.7 The delivery note

**Sales → Delivery Note → New**

| Field | Value |
| --- | --- |
| Sales Order | `SO-2026-0001` |
| Company | Sunrise Steel Works |
| Delivery Note Date | `25-10-2026` |
| Packing Slip ID | `PS-114` |
| Carrier Details | `Own vehicle` |
| Vehicle Number | `MH 12 AB 1234` |
| Driver Details | `Ramesh, 98200 55555` |
| Ship To Address | `3rd Floor, Shivaji Nagar, Pune 411005` |

**Items**: item code and quantity only — there is no rate on a delivery note,
because a delivery note moves goods, not money.

**Save**, then **Dispatched / In Transit**, then **Delivered**.

> This records *that* goods went. It does **not** reduce stock — see §9.

### 3.8 The invoice

**Finance → Receivables → Sales Invoice → New**

| Field | Value |
| --- | --- |
| Customer | Pinnacle Offices Pvt Ltd |
| Company | Sunrise Steel Works |
| Posting Date | `25-10-2026` |
| Due Date | `24-11-2026` |
| Sales Order | `SO-2026-0001` |
| Delivery Note | `DN-2026-0001` |
| Currency | `INR` |
| Tax Template | `GST 18% Within State` |
| Debit To | *leave blank — it fills in as `Debtors - SSW`* |
| Payment Terms | `Balance due 30 days from invoice` |

**Items**, two rows. Leave **Income Account** and **Cost Center** blank; both
fill themselves in:

| Item Code | Quantity | UOM | Rate |
| --- | --- | --- | --- |
| `FG-CHAIR-01` | `20` | Nos | `2400` |
| `FG-TABLE-01` | `4` | Nos | `5800` |

**Save.** Grand Total `84,016`, Outstanding Amount `84,016`.

**Press Posted / Unpaid.**

#### What just hit the books

**Finance → Ledger → GL Entry**, filter by this invoice:

| Account | Debit | Credit |
| --- | --- | --- |
| `Debtors - SSW` | 84,016 | |
| `Sales - SSW` | | 71,200 |
| `Round Off - SSW` | | 12,816 |

Pinnacle owes 84,016. Sales income is 71,200.

> **The tax line is the placeholder.** 12,816 lands in Round Off, not in Output
> Tax Payable, because the tax template has no field to name its account. The
> figure is right and the account is wrong, deliberately and visibly. §9.

The invoice can no longer be edited. To correct it, press **Cancelled** — which
writes an equal and opposite entry — and raise a new one.

### 3.9 Getting paid

**This is where the system stops and the paper carries on.** See §9.1.

---

## 4. Your first purchase

Six documents. Buying 500 kg of steel sheet.

| Step | Screen | Key values |
| --- | --- | --- |
| 1 | **Procurement → Purchase Requisition** | Title `Steel for October production`, Company Sunrise Steel Works, Required By `12-10-2026`. Item `RM-SHEET-01`, Quantity `500`, Required By `12-10-2026` |
| 2 | **Procurement → Request for Quotation** | Title `RFQ - MS Sheet October`, Purchase Requisition `PR-2026-0001`, Bid Closing `08-10-2026`, Delivery Deadline `12-10-2026`. Then **Published / Sent** |
| 3 | **Procurement → Supplier Quotation** | Supplier `Maharashtra Steel Traders`, Against RFQ `RFQ-2026-0001`, Currency INR, Valid Till `20-10-2026`, Technical Score `8`. Item `RM-SHEET-01`, Qty `500`, Rate `68`, Lead Time `4`. Grand Total calculates to **34,000**. Then **Under Evaluation** → **Shortlisted** → **Awarded** |
| 4 | **Procurement → Purchase Order** | Supplier `Maharashtra Steel Traders`, Supplier Quotation `SQ-2026-0001`, Order Date `09-10-2026`, Ship To Warehouse `Main Store`, Tax Template `GST 18% Within State`. Item `RM-SHEET-01`, Qty `500`, UOM `Kg` *(typed, not a dropdown here)*, Agreed Rate `68`, Discount `0`, Delivery Date `12-10-2026`. Net 34,000, tax 6,120, Grand **40,120**. Then **Pending Approval** → **Approved / Ordered** |
| 5 | **Procurement → Goods Receipt** | Purchase Order `PO-2026-0001`, Challan Number `MST/2026/889`, Challan Date `12-10-2026`, Carrier `MST Transport`, Vehicle `MH 12 CD 5678`, Receiving Warehouse `Main Store`. Then **Received in Bay** → **Pending Inspection** → **Accepted & Staged** |
| 6 | **Finance → Payables → Supplier Invoice** | Supplier `Maharashtra Steel Traders`, Vendor Invoice Number `MST/INV/2026/441`, Vendor Invoice Date `12-10-2026`, Purchase Order `PO-2026-0001`, Goods Receipt `GRN-2026-0001`, Freight `1500`, Tax Template `GST 18% Within State`, Statutory Tax Amount `6120`. Item `RM-SHEET-01`, Qty `500`, Rate `68` |

> **Two honest notes on the buying side.**
>
> Purchase Order and Supplier Quotation calculate their totals correctly. **The
> Supplier Invoice does not** — it is the one money document with no grand
> total, because whether freight and statutory tax belong inside that total is
> the client's accounting decision, not a software one. Ask their accountant;
> it is a ten-minute fix once answered.
>
> **Nothing on the buying side reaches the books.** No purchase posts to
> Creditors. The purchase documents are a complete record of what was ordered
> and received; the accounting for it is still manual.

---

## 5. The money, monthly

### 5.1 Who owes you

**KNIT 360** home page → **Amount Outstanding** and **Unpaid Invoices**.
For the detail: **Finance → Receivables → Sales Invoice**, filter Business
Status to `Posted / Unpaid` and `Overdue`.

### 5.2 Marking something overdue

The system does **not** do this by itself — there is no scheduled job for it.
Once a week, filter invoices where Due Date is in the past and Business Status is
`Posted / Unpaid`, and press **Overdue** on each.

### 5.3 The trial balance

**Finance → Ledger.** Every account that has moved, its debits, its credits, and
whether the whole thing balances. If it does not balance, something is wrong with
the system, not with the data — the system refuses to write an unbalanced entry.

### 5.4 Correcting a mistake

Never delete. Open the posted document, press **Cancelled**, and raise a
replacement. The original and its reversal both stay visible.

---

## 6. Who does what, day to day

For Sunrise Steel Works, with the caveat from §1.5 that everyone is currently a
System Manager.

| Person | Uses | Does |
| --- | --- | --- |
| **Anita** (sales) | `/knit360` on her phone | Leads, opportunities, quotations |
| **Ramesh** (stores and dispatch) | `/app` | Delivery notes, goods receipts |
| **Sunil** (accounts) | `/app` | Sales invoices, supplier invoices, journal entries, the trial balance |

### A first week that works

| Day | Do this |
| --- | --- |
| 1 | Steps 1–2. Look at the chart of accounts together. |
| 2 | Steps 3–8. Items and prices are the longest part. |
| 3 | Steps 9–17. |
| 4 | Steps 18–21. Opening balances with their accountant on the phone. |
| 5 | §3, all nine documents, with the client driving and you watching. |

Do not train on all 16 areas. Train on the one path in §3. Everything else can
wait until they ask.

---

## 7. Checking you did it right

After setup, these should all be true:

| Check | Where | Expect |
| --- | --- | --- |
| Company has a chart | Finance → Ledger → Account | 40 accounts, all ending `- SSW` |
| Company defaults filled | Platform → Company → Sunrise Steel Works | All eight account fields populated |
| Fiscal year covers today | Finance → Fiscal Year | `2026-2027`, Is Closed unticked |
| Items have prices | Inventory → Item Price | 6 rows |
| Customers have groups | CRM → Customer | 4, each with a Territory and a Customer Group |
| Suppliers are usable | Supplier Management → Supplier | 3, all `Approved / Active` |
| Books balance | Finance → Ledger trial balance | Debits = Credits = 325,000 before any sale |

---

## 8. Things that will confuse a paper-based client

Worth saying out loud, in these words.

**"Why can't I just type the status?"**
> Because then it would be a note, not a fact. The system only offers moves that
> are allowed from where the document is now. That is what stops an invoice
> being marked paid before the money arrives.

**"I made a mistake, let me delete it."**
> You can delete a draft. You cannot delete something that has reached the
> books. You reverse it. Your accountant will tell you the same thing about a
> paper ledger — you strike through and re-enter, you do not tear out the page.

**"Why do I have to create the item first?"**
> So that when you ask "how many chairs did we sell this year", there is an
> answer. If everyone types the product name freehand, "Office Chair", "office
> chair" and "Off. Chair" are three different products and the question has no
> answer.

**"There are so many screens."**
> There are 16 areas. You will use three. The rest are there for when the
> business needs them.

**"What if I put in the wrong number?"**
> On a draft, fix it and save. Once it is posted, reverse and re-enter. Nothing
> you do can quietly corrupt the books — the system would rather refuse than
> guess.

---

## 9. What is not built — tell the client before go-live

Each of these is a real gap, verified, not a limitation of this guide.

### 9.1 Recording money received

**Payment Entry exists as a form but does not post to the ledger and does not
reduce the outstanding amount.**

So: marking an invoice `Paid` moves a label and nothing else. The books will
still show the customer owing the money.

**What the client does instead:** keep receipts on paper or in their bank
statement as they do now, and reconcile with the system's outstanding list by
hand. **Do not mark invoices Paid** — it will make the outstanding figure lie.

This is the single biggest gap and the next thing to be built.

### 9.2 Stock quantities

Delivery Note and Goods Receipt record quantities but **do not move stock**. Bin
holds no figure. Warehouses are names.

**What the client does instead:** keep counting stock the way they do now.

### 9.3 Tax accounts

Tax calculates correctly and posts to **Round Off**, not to Output Tax Payable.

**What the client does instead:** their accountant works GST from the invoices,
not from the trial balance. Tell the accountant this explicitly.

### 9.4 Printing and emailing

**There are no print formats.** You cannot produce a PDF quotation or invoice
from the system, and it sends no email.

**What the client does instead:** read the figures off the screen and type them
into their existing letterhead. This is the gap they will feel first and
complain about soonest — raise it before they discover it.

### 9.5 Purchases do not reach the books

No purchase document posts to Creditors.

### 9.6 Supplier Invoice has no total

See §4. Blocked on one accounting question.

### 9.7 Overdue is manual

See §5.2.

### 9.8 Everyone is an administrator

See §1.5.

### 9.9 Not built at all

HR and payroll. Marketing. Customer service and support tickets. Projects.
Logistics. E-commerce. Document management. Business intelligence beyond the
eight built-in charts.

---

## 10. The honest summary to give the client

> KNIT 360 will replace your paper for **sales**: enquiries, quotations, orders,
> deliveries, invoices, and knowing who owes you money. That part is complete
> and the books behind it are sound.
>
> It will **not yet** replace your paper for receipts, stock counts, GST
> returns, or printing documents on your letterhead. Those are being built in
> that order.
>
> Start with sales. Keep your existing paper for the rest. When you stop needing
> the paper for a thing, that is when that part is finished.
