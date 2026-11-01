# The Money Decisions, in Plain Language

## Document control

- **Document ID:** `03-guides/06-the-money-decisions-in-plain-language`
- **Date:** 6 October 2026
- **Status:** Operational. Explains, in non-accounting language, seven decisions
  that were blocking work, and records what was decided and on whose authority.
- **Authority:** The owner read the blocking list in
  `03-handover-what-is-left.md` §2 and instructed: *"im not finance person so i
  want you to either explain in simple layman language all this or make decision
  your self."* That is an explicit delegation, and it is why these are now
  decisions rather than open questions. Recorded as `DEC-020` to `DEC-026` in
  `.kiya/AI-DECISIONS.md`.
- **Supersedes nothing.** It closes six of the seven blocking items in
  `03-handover-what-is-left.md` §2.1 and two of the five questions in `OQ-024`.

---

## 0. How to read this, and the one rule I held to

Each decision below is written three times over: **the question in ordinary
words**, **a worked example with real numbers**, and **what was decided and
why**. You do not need any accounting to follow the examples.

**The rule I held to while deciding for you:** every one of these is reversible
by changing a setting, not by rewriting the system. Where I had to pick a
default, I picked the one that is standard practice *and* put the choice in a
field you can change. Deciding on somebody else's behalf is only acceptable if
they can undo it cheaply, so that is how each one is built.

Two of the seven are **already built and proven by automated checks** as of
today. The rest are decided, which unblocks the build.

| | What it is about | State |
| --- | --- | --- |
| **DEC-020** | What a supplier's bill adds up to | **Built and proven** |
| **DEC-021** | Where the tax you charge is held | **Built and proven** |
| **DEC-022** | What "Paid" means | Decided — unblocks `W1` |
| **DEC-023** | What your stock cost when you sell it | Decided — unblocks `W2` |
| **DEC-024** | Whether we calculate payroll tax | Decided — sizes `W3` |
| **DEC-025** | Where your real master data comes from | Decided — becomes `W6` |
| **DEC-026** | What we call things in HR | Decided — already in effect |

---

## 1. `DEC-020` — What a supplier's bill adds up to

*Closes `D2`. Built today.*

### The question in ordinary words

A supplier sends you a bill. It lists the goods, then a delivery charge, then
tax. Our system had somewhere to type all three — but it never added them up,
so the invoice had no total at all. The question was: **is "the total" the goods
only, or everything on the bill?**

### The worked example

A supplier bills you:

```
4 raw coils  at 2,000      8,000
2 fittings   at 1,000      2,000
                          ------
goods                     10,000
delivery charge              750
tax                        1,800
                          ------
you pay                   12,550
```

If the total were the goods only, it would read **10,000**. But 12,550 is what
leaves your bank account.

### What was decided, and why

**The total is 12,550 — everything printed on the supplier's bill.**

This one is not really a judgement call once it is phrased that way. The number
the system stores as "what we owe this supplier" has to be the number we will
actually pay them, or the payment will never match the bill and someone will
spend a morning finding out why.

**One related thing I deliberately did *not* decide.** Where that 750 delivery
charge lands in the accounts — treated as a cost of this month, or added to the
cost of the goods in the warehouse so it comes out of profit only when you sell
them — is a separate question. It changes your profit figure; it does not change
the 12,550. So the total is built and that question stays open as **`OQ-025`**,
to be answered when the purchase side starts posting to the accounts (`W7`).

### Also decided here: we keep the supplier's tax figure, we do not recalculate it

On an invoice you send a customer, *we* work out the tax. On a bill you
*receive*, the tax is already printed on the supplier's document — and that is
the figure that belongs in your books, even if our own calculation would have
produced something slightly different. So the system records what they billed.
A check proves this: it enters a deliberately odd tax figure of 1,733.41 against
a template that would have produced 1,800, and asserts the 1,733.41 survives.

If their figure looks wrong, that is a conversation with the supplier, not
something the software should quietly paper over.

