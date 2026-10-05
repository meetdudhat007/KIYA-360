# KNIT 360 — User Guide

## Document control

- **Document ID:** `03-guides/01-user-guide`
- **Date:** 5 October 2026
- **Status:** Operational guide. Describes the system **as it is built today**, not as the BRD specifies it.
- **Method:** Every screen, field and behaviour described here was checked against
  the running site before it was written. Where something is not built, this
  guide says so rather than describing an intention.

This guide assumes no technical knowledge. It uses no jargon without explaining
it first.

---

## 1. What KNIT 360 is

KNIT 360 is one system that holds the whole life of a sale and the money behind
it. Instead of a quote in a spreadsheet, an order in an email and the invoice in
an accounting package, each of those is one record here and they are linked to
each other.

The central idea is **one document becomes the next**. A lead becomes an
opportunity. An opportunity becomes a quotation. A quotation becomes an order.
An order becomes an invoice. Nothing is re-typed, so nothing can disagree.

---

## 2. The two ways in

There are two front doors to the same data. Which one you use depends on what
you are doing, not on who you are.

| | **The simple screen** | **The full system** |
| --- | --- | --- |
| Address | `/knit360` | `/app` |
| Built for | Someone doing one job: working a sales pipeline | Someone who needs everything: finance, stock, purchasing |
| Shows | Three stages, one list, one document | 16 areas, 65 record types, charts |
| Works on a phone | Yes, designed for it | Poorly — it is a desktop screen |
| Tells you what to do next | Yes, in plain sentences | No, it assumes you know |

Start people on the simple screen. Move them to the full system when they ask
for something it does not have.

### Signing in

Both doors use the same sign-in. If you are signed in to one, you are signed in
to the other.

> **If signing in logs you out of something else:** a browser stores its sign-in
> against a host name and ignores the port number. Two systems both running on
> `localhost` therefore overwrite each other's sign-in. This is why KNIT 360 runs
> at `knit360.localhost` and not at `localhost:8000`. Use the name, not the port.

---

## 3. The simple screen, step by step

Open `/knit360`.

### 3.1 The strip across the top

```
  1  Leads            2  Opportunities        3  Quotations
     8 total               3 total                3 total
     5 still open          3 still open           3 still open
```

This is the journey, left to right. The numbers are live. Tap one to work in it.

On a phone the strip scrolls sideways, so the work stays at the top of the
screen rather than being pushed below the fold.

### 3.2 The three stages in plain words

**Leads** — someone who *might* buy from you. A name, a company, how they found
you. Nothing is promised and no money is involved. Most leads go nowhere, and
that is normal.

**Opportunities** — a lead you have decided is real. It has a value and an
expected closing date, so it can be forecast. One customer can have several.

**Quotations** — the price you have put in writing. It has lines, quantities,
rates, discounts and a total. This is the first document a customer sees.

### 3.3 Adding a lead

The form sits above the list. It asks for one thing that matters — who you spoke
to — and everything else is optional. Fill it in, press **Add this lead**.

### 3.4 Opening a record

Tap any row. On a wide screen the record opens beside the list. On a phone the
list is replaced by the record, and a **Back to the list** control appears at the
top.

### 3.5 Moving something forward

Each record shows:

- **Where it is now** — its status, with a sentence explaining what that means
- **What you can do next** — one button per legal move, no others
- **What has happened to it** — every past change, who made it and when

You cannot type a status. You can only press one of the offered buttons. This is
deliberate: it is what stops a quotation being marked Accepted before anyone sent
it.

Some moves are one-way. When a move will lock the record, you are warned before
it happens and asked to confirm.

### 3.6 Editing the lines on a quotation

Open a quotation and use the line editor. Enter the item, the quantity, the unit
rate and a discount percentage if there is one. The **amount** and the
**totals** are calculated — you cannot type them, because a total you can type is
a total that can disagree with its own lines.

Once a quotation has been sent, its lines are frozen. To change the price, raise
a new one.

---

## 4. The full system, area by area

