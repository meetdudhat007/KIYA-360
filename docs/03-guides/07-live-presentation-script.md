# KNIT 360 — The Live Presentation

## Document control

- **Document ID:** `03-guides/07-live-presentation-script`
- **Date:** 8 October 2026
- **Status:** Operational. Written to be followed on screen, in order, in front
  of a client.
- **Method:** Every figure, document number and button name in this script was
  read off the running demonstration site on 8 October 2026. Nothing here is an
  illustration. If a number on your screen differs from one here, the site has
  been used since — say the number on your screen, not the number in this book.
- **Running time:** 35 minutes at a steady pace, or 15 minutes using only the
  sections marked **[SHORT]**.

> **How to read this.** Each step has three parts. **Go** is where to click.
> **Type** is exactly what to enter. **Say** is what to say while you do it —
> it is a prompt, not a script to recite; use your own words once you know the
> ground.

---

## 0. Before they arrive — fifteen minutes

| # | Do this | Why |
| --- | --- | --- |
| 1 | Start Docker Desktop, then run `docker compose -f infrastructure/docker-compose.dev.yml up -d` | The site is dead without it, and it takes a minute to warm up |
| 2 | Open `http://knit360.localhost:8000/login` and sign in | **Not** `localhost:8000` — the cookie is scoped to the hostname |
| 3 | Open these four tabs, in this order, and leave them open | You never want to be typing a URL while somebody watches |
| 4 | Turn off notifications on the machine | A message popping up mid-demonstration costs you the room |
| 5 | Have this document open on a phone or a second screen | Not on the screen you are sharing |

The four tabs:

```
1  http://knit360.localhost:8000/app/knit-360            the home screen
2  http://knit360.localhost:8000/app/knit-360-lead       the pipeline
3  http://knit360.localhost:8000/app/knit-360-gl-entry   the ledger
4  http://knit360.localhost:8000/app/knit-360-stock-ledger-entry
```

**If the data looks wrong or thin**, reseed before they arrive:

```bash
docker exec knit-bench bash -lc 'cd ~/frappe-bench && bench --site knit360.localhost execute knit360_core.demo.seed'
```

It is safe to run twice: it skips anything that already exists.

### Records to keep off the screen

These are left over from earlier testing and the owner chose to keep them. They
are harmless, but they look careless if a client reads them:

| Record | What it is |
| --- | --- |
| `LEAD-2026-0009`, `0010`, `0011` | named "meet dudhat" |
| Customer `onethrid` | a typed test name |
| `QTN-2026-0001`, `QTN-2026-0004` | quotations totalling 0.00 |
| `OPP-2026-0004` | the opportunity behind them |
| `SINV-2026-0001` | a cancelled invoice of 4,324,000 |

If a list is sorted so one of these is on top, scroll past it without comment.
Never say "ignore that one".

---

## 1. Opening — one minute **[SHORT]**

**Go:** tab 1, `/app/knit-360`.

**Say:**

> "This is KNIT 360. It is not a demonstration built for today — it is the
> system, with a company's worth of data in it, and everything I am about to do
> I will do live. If I break something you will see me break it.
>
> Four numbers at the top: open leads, open opportunities, quotations awaiting a
> reply, and the amount customers owe us. Every one of them is counted from the
> records underneath, not typed into a slide."

Point at **Amount Outstanding ₹4.80 K** and leave it there for a moment.

> "That figure is going to go to nothing in front of you this morning, and
> you will see exactly why."

---

## 2. Find anything — two minutes **[SHORT]**

**Go:** the search bar at the very top of the window.

**Type:** `Ambar`

**Say:**

> "One bar. Not a customer search and then an invoice search — one bar over
> every record in the system."

You will see the customer, their sales order, their invoices, the payment, the
credit note, all in one list, each labelled with the record type and where it
has got to.

**Type (clear it first):** `SINV-2026-0002`

**Say:**

> "And it reads the status straight off the document. That invoice says *Partly
> Paid*, because it is. Nothing here is a copy of the truth kept in step by
> hand."

Press **Enter** on that result to open the invoice. Leave it open for section 6.

---

## 3. A new customer, from first contact — six minutes **[SHORT]**

This is the part to do slowly. Everything is typed live.

### 3.1 Create the lead