### Proven by

```
A supplier's bill totals goods, freight and tax
   PINV: 10000 + 750 freight + 1800 tax = 12550.0

A supplier's tax figure is recorded, not recalculated
   PINV: kept the billed 1733.41, total 11733.41
```

### Changing it later

The three things that add into the total are named in one place, in
`pricing/totals.py` — a list called `additions`. Removing the delivery charge
from the total is deleting one word.

---

## 2. `DEC-021` — Where the tax you charge is held

*Closes `D3`, which the requirements marked CRITICAL and BLOCKING (`OQ-005`).
Built today.*

### The question in ordinary words

When you add tax to a customer's invoice, **that money was never yours.** You
collect it from the customer and later hand it to the tax authority. You are a
middleman holding it.

The system was putting that tax into a bucket called **"Round Off"** — a bucket
meant for one-rupee rounding differences. That was deliberate and labelled as a
placeholder, because nobody had told me which bucket it should go in. But it was
wrong, and it was wrong in a way that gets worse every month.

### The worked example

You invoice a customer 1,000 for goods and add 18% tax:

```
goods                1,000
tax at 18%             180
                     -----
customer pays        1,180
```

**Your income from that sale is 1,000, not 1,180.** The 180 is a debt you owe
the government.

Before today the system recorded the 180 under "Round Off", an expenses
heading. On a year of sales that is a growing pile of money sitting in the wrong
place — so your accounts would show a tax bill you cannot explain and a
rounding figure nobody believes.

### What was decided, and why

**Tax charged to a customer goes to a liability account — a "money I owe" bucket
— called Output Tax Payable. Tax you pay a supplier goes to an asset account —
"money owed back to me" — called Input Tax Credit.**

Both accounts already existed in every company's chart of accounts; nothing was
pointing at them. Now:

- Every company has two new settings, **Default Output Tax Account** and
  **Default Input Tax Account**, filled in automatically.
- Each tax component on a tax template can **name its own account**, which
  matters when two parts of one tax go to two different authorities. Left blank,
  it uses the company default.
- Tax is now posted **one line per component**, not as a single lump. If an
  invoice carries two taxes, the accounts show two taxes.
- **An invoice carrying tax with nowhere to post it is refused.** It is not
  parked somewhere plausible. This is the same rule the system already applies
  to the customer's debt: a wrong account is much harder to find three months
  later than a blocked invoice is right now.

Why a liability and not income: because tax collected is not income. Putting it
in income would overstate your profit by the entire amount of tax you have
collected, and you would be taxed on money that was already tax. A check now
asserts the account's type is **Liability**, so a chart that files it under
income fails the test rather than quietly producing a wrong profit.

### Proven by

```
A company's tax accounts are a liability and an asset
   output Output Tax Payable (Liability), input Input Tax Credit (Asset)

Tax posts to a tax account, never to round-off
   SINV: 180 tax in 2 lines to Output Tax Payable, nothing to round-off

A tax component may name the account it posts to
   SINV: 100 to Input Tax Credit, 100 to Output Tax Payable

Tax with nowhere to post is refused, not guessed
   refused: Acceptance Tax Unrouted of 60.00 has no account to post to.
```

The second check asserts the new behaviour **and the absence of the old one** in
one go, so if anyone ever reinstates the round-off placeholder, the suite fails
instead of passing quietly.

### Changing it later

Point the two company settings at different accounts, or name an account on the
tax template row. No code.

---

## 3. `DEC-022` — What "Paid" means

*Closes `D4`. Decided, not yet built — this unblocks `W1`, the largest remaining
gap in the system.*

### The question in ordinary words

Today an invoice can be marked "Paid" with **no record of any money arriving.**
Nothing is wrong with the button; what is missing is everything behind it. To
build it, five ordinary situations need a rule each, and nobody had given me
one. Here they are with the rule I chose.

### The five situations

**1. A customer pays part of the bill.**

