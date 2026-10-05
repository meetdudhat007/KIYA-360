# KNIT 360 — Demonstration Script

## Document control

- **Document ID:** `03-guides/02-demonstration-script`
- **Date:** 5 October 2026
- **Status:** Operational. A script for showing the product as it stands today.
- **Audience:** Whoever is presenting. Not a customer handout.

Every claim in this script is one the running system can be made to perform. The
things it cannot do are in §6, and the script is built to avoid walking into
them by accident rather than to hide them.

---

## 1. Before anyone is in the room

### 1.1 Start it

```bash
docker compose -f infrastructure/docker-compose.dev.yml up -d
```

Give it about ninety seconds. Then confirm it answers:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: knit360.localhost" http://localhost:8000/knit360
```

A `200` or a `301` means it is up.

### 1.2 Make sure the data is there

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.demo.seed'
```

Safe to run twice. It will say the pipeline is already built if it is.

### 1.3 Make sure the test data is *not* there

The acceptance run creates documents, and the headline figures count documents
across every company. If anyone has run the tests recently, clear them:

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.acceptance.cleanup'
```

The home page should read **Open Leads 5**, not a number in the dozens. If it
reads in the dozens, the line above has not been run.

### 1.4 Open two browser tabs, signed in

- Tab 1: `http://knit360.localhost:8000/knit360` — the simple screen
- Tab 2: `http://knit360.localhost:8000/app/knit-360` — the full system

Use the host name `knit360.localhost`, never `localhost:8000`. If an ERPNext
instance is also running locally, the two will sign each other out, because a
browser stores a sign-in against the host name and ignores the port.

### 1.5 Know the answer to the licence question

It will be asked, usually early.

> KNIT 360 is built on Frappe Framework, which is MIT licensed — that licence
> puts no obligation on what we build with it. ERPNext is a separate
> application under GPL-3, and we have not installed it and have taken no code
> from it. You can verify that: the installed applications are `frappe` and
> `knit360_core`, and nothing else.

To show it rather than say it:

```bash
docker exec knit-bench bash -lc 'cat /home/frappe/frappe-bench/sites/apps.txt'
```

It prints two lines. The acceptance suite also asserts this on every run, so a
regression would fail a test.

---

## 2. The shape of the demonstration

Forty minutes, five movements. The order matters: it opens on something that
looks finished, spends the middle on what is genuinely strong, and arrives at
the gaps on its own terms rather than being driven there.

| | Movement | Minutes | What it proves |
| --- | --- | --- | --- |
| 1 | The morning dashboard | 5 | It is a real product, not a prototype |
| 2 | A deal, start to finish | 12 | The documents connect; nothing is re-typed |
| 3 | The system refuses to be wrong | 8 | **This is the differentiator** |
| 4 | The books | 7 | The money is sound |
| 5 | It is built, not assembled | 5 | Evidence, and the licence answer |
| | Questions | 3 | |

---

## 3. Movement by movement

### Movement 1 — The morning dashboard (5 min)

**Open on:** Tab 2, the full system home page.

Say: *"This is what someone running the business opens at nine in the morning."*

Point at the four headline figures, then the four charts. Let them read it.

Then open the sidebar and scroll it slowly: CRM, Sales, Finance, Tax,
Procurement, Supplier Management, Inventory, Warehouse, MRP, Manufacturing,
Quality, Asset Management, Maintenance, Platform.

Say: *"Sixteen areas, sixty-five record types, covering fourteen of the BRD's
twenty-eight modules."*

**Be ready for the obvious follow-up: "what about the other fourteen?"** The
answer is that four of them — workflow, integration, mobile and audit — are
served by the framework rather than built, and the remaining ten are not
started. Marketing, Customer Service, Projects, Logistics, HR and E-Commerce are
the notable ones. Say it plainly; the list is in the handover document and
someone will ask for it.

**Do not** click into Users, Website, Tools, Integrations or Build. They are the
framework's own screens and are not part of the product.

---

### Movement 2 — A deal, start to finish (12 min)

**Switch to:** Tab 1, the simple screen.

Say: *"The same data, but this is what a salesperson gets. One job, three
stages, works on a phone."*

Walk the strip: Leads, Opportunities, Quotations.

**Then do this live:**

1. Add a lead. Use a real name from the room if you can — it lands well.
2. Open it. Read the status sentence out loud: it explains in plain English what
   the status means and what to do next.
3. Press **Contacted**. Then **Qualified**.
4. Press **Convert**. Say: *"That one action created the customer record and the
   opportunity. Nobody re-typed a company name, so nothing can disagree later."*
5. Open the opportunity, move it to **Proposal Sent**.
6. Press **Create Quotation**.
7. Add two lines. Put a discount percentage on the second one.
8. Point at the amount column and the grand total. Say: *"Those are calculated.
   You cannot type them — so a total can never disagree with its own lines."*

**The phone moment.** Narrow the browser window until it is phone-width, or open
it on an actual phone. The layout flips: the list fills the screen, tapping a row
replaces it with the record, and a "Back to the list" control appears. Every
tappable thing is at least 44 pixels, which is Apple's published minimum and the
strictest level of the accessibility standard.

---

### Movement 3 — The system refuses to be wrong (8 min)

This is the part worth rehearsing. It is what the product has that a generic ERP
does not, and it demonstrates best as a series of attempts that fail.

**Attempt 1 — skip a step.**

