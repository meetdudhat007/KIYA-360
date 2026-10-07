# KNIT 360 — What Is Left, and Who Has To Do It

## Document control

- **Document ID:** `03-guides/03-handover-what-is-left`
- **Date:** 5 October 2026
- **Status:** Handover. Divides the remaining work by **who can do it**, not by module.
- **Method:** Each item was checked against the running system or the repository
  before being listed. Nothing here is an estimate dressed as a fact, and where a
  number is uncertain this document says so.

---

## 1. The honest summary

What exists and is proven:

| | |
| --- | --- |
| Record types built | 72 parent, 22 child — 94 in total |
| BRD modules with record types built | **15 of 28** |
| Lifecycle definitions | 25 |
| Automated checks | **140** — 49 structural, 91 runtime |
| Last full run | 49/49 and 91/91, 7 October 2026 |
| BRD modules with nothing built yet | **13 of 28** (listed below) |
| Flows running end to end | 1 of 3 (Customer-to-Cash) |

The thirteen BRD modules that have **no record types at all** are: Marketing (4),
Customer Service (5), Logistics & Transportation (15), Projects (16),
E-Commerce (20), Document Management (21), Business Intelligence (22), EPM /
Budget / Forecast (23), Workflow & Approvals (24), AI & Automation (25),
Integration & API (26), Mobile Application (27) and Audit (28).

HR & Payroll (19) is partially built: leave management is complete and proven;
attendance, payroll, appraisal and recruitment are not started.

Some of those are intended to be served by Frappe's own facilities rather than
built — Workflow, Integration, Mobile and Audit were assigned that way in the
hybrid-platform decision. The rest are genuinely not started.

What that does **not** mean: the record types exist and are correctly shaped, but
most of them are forms rather than working processes. The gap between "modelled"
and "working" is most of the remaining effort, and §4 is where it is listed.

---

## 2. Only you can decide these

I am instructed not to invent requirements, and `AGENTS.md` forbids it. Each of
these is a business decision. I can build any of them within about a day of a
decision; I cannot make the decision.

### 2.1 Blocking — all six are now closed

**On 6 October 2026 the owner delegated these six decisions** — *"im not finance
person so i want you to either explain in simple layman language all this or make
decision your self."* They are decided and recorded as `DEC-020` to `DEC-026`,
and each is explained in non-accounting language, with worked examples, in
`06-the-money-decisions-in-plain-language.md`.

Two of them are not merely decided but **built and proven** by automated checks.

| # | Was | Now | Decision |
| --- | --- | --- | --- |
| **D1** | Your real master data | **Closed.** Sample masters belong to the demo site only; a client site is loaded by import. No longer a decision — it is build task `W6`. | `DEC-025` |
| **D2** | Does freight and statutory tax belong in a Supplier Invoice total? | **Closed and built.** Both are inside: the total is the whole amount payable. The supplier's own tax figure is recorded, not recomputed. | `DEC-020` |
| **D3** | Which tax accounts does tax post to? (`OQ-005`, CRITICAL) | **Closed and built.** Output tax to a liability, input tax to an asset, one line per component, a per-component account override, and a refusal where neither resolves. The round-off placeholder is gone. | `DEC-021` |
| **D4** | What does "Paid" mean? | **Closed.** Part payment with its own status, allocation across invoices, over-payment held as an advance, derived outstanding, and a manual write-off inside a company tolerance. Unblocks `W1`. | `DEC-022` |
| **D5** | Stock valuation (`OQ-007`, CRITICAL) | **Closed.** FIFO default, weighted average per item, LIFO not offered — Ind AS 2 ¶25 permits only the first two. Balance derived per item per warehouse; Bin stays an address. Unblocks `W2`. | `DEC-023` |
| **D6** | The HR reference | **Closed.** Leave is built. Statutory payroll is out of version one; pay, posting and an export for the client's payroll provider are in. Sizes `W3`. | `DEC-024` |

**Two new open questions came out of deciding these, and neither blocks
anything:** `OQ-025`, whether a supplier's freight is expensed or added to the
cost of the goods — needed only when `W7` posts the buying side; and `OQ-026`,
when stock is written down to net realisable value, which Ind AS 2 requires and
nothing yet does.

### 2.2 Important but not blocking