```
invoice                   50,000
they send                 20,000
                          ------
still owed                30,000
```

> **Decided:** allowed. The invoice shows **30,000 outstanding** and its status
> becomes **Partly Paid** — a status distinct from both Unpaid and Paid, so
> nobody mistakes a part payment for a settled bill.

**2. One payment covers several invoices.** A customer sends 75,000 covering
three invoices of 50,000, 20,000 and 5,000.

> **Decided:** allowed, and this is the normal case rather than the exception.
> One receipt is split across the three invoices, and you choose the split.
> This is what the Allocations table on a Payment Entry is for.

**3. They pay more than they owe.** The invoice is 50,000 and they send 60,000.

> **Decided:** the system will **refuse to allocate more than an invoice
> actually owes**. The extra 10,000 does not vanish and does not inflate the
> invoice — it stays on the payment as **unallocated**, which is money you are
> holding for that customer. It is a debt to them, not a sale. You apply it to
> their next invoice.
>
> This also covers **advances**: a payment that arrives before any invoice is
> simply a payment with nothing allocated yet.

**4. A rounding residue is left behind.** They owed 50,000 and sent 49,999.60.
Forty paise. Nobody is chasing forty paise, but the invoice will never show as
paid.

> **Decided:** the company gets a **write-off tolerance**, set by you and
> defaulting to **one unit of your currency**. A residue inside the tolerance
> can be written off to the Round Off account — and this is the one legitimate
> use of that account, which is exactly what it exists for.
>
> **It is never automatic.** Somebody presses a button, and the write-off is
> recorded against their name. Automatic write-offs are how small amounts of
> money leave a business without anyone noticing.

**5. What does the invoice say, and when?**

> **Decided:** `outstanding = grand total − everything allocated to it`,
> calculated from the payments, **never stored as a separate running figure.**
>
> This is the same principle the whole system already uses for account balances
> and for leave days, and it is the single most important one in here. A stored
> total is a second copy of the truth. The moment it disagrees with the payments
> behind it, nothing can tell you which one is right. Derive it, and that can
> never happen.

### One thing I found while deciding this

The Payment Entry record is built with plain text boxes where it needs proper
links: the customer, the payment method, the bank account, and the invoice each
allocation points at are all free text today. So nothing stops a payment
referring to a customer who does not exist, or to an invoice that was deleted.
That has to be fixed as part of `W1` — I am noting it here so it is on the
record before the work starts, not discovered during it.

### Changing it later

The tolerance is a company setting. The rules on part payment, over-payment and
advances are the standard ones; they are what the approved baseline (`CD-001`,
`DEC-012`) already tells me to use where the BRD is silent, which is why I am
comfortable deciding them rather than guessing.

---

## 4. `DEC-023` — What your stock cost when you sell it

*Closes `D5`, marked CRITICAL (`OQ-007`). Decided, not yet built — unblocks
`W2`.*

### The question in ordinary words

You buy the same item twice at different prices. Then you sell some. **What did
the ones you sold cost you?** There is no single true answer, which is why it
needs a decision — and the answer changes your reported profit.

### The worked example

```
January    bought 10 coils at 100 each  = 1,000
February   bought 10 coils at 120 each  = 1,200
March      sold 5 coils
```

What did those five cost?

| Method | Reasoning | Cost of the 5 | Stock left |
| --- | --- | --- | --- |
| **First in, first out (FIFO)** | The oldest ones went out first | 5 × 100 = **500** | 1,700 |
| **Weighted average** | Blend everything: 2,200 ÷ 20 = 110 | 5 × 110 = **550** | 1,650 |
| **Last in, first out (LIFO)** | The newest ones went out first | 5 × 120 = **600** | 1,600 |

Same warehouse, same sale, three different profit figures.

### What was decided, and why

**FIFO — first in, first out — as the default. Weighted average available per
item. LIFO not offered at all.**

