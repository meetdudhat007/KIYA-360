# Frappe HR (HRMS) — Observed Workflow Reference and Licence Boundary

## Document control

- **Document ID:** `45-hrms-workflow-reference-and-licence-boundary`
- **Date:** 5 October 2026
- **Status:** `PROPOSED` — observation and classification only. **Takes no scope decision and authorises no build.**
- **Subject:** `https://github.com/frappe/hrms` — "Frappe HR"
- **Raises:** `OQ-024`
- **Relates to:** doc 43 (ERPNext parity and licence boundary), doc 37 (source component reuse inventory), `OQ-006` (payroll/statutory detail)

### Method — exactly what was and was not done

Stated first because it is the part that matters legally.

**Read:**
- `license.txt` from the repository, to establish the licence from the primary document
- The public user documentation at `docs.frappe.io/hr`
- Repository **directory listings** — that is, the *names* of modules and document types, via the GitHub contents API

**Not read, not copied, not translated:**
- No Python controller, no JavaScript, no doctype JSON, no SQL, no patch
- No source file of any kind was opened

Everything in §4 and §5 below is a list of **what capabilities exist and in what order a user performs them**. None of it is anybody's code, and none of it was derived by reading code.

---

## 1. Licence — verified, not assumed

| | |
| --- | --- |
| Licence | **GNU General Public License, Version 3 (GPL-3.0)** |
| Verified from | `license.txt` in the repository, first lines: "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007" |
| Not | GPL-2.0, LGPL, AGPL-3.0 or MIT |

This matches ERPNext (doc 43) and differs from Frappe Framework, which is MIT and which KNIT 360 is built on.

---

## 2. The boundary, with sources

Three things are established. One is not, and saying which is which is the point of this section.

### 2.1 Established — translating code is a modification

The GNU GPL FAQ, answering *"What does the GPL say about translating some code to a different programming language?"*:

> "Under copyright law, translation of a work is considered a kind of modification. Therefore, what the GPL says about modified versions applies also to translated versions."

**Consequence:** taking an HRMS controller and rewriting it in another language, or restructuring it into KNIT 360's shape, produces a modified version of a GPL-3 work. This is the single clearest line, and it is why no source file was opened.

### 2.2 Established — copyright does not reach ideas or methods

United States, 17 U.S.C. §102(b), verbatim:

> "In no case does copyright protection for an original work of authorship extend to any idea, procedure, process, system, method of operation, concept, principle, or discovery, regardless of the form in which it is described, explained, illustrated, or embodied in such work."

India — the jurisdiction that appears to apply here — reaches the same place through case law rather than statutory text. **R.G. Anand v. Deluxe Films, AIR 1978 SC 1613 (Supreme Court of India)** held that there is no copyright in an idea, subject matter, theme or plot; what is protected is the manner in which the idea is expressed. The Copyright Act, 1957 does not use the phrase "idea-expression dichotomy", but protects the form of expression rather than the underlying idea.

**Consequence:** "an employee requests leave, a manager approves it, the balance reduces" is a method of operation. The sequence of steps a user performs is not somebody's property.

### 2.3 Established — the GPL attaches on distribution

As recorded in doc 43 and unchanged: GPL-3 obligations are triggered by conveying the work. The gap for hosted software is addressed by AGPL-3, which this is not.

### 2.4 **Not established** — that reimplementation from observation is safe

This is the honest part, and it is a correction to any impression the three sections above might give.

The FSF's own GPL FAQ was checked for guidance on writing an independent implementation after studying GPL'd code, or on copying interface and functionality rather than code. **It does not address either question.** The FAQ states it addresses general questions, "may not apply in your specific legal situation", and that **the FSF cannot give legal advice**, directing such questions to its Compliance Lab.

So the position is:

