# Proving Requirement Coverage to a Client, in the Live System

## Document control

- **Document ID:** `03-guides/05-proving-requirements-to-a-client`
- **Date:** 5 October 2026
- **Status:** Operational. How to run an evidence session against the running system.
- **Supersedes nothing.** Read with `02-demonstration-script.md`, which is the
  product demo; this is the narrower, harder meeting about requirements.

---

## 1. Start from the truth, because the alternative does not survive the meeting

You asked how to prove you have met all their requirements. You cannot, and it
is better to know why before you are in the room than after.

**Two reasons, neither of them about how much work has been done.**

**First: 69 of 238 requirements are covered. 169 are not started.** That is the
system's own count, produced by reading itself, and it is in §3 below. Fourteen
of the BRD's twenty-eight modules have nothing built — including HR & Payroll,
Marketing, Customer Service, Projects and E-Commerce. A claim of full coverage
dies the moment someone asks to see payroll.

**Second, and more important: the BRD does not define "met".** Every one of the
238 requirements is recorded with the same detail:

> *TBD — The BRD does not specify this detail.*

`FR-SALES-002` says "Quotations". That is the entire requirement. There is no
acceptance condition, so there is nothing to test "met" against. If you claim
you have met it, the client gets to decide after the fact what it meant — and
they will decide that whenever they find something missing.

**So do not argue coverage. Offer evidence and a plan.** That is a stronger
position, and it is the one the system can actually back.

---

## 2. What you can prove, which is more than it sounds

Three things, each demonstrable live and none of them a claim:

| | What you prove | How |
| --- | --- | --- |
| **1** | **Traceability.** Every field in the system names the requirement it came from, and you can show the link in both directions. | The coverage report, §3 |
| **2** | **Behaviour.** Twelve requirements are not merely modelled — an automated check drives them on a live site and asserts on the result. | The acceptance run, §4 |
| **3** | **Honesty.** You can show them the 171 gaps before they find one. | The same report, "Only the gaps" |

A supplier who opens with their own gap list is in a different conversation
from one who gets caught. The second conversation is about trust; the first is
about scope and price.

---

## 3. The coverage report — the centrepiece

**Where:** `/app/query-report/KNIT 360 Requirement Coverage`
Or: search bar → "Requirement Coverage".

It reads the running system. Nothing in it is typed by hand except one short
list described below.

### What they see

Four cards across the top, then a donut, then 238 rows:

```
Proven by a live check             12
Modelled, not yet proven           57
Not started                       169
BRD modules with anything built  15 / 28
```

and the headline:

> **69 of 238 BRD requirements are covered (29.0%)** — 12 proven by an automated
> check that drives a live site, 57 modelled but not yet proven, 169 not
> started. 15 of 28 BRD modules have anything built.

### The columns, and what each one is worth

| Column | What it means |
| --- | --- |
| **Requirement** | The BRD's own id, e.g. `FR-PADM-1.1.1` |
| **What the BRD calls it** | The BRD's own words, e.g. "Company Master" |
| **BRD Module** | Which of the 28 |
| **Status** | `Proven`, `Modelled` or `Not started` — defined below |
| **Built as** | The record type that implements it |
| **Fields** | How many fields on it cite this requirement |
| **Also linked from** | How many *other* record types reference it |
| **Live records** | How many real documents exist right now |
| **Proven by this check** | For `Proven` rows, the named automated check |

### The three statuses, stated the way you should state them

> **Not started** — nothing in the system cites this requirement. 169 of them.
>
> **Modelled** — the data is designed for it and the fields exist, **but no
> automated check proves any behaviour.** A Delivery Note exists and cites
> `FR-SALES-005`, and it moves no stock. Modelled is not done.
>
> **Proven** — an automated check inserts a document, drives it through its
> lifecycle on a live site, and asserts on the result. Twelve of these.

Say "modelled is not done" out loud yourself. If the client has to work it out,
you have lost the room.

### Showing traceability in both directions

This is the part that lands. Pick a row — `FR-PADM-1.1.1 Company Master` — and
show:

1. The report says: built as **Company**, 9 fields cite it, 36 other record
   types link to it, 2 live records, proven by *"A company created the ordinary
   way gets its own books"*.
2. Open **Platform → Company**. The records are there.
3. Open one and hover any field. The field's own description reads
   `FR-PADM-1.1.1: ...`.

> **"That link is not documentation we maintain alongside the code. It is in the
> code. A structural test refuses to let any field exist without naming the
> requirement it came from — so the report cannot drift from the system."**

### Showing the gaps deliberately