LIFO is not offered because it is **not permitted**. India's accounting standard
on inventories, Ind AS 2, lists the methods you may use, and LIFO is not among
them. Paragraph 25, from the Institute of Chartered Accountants of India's own
published text:

> *"The cost of inventories, other than those dealt with in paragraph 23, shall
> be assigned by using the first-in, first-out (FIFO) or weighted average cost
> formula."*

So offering LIFO would be offering a setting that puts the client in breach.
That is not a feature, and it is not going in.

Between the two that *are* allowed, **FIFO** is the default because for physical
goods that are bought and stored in identifiable lots — which is what a knitting
or induction business handles — it matches what actually leaves the shelf. It is
also the method a stock count can be reconciled against, because each remaining
lot still has its own cost.

**Why the choice is per item and not one setting for the whole company.** The
same paragraph 25 continues:

> *"An entity shall use the same cost formula for all inventories having a
> similar nature and use to the entity. For inventories with a different nature
> or use, different cost formulas may be justified."*

So the standard itself requires consistency **within a kind of stock**, not
across all stock. The `valuation_method` field already exists on the Item record;
it will become a dropdown of exactly two choices rather than the free text box
it is today — a text box is how you end up with "fifo", "FIFO " and "Fifo" as
three different methods.

Two further points the standard settles for us:

- **Serial-numbered items are costed individually.** Paragraph 23 requires
  specific identification for items that are *"not ordinarily interchangeable"*.
  A serial number is precisely the declaration that one unit is not
  interchangeable with another, so a serial-tracked item carries its own cost.
- **Stock is counted per item per warehouse.** Not per bin. In this system a Bin
  is already an *address* — aisle, rack, shelf — which tells you where to walk,
  not what you own. It stays that way, and quantity and value are **derived from
  a ledger of stock movements**, the same pattern as the accounts and the leave
  days.

### One thing the standard requires that we are not building yet

Ind AS 2 also requires stock to be carried at **the lower of what it cost and
what it can actually be sold for**. If 1,700 of yarn can now only fetch 1,200,
the standard says write it down to 1,200.

Nothing in the system does this, and I am not going to decide a write-down
policy — it needs judgement about your market, per item. **Raised as `OQ-026`.**
I am recording it rather than leaving it out, because a stock system that can
only ever value stock upward is a known gap, not an unknown one.

### Changing it later

Change the dropdown on an item, or the company default. Costing methods cannot
be changed retrospectively without restating past figures — but that is the
standard's constraint, not the software's.

---

## 5. `DEC-024` — Whether we calculate payroll tax

*Closes `D6` and `OQ-024` item 4. This is the decision that sizes the remaining
HR work.*

### The question in ordinary words

A payslip has two halves. The first is **what the person earned** — salary,
overtime, allowances, minus leave without pay. The second is **what the law
takes out** — income tax, provident fund, state professional tax, and so on.

The first half is arithmetic you can check on paper. The second half is
legislation, it changes every year, and it differs by state.

### What was decided

**Version one builds the first half completely and does not attempt the second.**

Concretely, version one will:

- let you define pay components — basic, HRA, overtime, any deduction
- build a salary structure from them and assign it to people
- produce a payslip showing gross pay, deductions and net pay
- feed leave and attendance into it, so unpaid leave reduces pay automatically
- post the payroll to the accounts as a proper journal entry
- **export a file for your payroll bureau or accountant**

It will **not** calculate income tax slabs, exemption declarations and proofs,
provident fund, employee state insurance, professional tax, or gratuity.

### Why — and this is the part worth reading

Not because it is hard. Because **getting it wrong is your client's legal
problem, not a missing feature in our software.**

Professional tax alone shows why. It is levied by each **state**, under
Article 276 of the Constitution of India — not nationally. Each state that
levies it sets its own salary bands, its own amounts, its own registration,
filing dates and exemptions. Maharashtra's bands differ from Tamil Nadu's.
Maharashtra has different bands for men and women. **Delhi, Haryana and Uttar
Pradesh do not levy it at all.** So "professional tax" is not one rule to
implement; it is a different rule per state, each changing on its own schedule.