On a fresh lead, point out that the only buttons offered are *Contacted*,
*Disqualified* and *Lost*. There is no *Converted*.

Say: *"You cannot convert a lead you have not qualified. Not because someone
remembered to check — because the system was never willing to offer it."*

**Attempt 2 — edit a posted invoice.**

Open a posted invoice from the sample data. Try to change a figure. It refuses.

Say: *"It has hit the ledger. You reverse it, you do not rub it out. The books
keep what they once said."*

**Attempt 3 — the technical back door.**

Open a draft Journal Entry in the full system and press the framework's own
**Submit** button. It refuses, and names the reason.

Say: *"That is the framework's button, not ours. If it worked, it would post to
the ledger without the business status changing, and the document and the books
would then disagree. So we closed it."*

**Attempt 4 — an unbalanced entry.**

Create a Journal Entry with debits of 100 and credits of 90. It refuses before
saving.

Say: *"An unbalanced entry is never written. Not written and flagged — not
written at all."*

**Then land the point:**

> *"Every one of those refusals is a line in a test that runs on every change.
> Ninety-four checks: forty-seven on the definitions, forty-seven that drive the
> running system. If someone removes a guard, a test goes red the same day."*

---

### Movement 4 — The books (7 min)

**Back to:** Tab 2, Finance.

Show the chart of accounts. Forty accounts, five roots, built automatically when
a company is created.

Say: *"Group accounts are headings and hold nothing. Postings go to leaves. Try
to post to a heading and it refuses, so a group's balance is always exactly the
sum of what is under it."*

Open the trial balance. Point at the totals: debits equal credits.

Then show a reversal:

1. Post a small Journal Entry.
2. Show the two ledger entries it wrote.
3. Cancel it.
4. Show that there are now four entries, not zero, and that the net effect is
   nil.

Say: *"Nothing is deleted. The original is still there, the reversal is beside
it, and the history is intact."*

---

### Movement 5 — It is built, not assembled (5 min)

Go to a terminal and run the acceptance suite in front of them:

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.acceptance.run_and_clean'
```

It takes about a minute and prints a line per check. It ends with `47/47 checks
passed` and then removes its own data.

Say: *"That is not a screenshot. It just inserted documents, moved them through
their lifecycles, posted to the ledger, tried to break the guards, and confirmed
each one held."*

Then the licence answer from §1.5.

---

## 4. If you only have ten minutes

Movement 2, steps 1–8. Then Movement 3, attempts 1 and 3. Then the test run.

That is the whole argument: the documents connect, the system refuses to be
wrong, and there is evidence.

---

## 5. Questions you will be asked

**"How is this different from ERPNext?"**
> ERPNext lets you set a status and trusts you. KNIT 360 defines what each
> document is allowed to do at each point in its life and offers nothing else.
> Twenty-three of those lifecycle definitions, every one tested. It is a
> narrower system on purpose.

**"How much is finished?"**
> The spine of Customer-to-Cash runs end to end and the ledger underneath it is
> sound. Sixty-five record types are modelled against the BRD's twenty-eight
> modules. Taking payments, moving stock and HR are not built yet, and §6 is the
> honest list.

**"Can we see our own data in it?"**
> Not today. Data import is one of the named gaps. It is a known piece of work,
> not a surprise.

**"What happens when we grow?"**
> It is multi-company already — a second company gets its own chart of accounts
> automatically, with accounts suffixed by the company's initials so they cannot
> be confused.

**"Who else uses it?"**
> Nobody yet. Say so. The next question is usually what it would take to be
> first, and that is a better conversation than a dodge.

---

## 6. Do not demonstrate these

Not because they look bad — because they are **not built**, and improvising over
a gap is how a demonstration loses a room.

| Avoid | Why | If asked |
| --- | --- | --- |
| Marking an invoice **Paid** | Payment Entry does not post to the ledger or reduce the outstanding figure. The status would move and the money would not. | *"Taking payment is the next piece of work. I would rather show you an outstanding invoice that is true than a paid one that is not."* |
| Stock levels, Bin quantities | Delivery Note and Goods Receipt record quantities but do not move stock. Bin holds no live figure. | *"Stock movement is scheduled, not built."* |
| Printing a quotation **to a customer** | It prints and makes a PDF, but with no letterhead and no layout — it looks like a system printout. Emailing is unconfigured. | *"It prints today; what it does not have yet is your letterhead and layout. Designing that is a known, unblocked piece of work."* |
| The tax figure on an invoice | It calculates correctly but posts to the round-off account as a deliberate placeholder. | *"The calculation is right; where it posts is waiting on the tax masters."* |
| Anything in HR | Not started. | *"Deferred on purpose — we are doing it next, against a reference you are providing."* |
| Users, Website, Tools, Build | Framework screens, not ours. | Just do not open them. |

---

## 7. The one-paragraph version

> KNIT 360 is a CRM and ERP built on Frappe, an MIT-licensed framework, with no
> ERPNext code in it. Sixty-five record types cover fourteen of the BRD's
> twenty-eight modules. What makes it different is that every important document has a
> defined life, and the system offers only the moves that life allows — you
> cannot convert an unqualified lead, edit a posted invoice, or post an
> unbalanced entry, because those options are never on the screen. Ninety-four
> automated checks hold those rules in place. Customer-to-Cash runs end to end
> on a double-entry ledger that balances and reverses rather than deletes.
> Taking payments, moving stock and HR are the next three pieces of work.