**Go:** tab 2 → the blue **+ Add KNIT 360 Lead** button, top right.

**Type:**

| Field | Value |
| --- | --- |
| Lead Name | `Sanjay Kulkarni` |
| Organization Name | `Vidarbha Castings Pvt Ltd` |
| Lead Source | `Trade enquiry` |
| Company | `KNIT 360 Demo Co` |
| Territory | `West` |
| Email | `sanjay@vidarbha.example` |
| Phone | `+91 98000 00000` |
| Estimated Requirement | `Two 50 kW induction coil assemblies and commissioning` |

**Ctrl + S** to save.

**Say:**

> "That is an enquiry. Nothing has been promised and nothing has been counted."

### 3.2 Walk it along

Look at the **top right of the form**. There is a dark button with the next
step on it, and a `...` menu with the other legal moves.

**Go:** press the dark button — **Contacted**. Then press it again —
**Qualified**.

**Say:**

> "The system only ever offers the moves that are legal from where this document
> actually is. There is no dropdown of thirty statuses to pick the wrong one
> from, and the status cannot be typed at all — look at the field, it is grey."

### 3.3 Convert

**Go:** `...` menu → **Convert to Customer + Opportunity**.

**Say:**

> "One action. It creates the customer record and the opportunity, links them
> both back to where the enquiry came from, and marks the lead converted. Three
> records that can never disagree about who this is."

The screen moves to the new opportunity.

### 3.4 Raise the quotation — the moment worth waiting for

**Go:** on the opportunity, `...` menu → **Raise Quotation**.

On the quotation, scroll to **Items** and add two rows. **Enter the quantity
and nothing else:**

| Item Code | Qty | Unit Rate |
| --- | --- | --- |
| `FG-COIL-01` | `3` | **leave empty** |
| `SV-COMM-01` | `8` | **leave empty** |

**Ctrl + S.**

**Say — before you press save:**

> "I am going to enter what they want, and no prices at all."

**Say — after it saves:**

> "₹86,400. Three coils at twenty-four thousand, eight hours of commissioning at
> eighteen hundred. I did not type a single rate: those came from the price
> list, which is where your pricing decisions live. If I had typed a rate it
> would have stood — the salesperson in front of the customer may know something
> the master does not — and the list price would still have been recorded beside
> it, so you can see every discount anyone ever gave."

Scroll right on a line to show the **Price List Rate** column.

---

## 4. The order, and what a status means — three minutes

**Go:** tab 1 → search `SO-2026-0001` → open it.

**Say:**

> "This order is ₹1,24,800 and it is still a draft, because nobody has confirmed
> it. Watch the top right."

**Go:** press the dark **Confirmed / Booked** button.

**Say:**

> "That is not a label change. Confirming an order is where this business
> commits, so that is where the system checks the customer's credit — and we
> will come back to that in a minute.
>
> One more thing worth seeing." — open the `...` menu —
> "Every move it offers is a move the lifecycle allows from here. There is no
> Delete on a confirmed order, and no way to get it back to draft by editing a
> field. If something was wrong, you reverse it, and the reversal is visible."

---

## 5. Money in — five minutes **[SHORT]**

**Go:** the `SINV-2026-0002` tab from section 2 (or search it again).

**Say:**

> "Forty-eight thousand invoiced to Ambar Alloys. The invoice says ₹4,800 is
> still outstanding. That figure is not stored anywhere — it is worked out from
> the ledger every time you look at it, which is the only way it can never drift
> out of step with the books."

### 5.1 Show where the rest went

**Go:** search `PAY-2026-0001` → open it.

**Say:**

> "₹19,200 arrived and was allocated against that invoice. Allocation is the
> point: a payment can settle several invoices, or part of one, or arrive with
> no invoice at all — in which case the system holds it as money owed back to
> the customer, not as income. You cannot allocate more than an invoice owes.
> It refuses, rather than quietly capping the figure somebody typed."

### 5.2 Take the last payment live

**Go:** `/app/knit-360-payment-entry` → **+ Add KNIT 360 Payment Entry**.

**Type:**

| Field | Value |
| --- | --- |
| Company | `KNIT 360 Demo Co` |
| Payment Direction | `Receive` |
| Party Type | `KNIT 360 Customer` |
| Party | `Ambar Alloys Ltd` |
| Payment Date | today |
| Amount | `4800` |
| Bank Account | `Bank Account - K3DC` |
| Payment Mode | `Bank Transfer` |