Income tax is worse: the slabs move with each year's Finance Act, and a payroll
system that is correct in April is wrong the following April unless somebody is
paid to track legislation and ship updates. That is a subscription service with
an ongoing legal obligation attached, not a module you finish.

Meanwhile the bureau or chartered accountant your client already uses does this
for a living, carries the professional liability for it, and keeps up with the
changes. Handing them a clean file is a better outcome for the client than our
best guess at this year's slabs.

**So: we compute pay, we post the accounting, we hand over the file.**

### What this does not foreclose

The pay-component model is deliberately the same shape a statutory engine would
need. Adding statutory calculation later means adding a calculation behind an
existing component — it does not mean rebuilding the salary structure, the
payslip or the posting. If you later sell into a market that demands it, or hire
someone to own the legislation tracking, the road is open.

### What I am explicitly not deciding

Whether the client **accepts** this. It is a scope reduction against
`FR-HR-004` and `FR-HR-005`, and they must be told in those words, early, in the
requirements session — not discovered at go-live. The honest sentence is:

> *"The system will calculate what each person is paid and produce the
> accounting entry. It will hand statutory deductions to your payroll bureau,
> because professional tax is set state by state and income tax changes every
> year, and we are not going to make you depend on us getting that right."*

---

## 6. `DEC-025` — Where your real master data comes from

*Closes `D1`, by changing it from a decision into a task.*

### The question in ordinary words

The system holds sample data I invented — units of measure, item categories,
sales territories, customer groups, a price list — so that there was something
to demonstrate with. **Invented masters cannot carry real transactions.** Your
actual categories are yours; nobody else can write them.

### What I found while looking at this

Something that changes the answer. The units, item categories, territories,
customer groups and price lists are **site-wide, not per-company.** I had
previously described them as confined to the demo company; they are not. So
putting a real client's company onto the same site as the demo means the real
company's dropdowns show my invented categories.

### What was decided

**The sample masters belong to the demo site, and only to the demo site. A real
client's site starts empty of them and is loaded with the client's own, by
import.**

Which means D1 is no longer a decision waiting on you. It is `W6`, a build task
I can do: a spreadsheet template per master, an importer that refuses a row it
cannot place rather than inventing a parent for it, and a report of what went in.

You still have to supply the lists — nobody else knows your categories. But you
supply them as a filled-in spreadsheet, not as answers to my questions, and that
is a much smaller ask.

---

## 7. `DEC-026` — What we call things in HR

*Closes `OQ-024` items 1 and 2. Already in effect.*

### The question in ordinary words

There is an open-source HR system, Frappe HR, under a licence (GPL-3) that would
force us to publish our own source code if we copied from it. I studied **what
it does and in what order a user does it** — which is not protected — and read
**none of its code**, which is.

Two questions were left open from that study, and they are now decided.

**Does KNIT 360 use the same words?** Yes, for ordinary ones. "Leave
Application", "Holiday List", "Leave Type" are plain HR English and were in use
long before any software. **But we do not take the arrangement wholesale.** That
system has around 157 record types; KNIT 360's leave module has **seven**, which
is what the BRD's requirements actually need. Using common vocabulary is not
copying; reproducing someone's whole structure starts to look like it, so we
don't.

**What is the leave approval sequence?** Their documentation never stated it, and
`AGENTS.md` forbids me inventing requirements. So the sequence KNIT 360 uses —
Draft, Pending Approval, Approved, with Rejected returning to Draft — is marked
**BRD-DERIVED** and built on the approved baseline (`CD-001`, `DEC-012`) that
says to use standard practice where the BRD is silent. It is a reasonable
reading, labelled as a reading, and changeable in one file.

One property of it is worth knowing because it protects you: **Rejected counts
as a draft.** A refused leave request can never have touched the leave balance,
by construction rather than by care. A check proves it.