| # | Decision | Where it is recorded |
| --- | --- | --- |
| D7 | Approval matrices — who approves what, at what value, and what happens on escalation | `OQ-003` |
| D8 | Notification triggers and templates — what the system emails, to whom, when | `OQ-004` |
| D9 | Supplier scorecard measures | `OQ-010` |
| D10 | Warranty terms, expiry and claim handling | `OQ-011` |
| D11 | Which systems KNIT 360 must talk to | `OQ-012` |
| D12 | Measurable performance targets | `OQ-015` |
| D13 | Which of the 14 capabilities the BRD never mentions enter scope | `OQ-023`, listed in doc 44 |
| D14 | How close to ERPNext's feature set you are actually aiming | `OQ-022` |

> **On `OQ-023`:** three of those fourteen deserve attention ahead of the rest
> for structural reasons rather than commercial ones. **Credit and debit notes**
> — the BRD names Returns and Credit Memos as requirements but never defines the
> accounting instruments, so a return cannot currently be settled. **Warranty** —
> BRD §6.3 names it as a stage of a core flow, so it is a hole in a required flow
> rather than an extra. **Data migration** — no client can go live without it.

---

## 3. Only you can do these

Not decisions — actions outside what I can reach.

| # | Task | Why it has to be you |
| --- | --- | --- |
| **Y1** | **Legal sign-off on the licence position.** | I have set out the reasoning — Frappe is MIT, ERPNext is GPL-3, we installed and copied neither — and the acceptance suite asserts ERPNext is absent on every run. **I am not a lawyer and this is not legal advice.** A commercial product needs a real opinion. |
| **Y2** | **Hosting, domain, TLS, backups.** | Everything so far runs in Docker on one machine. There is no production environment, no backup schedule and no restore test. |
| **Y3** | **The administrator password.** | It is not recorded anywhere in the repository. I did not guess it and I did not change it. You will need it to sign in during the demonstration. |
| **Y4** | **The 238 BRD requirements are every one marked "TBD — the BRD does not specify this detail."** | Until a stakeholder fills those in, "match the BRD" means building to the ERP-standard baseline agreed in CD-001. That is what has been done. It is a reasonable reading, not the specification. |
| **Y5** | **User acceptance testing by someone who does the job.** | My 140 checks prove the system does what it was built to do. They cannot tell you whether that is what your business actually needs. |
| **Y6** | **Decide what happens to the seven ERPNext reference documents** in `docs/` (`erpnext_accounting_module.md` and six others, roughly 4,200 lines). | I did not write them; they were swept into commit `2be7a50` by a `git add -A`. They are reference material about a GPL-3 product sitting in this repository. I flagged this previously and have had no answer. **This is the one item on this list I would act on soonest.** |
| **Y7** | **Delete or keep the "Kelvinotherm Induction LLP" company** on the demo site. | It predates this work and holds one lead from 23 September. Harmless, but it appears in the company dropdown during a demonstration. |

---

## 4. I can do these without you

Ordered by value. Each is a self-contained piece of work.

| # | Work | Size | Why it matters | Blocked by |
| --- | --- | --- | --- | --- |
| ~~**W1**~~ | ~~Payment Entry posting and allocation~~ | — | **Done 7 October 2026** (`DEC-029`). Receipts post, allocate across invoices, hold an overpayment as an advance, and drive the invoice's status. Outstanding is derived from the ledger. Twelve checks. | — |
| **W2** | Stock ledger — Delivery Note and Goods Receipt actually move stock | Large | Inventory, Warehouse and MRP are forms without it. Balance is derived per item per warehouse; Bin stays a storage address and holds no figure. | — (`DEC-023`) |
| **W3** | HR: attendance, then payroll, then appraisal | Medium | Leave is built and proven (`FR-HR-003`). Attendance feeds payroll; payroll ends in a Journal Entry that already works. **Sized down by `DEC-024`:** statutory computation is out of version one, so payroll is pay, posting and an export. | — |
| **W4** | Designed print formats and a letterhead | Medium | Printing and PDF already work; the output is Frappe's standard field dump. What is missing is a laid-out quotation, order and invoice carrying the client's letterhead. Nothing blocks this. | — |
| **W5** | Pricing reads from Item Price instead of being typed | Small | The masters exist and are populated; the documents ignore them. | — |
| **W6** | Data import — opening balances, customers, items | Medium | Blocks the first customer, not the tenth. | — |
| **W7** | Procure-to-Pay posting — Purchase Order and Supplier Invoice reach the ledger | Medium | The buying side totals correctly now but never reaches the books. | `OQ-025` for where freight lands |
| **W8** | Credit and debit notes | Medium | Returns cannot be settled without them. | **D13** |
| **W9** | Customer credit limit and credit hold | Small | A finance controller asks for this in the first demonstration. | **D13** |
| **W10** | Email on status change | Small | Nothing is sent by the system today. | D8 for content |
| **W11** | **Roles other than System Manager** | Medium | All 65 record types grant access to `System Manager` and nothing else, verified against the permissions table. So a salesperson cannot be given leads without also being given the power to delete the company's accounts. Acceptable for a pilot, not for a live client. | — |