Open `/app`. The left sidebar lists 16 areas. Each one is a group of related
record types.

### The landing area

**KNIT 360** — the home page. Four headline figures across the top, then four
charts, then shortcuts into the Customer-to-Cash documents. This is the page to
open first each morning.

### The sales side

| Area | What it holds | What you do here |
| --- | --- | --- |
| **CRM** | Lead, Opportunity, Customer, Contact, Customer Group, Territory | Everything before there is a price. Who they are, where they are, how real the deal is. |
| **Sales** | Enquiry, Quotation, Sales Order, Delivery Note | From the customer asking, to the price, to the commitment, to the goods leaving. |
| **Finance** | Split into three: **Ledger**, **Receivables**, **Payables** | The money. Invoices, payments, journals and the accounts themselves. |
| **Tax** | Tax Template | The rates applied to a document. |

### The buying side

| Area | What it holds | What you do here |
| --- | --- | --- |
| **Procurement** | Purchase Requisition, Request for Quotation, Supplier Quotation, Purchase Order, Goods Receipt | From "we need this" to "it has arrived". |
| **Supplier Management** | Supplier, Supplier Group, Supplier Scorecard, Sourcing Project | Who you buy from and how well they perform. |

### The things side

| Area | What it holds | What you do here |
| --- | --- | --- |
| **Inventory** | Item, Item Group, Brand, Price List, Item Price, Stock Reservation | What you sell and buy, and what it costs. |
| **Warehouse** | Warehouse, Bin, Putaway Task | Where it physically sits. |
| **MRP** | Material Plan | What you will need and when. |
| **Manufacturing** | BOM, Work Order | What is made from what, and the instruction to make it. |
| **Quality** | Quality Inspection, Inspection Template, Non Conformance Report | Whether it was right, and what happened when it was not. |

### The after-the-sale side

| Area | What it holds | What you do here |
| --- | --- | --- |
| **Asset Management** | Asset | Equipment you own or have sold and still support. |
| **Maintenance** | Service Request, Field Work Order, Service Contract, Service Dispatch, Maintenance Schedule | Someone needs a machine fixed, and the engineer who goes. |

### The underneath

| Area | What it holds | What you do here |
| --- | --- | --- |
| **Platform** | Company, Location, Branch, Division, Department, Designation, Employee, UOM, Incoterm, Terms and Conditions | Set-up. Mostly done once. |
| **Business Status** | Business Status Log | The audit trail of every status change in the system. |

> **Users, Website, Tools, Integrations, Build** also appear in the sidebar.
> These belong to Frappe, the framework KNIT 360 is built on. They are not part
> of KNIT 360 and most people should ignore them.

---

## 5. How a document moves — the one concept worth learning

Every important record has a **business status**. Not "Submitted" or "Draft" in a
technical sense — words that mean something to the business: *Qualified*,
*Issued / Sent*, *Posted / Unpaid*, *Overdue*.

Twenty-three of these status tracks are defined, one per document type.

The moves open to a record appear as buttons at the top right of its screen.
They are generated from what is legal at that moment, so the set changes as the
record moves.

Three rules hold everywhere:

**1. You cannot type a status.** The field is read-only on every single
document. The only way it changes is by pressing an offered button.

**2. Only legal moves are offered.** A lead can go from *New* to *Contacted*,
*Disqualified* or *Lost* — and to nothing else. *Converted* is not offered,
because you have not qualified them yet.

**3. Some statuses lock the document.** Once a quotation is *Issued / Sent*, its
lines cannot change. Once an invoice is *Posted / Unpaid*, it has hit the
ledger and cannot be edited at all. You reverse it; you do not rub it out.

> **A note on the Submit button.** Frappe, the underlying framework, puts a
> Submit button on documents. In KNIT 360 pressing it does nothing — it refuses
> and tells you to move the business status instead. This is on purpose: if
> Submit worked, it would post to the ledger without the status changing, and
> the books and the document would then disagree.

---

## 6. The money, and where it goes

### 6.1 The chart of accounts