In **Allocations**, add one row:

| Reference Doctype | Reference Name | Allocated Amount |
| --- | --- | --- |
| `KNIT 360 Sales Invoice` | `SINV-2026-0002` | `4800` |

**Ctrl + S**, then press the dark button twice: **Pending Bank
Authorization**, then **Disbursed / Cleared**.

**Go:** back to `SINV-2026-0002` and reload.

**Say:**

> "Paid. The invoice moved itself — I did not set that status, the settlement
> did. And if you go back to the home screen and reload it, Amount Outstanding
> is now nothing. Nobody updated that tile; it was counting the ledger all
> along."

---

## 6. A return, handled honestly — three minutes

**Go:** search `CRN-2026-0001` → open it.

**Say:**

> "A coil came back damaged. Most systems handle that by cancelling the invoice
> and pretending the sale never happened, which is a lie — the goods went out,
> the customer had them for a fortnight.
>
> This is a credit note for ₹24,000 against that invoice. It reduced what was
> owed, by exactly the mechanism a payment does, and it put the twenty-four
> thousand in an account called **Sales Returns** rather than quietly netting it
> off sales. That means at the end of the quarter you can answer the question
> 'how much did we take back, and from whom' — which you cannot do if returns
> disappear into the sales figure."

---

## 7. Stock, and what it really cost — five minutes **[SHORT]**

**Go:** tab 4, `/app/knit-360-stock-ledger-entry`.

**Say:**

> "Every movement of every item, and nothing else. There is no quantity field
> anywhere in this system. What you hold is the sum of what moved — so it cannot
> be edited, and it cannot disagree with itself."

**Go:** search `DN-2026-0018` → open it → scroll to **Items**.

**Say, pointing at the Cost column (`7,290.00`):**

> "Fifty IGBT modules went out on that dispatch. Nobody typed that cost.
>
> Those fifty came out of two deliveries — forty bought at ₹7,200 and forty at
> ₹7,650 — and the system took the oldest stock first, as it should: forty at
> 7,200 and ten at 7,650. ₹3,64,500 in total, which averages the 7,290 you are
> looking at. Thirty are left, and they are worth ₹2,29,500, because they are
> the newer ones.
>
> A dispatch is a quantity decision. What it cost was settled when you bought
> it."

**Then the line that lands with a finance person:**

**Go:** tab 3, `/app/knit-360-gl-entry` → filter **Account** = `Stock In Hand - K3DC`.

**Say:**

> "Stock In Hand in the accounts: ₹10,90,200. The stock ledger, item by item,
> adds to ₹10,90,200. Not reconciled monthly — the same event wrote both, so
> they cannot be different."

---

## 8. The buying side — four minutes

**Go:** search `GRN-2026-0001` → open it.

**Say:**

> "Goods arrive. They are ours and we owe for them, but no bill has said how
> much — so the value sits in an account of its own called **Stock Received But
> Not Billed**, instead of being guessed at in creditors."

**Go:** search `PINV-2026-0002` → open it.

**Say:**

> "Here is the bill that says how much: ₹3,42,240, which is forty modules,
> freight, and the tax they charged us. Three things happened when it was
> approved.
>
> It cleared exactly what that goods receipt had left waiting — not a figure
> recalculated from the bill, the figure that was actually posted, so a bill can
> never clear the same receipt twice.
>
> The tax they charged went into an asset, because you get it back. It is not an
> expense and it must not be buried in one.
>
> And the whole amount became a payable. It shows ₹3,27,840 owing now, because
> two modules failed inspection and went back on a debit note."

---

## 9. What it prints — three minutes **[SHORT]**

**Go:** open `SINV-2026-0002` → **Print** (the `...` menu, or Ctrl + P).

**Say:**

> "This is what the customer receives. Your letterhead at the top — and that is
> built from your company record, so when you change your address you change it
> in one place and every document follows.
>
> Tax broken out line by line, the amount in words, what has already been
> settled and what is now due."

**Then, and this is worth saying out loud:**

**Go:** search `DN-2026-0018` → **Print**.

**Say:**