- Copying or translating the code is clearly inside the licence. **Avoided.**
- Building to a functional description is on the far side of a line that §102(b) and *R.G. Anand* describe but that no source consulted here applies to this specific case.
- Where exactly that line sits for a commercial product is **a question for a lawyer, not for this document.**

**Nothing here is legal advice.** `Y1` in `docs/03-guides/03-handover-what-is-left.md` — obtain a corporate legal opinion on the licensing position — remains open and now covers HRMS as well as ERPNext.

### 2.5 Working rules adopted for this exercise

| Rule | Status |
| --- | --- |
| Do not read HRMS source files | Followed |
| Do not copy or translate any code | Followed |
| Do not install HRMS alongside KNIT 360 | Followed — installed apps remain `frappe`, `knit360_core` |
| Do not reuse HRMS doctype names verbatim as KNIT 360 doctype names | **Decided 6 October 2026 — `DEC-026`.** Ordinary HR terms are used; the arrangement is not. |
| Record every observation's source | Followed |

On the last rule: names such as "Leave Application" are ordinary HR vocabulary and predate the software. But adopting 157 of them in the same arrangement starts to look like copying an arrangement rather than using common terms. This deserves a decision rather than a default.

---

## 3. What Frappe HR is, in scale

Document types observed by directory name:

| Module | Document types |
| --- | --- |
| `hrms/hr` | 114 |
| `hrms/payroll` | 43 |
| **Total** | **157** |

The other top-level directories — `leaves`, `shift_and_attendance`, `performance`, `recruitment`, `tenure`, `expenses`, `tax_and_benefits`, `regional` — hold workspace and sidebar configuration; their document types live under `hr` and `payroll`.

For scale: **KNIT 360 has 86 document types in total, covering fourteen BRD modules.** HRMS has 157 for one.

The README describes it as "a complete HRMS solution with over 13 different modules".

---

## 4. Observed capability surface

Grouped by function. Every name is a directory name in the repository or a term from the public documentation.

### 4.1 Recruitment
Staffing plan · job requisition · job opening · job applicant · job applicant source · employee referral · interview · interview type · interviewer · interview feedback · job offer · job offer terms · appointment letter and templates

### 4.2 Employee lifecycle
Employee onboarding and templates · boarding activity · employee grade · employment type · employee promotion · employee transfer · employee property history · employee separation and templates · exit interview · full and final statement, with asset and outstanding-statement detail

### 4.3 Leave
Leave type · leave period · leave policy · leave policy assignment · leave allocation · leave application · **leave ledger entry** · leave block list · leave encashment · compensatory leave request · earned leave schedule · leave adjustment · leave control panel · holiday list assignment

### 4.4 Attendance and shift
Attendance · attendance request · employee checkin · employee attendance tool · shift type · shift assignment · shift request · shift schedule · shift location · shift assignment tool · overtime type · overtime slip · overtime details

### 4.5 Performance
Appraisal · appraisal cycle · appraisal template · appraisal goal · KRA and appraisal KRA · goal · appraisee · employee performance feedback · feedback criteria · feedback rating

### 4.6 Payroll
Salary component and component account · salary structure · salary structure assignment and bulk assignment · salary detail · **salary slip** (with leave, loan and timesheet detail) · **payroll entry** · payroll period · payroll employee detail · payroll settings · payroll correction · salary withholding and withholding cycle · additional salary · arrear · retention bonus · employee incentive · employee other income · employee cost center

### 4.7 Tax and benefits
Income tax slab and other charges · taxable salary slab · employee tax exemption category, sub-category, declaration and proof submission · employee benefit application, claim and ledger · gratuity, gratuity rule and rule slabs

### 4.8 Expenses and travel
Expense claim, type, detail, advance and account · expense taxes and charges · employee advance · travel request · travel itinerary · travel request costing · purpose of travel

### 4.9 Training, skills, grievance, fleet
Training program · training event and attendees · training result · training feedback · skill · employee skill and skill map · designation skill · expected skill set · skill assessment · employee grievance and grievance type · vehicle log · vehicle service · employee health insurance