Tick **Only the gaps**. 169 rows. Scroll it.

Then filter **BRD Module → HR & Payroll**: seven rows, one of them `Proven`
(`FR-HR-003 Attendance & Leave`) and six `Not started`.

> **"Leave management is built and proven. Attendance, payroll, appraisal and
> recruitment are not. I would rather show you this now than have you find it
> in month three."**

### Exporting it

Menu → **Export** → Excel or CSV. Send it with the minutes. A client who can
re-read the gap list at their desk is a client who is not surprised later.

---

## 4. The acceptance run — proving behaviour, not drawings

A report is still a report. This is the part that is not.

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.acceptance.run_and_clean'
```

About a minute, one line per check, ending `149/149 checks passed`, then it
removes its own data.

> **"That was not a recording. It just created a company and its chart of
> accounts, made a lead, qualified it, converted it, priced a quotation,
> raised an invoice, posted it to the ledger, tried to edit it after posting,
> tried to post an unbalanced entry, tried to submit around the lifecycle — and
> confirmed every refusal held."**

The twelve `Proven` requirements are these checks. Show one connection explicitly:

- Report row `FR-FIN-003 Accounts Receivable` → **Proven by:** *"A sales invoice
  posts a receivable and reports it outstanding"*
- That exact line appears in the run output.

**198 checks in total**: 49 structural, 149 runtime. Structural ones read the
definitions; runtime ones drive the system.

---

## 5. The shape of the session

Fifty minutes. Different from the product demo: this room contains someone with
the BRD open.

| | Part | Minutes | Point |
| --- | --- | --- | --- |
| 1 | State the position (§1) | 5 | You set the frame, not them |
| 2 | The coverage report, all 238 rows | 10 | Everything is accounted for |
| 3 | Traceability both ways on one requirement | 10 | The link is in the code |
| 4 | The acceptance run, live | 10 | Behaviour, not drawings |
| 5 | "Only the gaps", module by module | 10 | You disclose, they don't discover |
| 6 | What it takes to close them | 5 | Ends on a plan |

**Open with something like:**

> *"I am not going to tell you we have met all 238 requirements. I am going to
> show you exactly which ones the system covers, which of those are proven by
> automated tests rather than by my say-so, and which are not started — and then
> what it takes to close the rest."*

**Close on §4 of the handover**, which already orders the remaining work by
value. The top three are Payment Entry posting, the stock ledger, and HR.

---

## 6. The questions that will come, and honest answers

**"29% after all this time?"**
> *"29% of a 238-requirement BRD where every requirement says the detail is TBD.
> What exists is the spine — the sales cycle end to end onto a double-entry
> ledger that balances. The 171 are mostly whole modules nobody has specified
> yet. Six decisions that were blocking the next three large pieces of work
> were closed on 6 October, so Payment Entry, the stock ledger and payroll are
> all buildable now."*

**"How do we know 'Proven' means anything?"**
> Run it in front of them. Then: *"And a structural test refuses to let a
> requirement be marked Proven unless it names an acceptance check that actually
> exists. The report cannot flatter itself."* That test is real:
> `test_every_proven_requirement_exists`.

**"Can we have this report every month?"**
> Yes. It reads the live system, so it is current whenever it is opened. Export
> it and the trend is the project plan.

**"Who decided what counts as covered?"**
> *"Nobody decided per requirement. A requirement counts as covered when a field
> in the system cites it, which is enforced by a test rather than by judgement.
> The only hand-written part is which twelve are marked Proven, and each of those
> names the check that backs it."*

**"What about the requirements where you built something but it is wrong?"**
> A fair question and the honest answer is that `Modelled` does not rule it out.
> That is precisely why the status is not called "done", and why the gap between
> 57 modelled and 12 proven is the real backlog.

---

## 7. What to never say

| Do not say | Say instead |
| --- | --- |
| "We've met all your requirements" | "69 of 238 are covered; here is the breakdown" |
| "That module is done" | "That module is modelled. Nothing proves the behaviour yet." |
| "It's basically finished" | "The sales spine is proven. Here is what is left, in order." |
| "We can add that easily" | "That is a decision I need from you first — here is the question." |

---

## 8. Running the numbers yourself before the meeting

```bash
docker exec knit-bench bash -lc 'cd /home/frappe/frappe-bench && bench --site knit360.localhost execute knit360_core.traceability.print_summary'
```

Prints the headline and a per-module breakdown. Read it before you walk in, so
no figure on the screen is new to you.

Check the data is seeded and the test data is cleared first — §1 of the
demonstration script.