> "And the delivery note has no money on it anywhere. The system knows what
> those goods cost — it needs to, for the accounts — but the person signing for
> them at the gate is not handed your cost price. That is deliberate, and there
> is an automated test that fails if anyone ever changes it."

---

## 10. Credit control, live — two minutes

**Go:** `/app/knit-360-customer/Konkan Steel Works`.

**Type:** Credit Limit = `50000`. **Ctrl + S.**

**Go:** `/app/knit-360-sales-invoice` → **+ Add** →

| Field | Value |
| --- | --- |
| Company | `KNIT 360 Demo Co` |
| Customer | `Konkan Steel Works` |
| Posting Date | today |
| Due Date | thirty days out |

One item line: `FG-PANEL-01`, qty `1`, rate `86000`. **Ctrl + S**, then press
the dark **Posted / Unpaid** button.

**It will refuse**, naming the limit and what they already owe.

**Say:**

> "Refused, not warned. A credit control that writes a warning into a log is one
> nobody reads — by the time anybody looks, the goods have gone.
>
> And it is checked against the ledger at the moment of the commitment, not
> against a stored total somebody maintains. If they paid you this morning, the
> headroom is back this morning."

**Afterwards:** set the limit back to blank and delete the draft invoice.

> "Blank means no limit, by the way. Not a limit of zero. A field nobody has
> filled in must never mean 'refuse everything'."

---

## 11. People — two minutes

**Go:** `/app/knit-360-leave-application`.

**Say:**

> "HR is one piece so far, and it is finished rather than sketched: leave.
> Entitlement, application, approval, and a ledger of days taken that works the
> same way the money ledger works — balance derived from entries, never stored.
>
> Open one and you will see the same lifecycle buttons you have seen all
> morning. It is one system, not five bolted together."

Open `LAP-2026-0002` (Fatima Shaikh, awaiting approval) and show the buttons.

**Be straight about the rest:**

> "Attendance, payroll, appraisal and recruitment are not built. I would rather
> show you four things that work than fourteen that nearly do."

---

## 12. The books — three minutes **[SHORT]**

**Go:** tab 3, `/app/knit-360-gl-entry`.

**Say:**

> "Everything you have watched this morning landed here, and this is the only
> place it landed. One module writes to this ledger. Nothing else in the system
> can, and there is a test that fails if that ever stops being true.
>
> Three rules, and they are not settings:
>
> Every entry balances, or it is never written.
>
> Nothing is ever deleted. Cancel an invoice and you get a mirror-image entry
> and both stay, so last month's accounts still say what they said last month.
>
> And a posting cannot be edited. Not by me, not by the administrator."

**Then the number:**

> "The whole company's books balance at ₹53,01,740 on each side. Not because
> somebody adjusted them — because an unbalanced entry has never been written."

---

## 13. Why you should believe any of it — three minutes **[SHORT]**

**Say:**

> "Two hundred and five automated checks run against this system. Forty-nine
> read the definitions. One hundred and fifty-six drive the live application —
> they create documents, move them, post to the ledger, and assert on what came
> back — and then delete everything they made.
>
> I can run them now if you would like. It takes about a minute."

**Go (only if they say yes):** a terminal, and run

```bash
docker exec knit-bench bash -lc 'cd ~/frappe-bench && bench --site knit360.localhost execute knit360_core.acceptance.run_and_clean'
```

It prints a line per check and ends with `156/156 checks passed`.

**Then the coverage report, which is the honest part:**

```bash
docker exec knit-bench bash -lc 'cd ~/frappe-bench && bench --site knit360.localhost execute knit360_core.traceability.print_summary'
```

**Say:**

> "And this is the figure I would be hiding if I were selling you something.
> Seventy-one of the two hundred and thirty-eight requirements in your document
> are covered: twelve proven by a test that drives them, fifty-nine modelled —
> the records exist and are correctly shaped — and a hundred and sixty-seven not
> started. Fifteen of the twenty-eight modules have something in them.
>
> That report is generated from the system itself, every time you run it. It
> cannot flatter us."

---

## 14. On a phone — one minute

Open the same site on your phone, or narrow the browser window hard.

**Say:**

> "Same system, no separate app to buy. The next step in a document's life is a
> button under your thumb rather than three taps into a menu, and the forms read
> as forms rather than as a specification."

---