### 4.10 Reports named in the documentation
Employee Leave Balance · Salary Register · Monthly Attendance Sheet · Shift Attendance · Vehicle Expenses Report · Employee Exits · Employee Birthday · Employee working on a holiday · Bank Remittance Report · Loan Repayment Report

---

## 5. Observed sequences

From the public documentation. These are methods of operation, and they are also simply how payroll works in any organisation.

### 5.1 Leave

```
Leave Policy            the company's rules
   ↓ assigned by
Leave Policy Assignment to an employee, for a Leave Period
   ↓ produces
Leave Allocation        a balance of a Leave Type
   ↓ drawn against by
Leave Application       employee requests dates; an approver decides
   ↓ recorded in
Leave Ledger Entry      the transaction record behind the balance
```

**The observation worth the whole exercise:** leave balance is not a number stored on the employee. It is derived from a **ledger of entries**, the same shape as a general ledger — allocations credit, applications debit, and the balance is the sum. Encashment and compensatory requests are further entry types.

That is the same reasoning KNIT 360 already applies in `finance/ledger.py`, where a balance is never stored and always derived. It is a structural insight, not a piece of anyone's code.

### 5.2 Payroll

```
Salary Component              individual earnings and deductions
   ↓ composed into
Salary Structure
   ↓ assigned by
Salary Structure Assignment   per employee, with a base
   ↓ generated in bulk by
Payroll Entry                 Draft → Submitted
   ↓ which produces
Salary Slip                   Draft → Submitted, per employee
   ↓ books through
Journal Entry                 salary expense and payable into the accounts
```

Documented statuses: Payroll Entry *Draft → Submitted*; Salary Slip *Draft → Submitted*. The documentation consulted did not state a fuller status set, and none is invented here.

Payroll Period and Income Tax Slab bound the calculation and the tax.

**Second observation:** payroll reaches the books through an ordinary **journal entry**, not a private mechanism. KNIT 360 already has a working Journal Entry and a ledger that refuses unbalanced postings, so the accounting end of payroll is a consumer of something that exists.

### 5.3 Leave application statuses

The documentation consulted **did not state** the full status set for a Leave Application. It describes that an approver can approve or reject. A complete lifecycle is not recorded here because it was not observed, and `AGENTS.md` forbids inventing it. See `OQ-024`.

---

## 6. Mapping to the BRD

The BRD gives module 19 seven requirements, every one marked *"TBD — The BRD does not specify this detail."*

| BRD requirement | Observed HRMS area | Comment |
| --- | --- | --- |
| `FR-HR-001` Employee Master | Employee, grade, employment type, skills, property history | **KNIT 360 Employee already exists**, in Platform |
| `FR-HR-002` Organization Management | Department, designation, grade, approvers | **Department and Designation already exist**, in Platform. Overlaps `FR-PADM-1.1.x` |
| `FR-HR-003` Attendance & Leave | §4.3 and §4.4 — ~27 document types | Largest single area |
| `FR-HR-004` Payroll Processing | §4.6 — 18 document types | `OQ-006` already open on statutory detail |
| `FR-HR-005` Benefits Management | §4.7 — benefits, gratuity, tax exemption | Deeply India-statutory |
| `FR-HR-006` Performance Management | §4.5 — appraisal, KRA, goals, feedback | Self-contained |
| `FR-HR-007` HR Analytics | §4.10 — the named reports | Needs the others first |

### Observed in HRMS, outside the seven BRD requirements

Recruitment · training · travel · expense claims and advances · grievance · fleet · health insurance · employee referral · skill assessment.

Per `AGENTS.md` these are **not** classified OUT-OF-SCOPE. They are unspecified. Expense claims in particular are a common early ask and sit close to Finance, which is built.

---

## 7. What this suggests for KNIT 360 — proposal only

No decision is taken here.