When a company is created, KNIT 360 builds it a chart of accounts: 40 accounts
under five roots — Assets, Liabilities, Equity, Income, Expenses.

Accounts come in two kinds. **Group** accounts are headings and hold no money of
their own; their balance is the sum of what is underneath. **Leaf** accounts are
where postings land. Posting to a group account is refused.

### 6.2 What actually posts

Only two documents currently write to the ledger:

| Document | What it does to the books |
| --- | --- |
| **Journal Entry** | Whatever you tell it, as long as it balances. Used for opening balances, corrections, write-offs. |
| **Sales Invoice** | Debits the receivable account with the total; credits each line's income account. |

Every posting is double-entry: debits must equal credits, to within half a paisa,
or nothing is written at all.

### 6.3 Reversing

Nothing in the ledger is ever deleted or edited. Cancelling a posted document
writes an equal and opposite entry, so the original stays visible and the net
effect is nil. You can always see what the books once said.

### 6.4 The trial balance

Finance → the trial balance lists every account that has moved, its debits, its
credits and its balance, and states whether the whole thing balances. It is the
one-line answer to "are the books sound?"

---

## 7. The charts

Eight charts and six headline figures are built into the system and refresh
themselves.

| Figure | What it counts |
| --- | --- |
| Open Leads | Leads not yet converted, disqualified or lost |
| Open Opportunities | Deals neither won nor lost |
| Pipeline Value | The money value of those open deals |
| Quotations Awaiting Reply | Quotations sent and not yet answered |
| Unpaid Invoices | Invoices posted, part-paid or overdue |
| Amount Outstanding | What that adds up to |

Charts appear on the home page and on the CRM, Sales, Finance and Procurement
areas, each showing what is relevant there.

---

## 8. Common tasks

### Win a deal, from first contact to invoice

1. **CRM → Lead → new.** Name, company, how they found you. Save.
2. Press **Contacted** when you have spoken to them.
3. Press **Qualified** when you believe it is real.
4. Press **Convert**. This creates the Customer and the Opportunity in one step.
5. Open the Opportunity. Set its value and expected closing date.
6. Move it to **In Negotiation**, then **Proposal Sent**.
7. Press **Create Quotation**. The customer and the link back are filled in.
8. Add the lines. The totals calculate.
9. Move the quotation to **Pending Approval**, then **Issued / Sent**.
10. When they say yes, **Accepted**.
11. **Sales → Sales Order → new**, referencing the quotation. Add the lines.
12. **Finance → Sales Invoice → new**, referencing the order.
13. Move it to **Posted / Unpaid**. It now hits the ledger and shows as
    outstanding.

### Correct a posted invoice

You cannot edit it. Move it to **Cancelled**, which reverses its ledger entries,
then raise a replacement.

### Set up a second company

**Platform → Company → new.** Give it a name and a currency. Its chart of
accounts is built automatically. Accounts are suffixed with the company's
initials, because two companies both need an account called Debtors.

---

## 9. What you will notice is missing

Stated plainly, because finding out during a demonstration is worse.

| What | What happens today |
| --- | --- |
| **Recording a payment** | Payment Entry exists as a form but does not post to the ledger and does not reduce the outstanding amount. Marking an invoice Paid is currently an unbacked claim, which is why the sample data leaves invoices outstanding. |
| **Stock levels** | Delivery Note and Goods Receipt record quantities but do not move stock. Bin holds no live figure. |
| **Tax accounts** | A tax template calculates a figure correctly, but on an invoice that figure is posted to the round-off account as a visible placeholder. Real tax accounts are a separate piece of work. |
| **Purchasing and the ledger** | Purchase Order and Supplier Quotation now total correctly, but nothing on the buying side posts to the books. |
| **HR and payroll** | Not started. Deliberately deferred. |
| **Printing** | Printing and PDF both work, but there is no designed print format and no letterhead, so output is a plain field-by-field printout rather than a laid-out document. |
| **Email** | The system can email documents, but no outgoing mail account is configured, so nothing can be sent yet. |

Section 3 of the handover document lists what has to happen to close each of
these and who has to do it.