---

## 8. What is still genuinely not mine to decide

I would rather be short and clear about these than pad the list above.

| | Why it stays with you |
| --- | --- |
| **`OQ-025`** Whether a supplier's delivery charge is this month's cost or part of the cost of the goods | Both are accepted practice. It changes your reported profit, so it is your accountant's call. Does not block anything until `W7`. |
| **`OQ-026`** When stock is written down because it can no longer be sold for what it cost | Ind AS 2 requires it; the judgement of *when* is about your market, item by item. |
| **`D7`–`D14`** Who approves what and at what value; what the system emails and to whom; supplier scorecards; warranty terms; which other systems we talk to | These are your organisation's rules. There is no standard practice to fall back on — "a purchase order over 50,000 needs the director" is a fact about your company, and inventing it would be inventing a requirement. |
| **HR beyond the BRD's seven requirements** — expense claims, recruitment, training | Classified **TBD**, not out of scope, per `DEC-009`. Not in version one. Expense claims are the likeliest early ask. |
| **`Y1`** The licence position | I have set out the reasoning and the suite proves no GPL code is installed. **I am not a lawyer.** A commercial product needs a real opinion, and the question of whether reimplementing from observation is safe is one the Free Software Foundation's own FAQ does not answer. |
| **`Y5`** Whether any of this matches how your business actually works | 116 automated checks prove the system does what it was built to do. They cannot tell you it was built to do the right thing. Only someone who does the job can. |

---

## 9. Where this leaves the system

```
                        before today     after today
automated checks        110              116
  structural             49               49
  runtime                61               67
proven requirements      10               12
covered requirements     69 of 238        69 of 238  (29.0%)
BRD modules started      15 of 28         15 of 28
blocking decisions        6                2   (OQ-025, OQ-026 — neither blocks)
```

Coverage did not move, and it should not have: both requirements touched today
were already *modelled*. What changed is that two of them are now **proven** —
Tax & Statutory Compliance has its first proven requirement, and Accounts
Payable has one. That is the gap between a drawing and a working thing, and it
is the only figure in the report worth arguing about.

Three large pieces of work are now unblocked and can be built in order:

1. **`W1` Payment Entry** — `DEC-022`. The largest single gap in the system.
2. **`W2` Stock ledger** — `DEC-023`. Inventory, Warehouse and MRP are forms
   until this exists.
3. **`W3` HR attendance, then payroll** — `DEC-024` fixes the size.

---

## 10. Sources

Decisions in this document that rest on something other than ordinary practice
cite it here, so the reasoning can be checked rather than taken on trust.

- Ind AS 2 *Inventories*, paragraphs 23, 25, 26 and 27 — permitted cost
  formulas, consistency within a class of inventory, and specific
  identification. Read from the Institute of Chartered Accountants of India's
  own published text: [resource.cdn.icai.org/23698IndAS-2.pdf](https://resource.cdn.icai.org/23698IndAS-2.pdf)
- Ind AS 2 paragraph 28 onward — lower of cost and net realisable value. Same
  source. The basis for `OQ-026`.
- Professional tax as a state levy under Article 276 of the Constitution of
  India, with state-by-state bands and some states not levying it:
  [en.wikipedia.org/wiki/Professional_Tax](https://en.wikipedia.org/wiki/Professional_Tax),
  corroborated by [pkcindia.com state-wise guide](https://www.pkcindia.com/blog/professional-tax-in-india-state-wise-rates-applicability-compliance-guide/)
  and [lkslaw.com framework note](https://employmentlaw.lkslaw.com/professional-tax).
  The basis for `DEC-024`.
- `CD-001` / `DEC-012` — the approved decision to use standard ERP behaviour as
  the baseline where the BRD is silent. The authority for `DEC-022` and
  `DEC-026` rather than my own preference.
- `DEC-009` — unspecified functionality is TBD, never automatically
  out of scope. Why §8 says "not in version one" and not "out of scope".