**1. Do not attempt 157 document types.** HRMS is a mature product with a large team behind it. The BRD asks for seven requirements.

**2. A defensible first cut, in order:**

| Order | Area | Why first |
| --- | --- | --- |
| 1 | Employee master, completed | It exists; finish it |
| 2 | Holiday list, leave type, leave allocation, leave application, **leave ledger** | Smallest useful whole. The ledger shape is already proven in Finance |
| 3 | Attendance and check-in | Feeds payroll; standalone value |
| 4 | Salary component, structure, assignment, salary slip, payroll entry | Ends in a Journal Entry that already works |
| 5 | Appraisal | Self-contained, no dependencies |

**3. Reuse what exists rather than restating it.** `business_status` for lifecycles, `finance/ledger.py`'s derived-balance pattern for leave, `pricing/totals.py` for salary slip arithmetic, `Journal Entry` for the accounting leg.

**4. Statutory payroll is the risk, not the HR.** Income tax slabs, exemption declarations and proof, gratuity rules, PF, professional tax and bank remittance formats are **legal requirements that change by jurisdiction and by year, and getting them wrong has consequences for the client's employees.** This is `OQ-006`, and it should be scoped separately from the rest of HR and probably taken on specialist advice.

---

## 8. `OQ-024` — open questions

**Three of the five were closed on 6 October 2026** by owner delegation, and are
recorded as decisions. See `docs/03-guides/06-the-money-decisions-in-plain-language.md`.

1. ~~**Does KNIT 360 reuse HR vocabulary verbatim?**~~ **Closed — `DEC-026`.** Ordinary HR terms are used; the arrangement is not. Seven record types serve the BRD's leave requirement, against roughly 157 in that product.
2. ~~**What is the Leave Application lifecycle?**~~ **Closed — `DEC-026`.** Draft, Pending Approval, Approved, with Rejected returning to Draft as a draft state, classified BRD-DERIVED on the `CD-001` baseline and labelled as a reading rather than a specification.
3. **Which of §6's out-of-BRD areas enter scope?** Still open. Expense claims are the likeliest early ask. Classified **TBD** per `DEC-009` — not in version one, and not OUT-OF-SCOPE.
4. ~~**Is statutory payroll in scope at all?**~~ **Closed — `DEC-024`.** It is not, for version one. Pay components, salary structure, payslip, the payroll journal entry and an export for the client's payroll provider are in; income tax slabs, provident fund, employee state insurance, professional tax and gratuity are out. Professional tax is an Article 276 **state** levy whose bands differ by state and which some states do not levy at all; income tax slabs move with each Finance Act. The risk is the client's legal exposure, not a feature gap.
5. **Does the legal opinion in `Y1` cover reimplementation-from-observation, or only non-installation?** Still open, and **not mine to close.** The FSF FAQ does not answer it and I am not a lawyer. §2.4.

---

## 9. What this document does not do

It authorises nothing, specifies nothing, and schedules nothing. It contains no HRMS source code, no translation of any, and no field-level design. It is a record of what the product does and in what order, so that a specification can be written against the BRD — by people, with the owner's decisions and a lawyer's opinion in hand.

---

## Sources

- [frappe/hrms](https://github.com/frappe/hrms) — repository, README, `license.txt`, directory listings via the GitHub contents API
- [Frappe HR documentation](https://docs.frappe.io/hr) — introduction, leave management, payroll, employee lifecycle, HR reports
- [GNU GPL Frequently Asked Questions](https://www.gnu.org/licenses/gpl-faq.html) — translation as modification; FSF cannot give legal advice
- [17 U.S.C. §102](https://www.law.cornell.edu/uscode/text/17/102) — subsection (b)
- [R. G. Anand v. Deluxe Films](https://en.wikipedia.org/wiki/R._G._Anand_v._Deluxe_Films) — AIR 1978 SC 1613, Supreme Court of India