## 15. The questions they will ask

| They ask | Say |
| --- | --- |
| "Can it do GST returns?" | "It records the tax on every document and posts it to the right accounts — output tax to a liability, input tax to an asset. **It does not file returns and it does not print a customer's GSTIN or HSN codes**, because no field holds them yet. That is a defined piece of work, not a mystery." |
| "What about e-way bills / e-invoicing?" | "Not built. It would be an integration with the government portal and it needs a decision from you about which provider." |
| "Can we import our existing data?" | "Not yet — that is the next piece of work and nothing blocks it. It is also the thing that decides your go-live date, so it is worth starting early." |
| "Can my salesperson see only their own leads?" | "Today every user who can log in is an administrator. Roles are built but not yet assigned per record type. That is a known gap and it is written down." |
| "Does it email the customer the invoice?" | "The documents are ready to send. The mail account is not connected yet — that is a five-minute job needing your mail password, which I will not ask you for and would not type in anyway." |
| "How many users?" | "No licence limit in the software. The question is the machine it runs on, and that is a hosting decision we have not taken." |
| "Is this ERPNext?" | "No. It runs on the Frappe framework, which is MIT-licensed, and ERPNext is not installed — there is a test on every run that fails if it ever is. The business logic is ours." |
| "What happens if two people edit the same thing?" | "The second one is told the document changed under them. Nothing is silently overwritten." |
| "Can we see who changed what?" | "Every status move is logged with who, when and why, and the ledger keeps cancelled entries rather than deleting them." |

**If you do not know, say so.** The one answer that costs you the deal is a
confident wrong one.

---

## 16. If something goes wrong

| What happens | Do this |
| --- | --- |
| A page will not load | Reload once. If it is still dead, `docker compose -f infrastructure/docker-compose.dev.yml restart bench` and talk about the architecture for ninety seconds |
| A button you expected is missing | The document is not where you thought. Check the Business Status field — say "it is already past that step" and move on |
| A save is refused | **Read the message out loud.** It is written in plain English and the refusal is the feature. "That is the system stopping me doing something wrong" is a better moment than the one you planned |
| A figure differs from this script | Say the figure on the screen. The site has been used since this was written |
| You lose your place | Go to tab 1 and start the next section. The sections do not depend on each other except section 5, which needs section 2 |

---

## 17. The closing — thirty seconds **[SHORT]**

**Say:**

> "What you have seen is the spine: an enquiry becoming a customer, a quotation
> becoming an order, goods moving and being costed, money arriving, and all of
> it landing on a ledger that balances and cannot be rewritten.
>
> Around that spine there are ninety-nine record types, and most of them are
> still forms rather than finished processes. I have a written list of exactly
> which, and I would rather hand you that than let you find out yourself."

Hand them `docs/03-guides/03-handover-what-is-left.md`, or read the honest
summary out of it.

---

## Appendix — every figure in this script

Read from the demonstration site on 8 October 2026.

| Thing | Figure |
| --- | --- |
| Open leads / opportunities / quotations awaiting reply | 4 / 5 / 3 |
| Amount outstanding (before section 5) | ₹4,800 |
| `SINV-2026-0002` | 48,000 total, 4,800 outstanding, Partly Paid |
| `PAY-2026-0001` | 19,200 received and allocated |
| `CRN-2026-0001` | 24,000 credited against `SINV-2026-0002` |
| `SO-2026-0001` | 1,24,800, Draft |
| `QTN-2026-0005` | 1,43,865.60, Issued / Sent |
| Live quotation (section 3) | 3 × 24,000 + 8 × 1,800 = **86,400** |
| `DN-2026-0018` | 50 IGBT out at 7,290 = 3,64,500 |
| IGBT left in Main Store | 30, worth 2,29,500 |
| Stock In Hand (ledger and accounts) | 10,90,200 |
| Stock Received But Not Billed | 12,40,300 still awaiting bills |
| `PINV-2026-0002` | 3,42,240 billed, 3,27,840 owing |
| `DBN-2026-0001` | 14,400 debited back |
| Trial balance | 53,01,740 each side |
| Automated checks | 205 — 49 structural, 156 runtime |
| Requirement coverage | 71 of 238 — 12 proven, 59 modelled, 167 not started |
| Modules with something built | 15 of 28 |