**If you want one thing done next, make it W1.** It needs D4 answered first, and
D4 is four short questions about how your business handles money coming in.

---

## 5. What I found while testing, and what I did about it

Recorded because the method matters as much as the result. The 46 tests that
existed before this session all read files; none opened a database transaction.
Writing 42 that drive the running system found five real defects in a day.

| Found | Severity | Status |
| --- | --- | --- |
| Thirteen of fifteen documents with line items computed **no total at all** — including Quotation, the central document of Customer-to-Cash | **High** | **Fixed.** One shared pricing engine now serves Quotation, Sales Order, Purchase Order, Supplier Quotation and Sales Invoice. |
| Four tree masters had no naming rule, so records were named with a random hash — the first one inserted was called `b497tuqe2q` | **High** | **Fixed**, and a test now requires every record type to declare how it is named. |
| `set_items` silently discarded any column it did not recognise, so sending `rate` to a table whose column is `unit_rate` stored a priceless line **and reported success** | **High** | **Fixed.** It now refuses and names the columns that exist. |
| The web seam returned `docstatus` and `modified` — the exact framework details it exists to hide | Low | **Fixed.** The page never read them. |
| The acceptance runner counted a check that returned no evidence as a pass. One check lost its assertions to an edit and still showed green | **High** (in the harness) | **Fixed.** A check must now return evidence or it fails. |
| **Creating a company through the normal screen produced no chart of accounts.** Only the demo and test scripts built one, so setting up a real client needed a command line — and without a receivable account you cannot raise an invoice | **Blocking** | **Fixed.** A new company builds its own books on save. A check enforces it. |
| **No business status could be changed from the Desk at all.** The status field is read-only and nothing rendered a button, so Sales Order, Delivery Note, Sales Invoice, Journal Entry and the entire purchasing side had no reachable lifecycle. Only the three stages on `/knit360` could be moved | **Blocking** | **Fixed.** Every form now renders one button per legal move, asked from the engine. |
| Converting a lead existed only on `/knit360`, so a Desk user could qualify a lead and had nowhere to take it | **High** | **Fixed.** Convert and Raise Quotation are Desk buttons, sharing the web page's own rules rather than restating them. |
| A Qualified lead showed both **Converted** and **Convert to Customer + Opportunity**. The first marks it converted and creates nothing | **High** | **Fixed.** An action now declares the status it reaches, and the duplicate button is left out. |
| The form script was served from a fixed path with no content hash, so any change to it would need a hard refresh on every machine | Medium | **Fixed.** Renamed to a `.bundle.js` so Frappe's bundler hashes it. |

Two things were deliberately **not** changed:

- **GL Entry and Business Status Log refuse deletion.** The teardown had to go
  around them with raw SQL, pinned to the test company. The guards are right and
  were left alone.
- **Supplier Invoice has no grand total.** That is D2, and it is a business
  decision, so it is recorded rather than guessed.

---

## 6. How to check any of this yourself

Everything above is reproducible.

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost run-tests --app knit360_core'
```
49 structural checks. Reads the definitions.

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.acceptance.run_and_clean'
```
91 runtime checks. Drives the live system, then removes its own data.

```bash
docker exec knit-bench bash -lc 'cat /home/frappe/frappe-bench/sites/apps.txt'
```
Two lines: `frappe`, `knit360_core`. No ERPNext.

---

## 7. The one honest sentence

> The spine of the product is real and proven — a sales pipeline that runs end to
> end onto a double-entry ledger that balances, reverses rather than deletes, and
> refuses to be driven into a wrong state. Around that spine sit sixty-five
> correctly-modelled record types, most of which are still forms rather than
> working processes, and the three things standing between this and a system a
> business could run on are **taking payments, moving stock, and HR** — in that
> order.
