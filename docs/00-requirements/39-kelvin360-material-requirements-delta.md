# KIYA 360 — Supplementary Flow Material: Requirements Delta

## Document control

- **Document ID:** 39-kelvin360-material-requirements-delta
- **Status:** `PROPOSED` — assessment and classification only. Not an approved requirement expansion.
- **Received:** 22 September 2026, as pasted stakeholder material covering Sales/Receivables, Purchase/Payables, Accounting, PCB/BOM architecture, a module design roadmap, manufacturing workflows and a module connection map.
- **Baseline:** `source/KIYA360_BRD.pdf` v2.0 remains the authoritative source. This document does not amend it.

## Purpose and boundary

This document classifies the supplementary material against the sealed 28-module BRD baseline. It exists because `AGENTS.md` prohibits inventing business requirements and requires that material detail be recorded and traced before it is built.

It records three categories:

- **DETAIL** — elaborates a capability the BRD already mandates. Absorbable into detailed requirements without a scope decision.
- **NEW** — scope the BRD does not contain. Requires an approved change decision before specification or build.
- **CONFLICT** — contradicts an approved requirement, decision or architecture invariant. Must be resolved, not absorbed.

Nothing here is classified `OUT-OF-SCOPE`; the BRD does not explicitly exclude any of it.

## Recorded stakeholder decisions

Two decisions were taken on receipt of this material and are recorded here pending formal entry in the decision register:

| Ref | Decision | Consequence |
| --- | --- | --- |
| Pending `CD-003` | The supplementary material **extends** KIYA 360. It does not replace the BRD and is not a separate product. | The 28-module baseline, Phase 0 and Phase 1 seals remain valid. New scope enters through change decision, not by assumption. |
| Pending `CD-004` | "Single-entry accounting principle" in the source material means **single point of data entry**, not single-entry bookkeeping. Double-entry bookkeeping is retained. | `DEC-009` financial integrity and the atomic double-entry balancing invariant in `docs/02-architecture/04-target-architecture.md` §7 are unaffected. Trial Balance, P&L and Balance Sheet remain producible. |

The source material's wording on the second point is unsafe and should be corrected at source. "Single-entry accounting" names a specific bookkeeping method under which a Trial Balance and Balance Sheet cannot be produced, while the same material requires both.

---

## 1. Sales / Receivables and Purchase / Payables — `DETAIL`

**Classification:** `BRD-DERIVED`. Elaborates `MOD-17` Finance & Accounting and the `FR-FIN-*` requirement set. The BRD mandates the capability; this material supplies operational detail the BRD does not.

Absorbable content:

| Area | Supplementary detail | BRD anchor |
| --- | --- | --- |
| Receivables cycle | Sales Invoice → Customer Ledger → Customer Receivable → Payment Received → Receipt Entry → Bank/Cash → Bank Reconciliation | `MOD-17`, `DEP-001` |
| Payables cycle | Purchase Invoice → Vendor Ledger → Vendor Payable → Make Payment → Payment Entry → Bank/Cash → Bank Reconciliation | `MOD-17`, `DEP-005` |
| Receivable branching | Due/Upcoming → Payment Reminder; Overdue → Aging Report | `MOD-17` |
| Payable branching | Upcoming → Payment Planning; Overdue → Aging Report | `MOD-17` |
| Payment modes | Cash, Bank, Cheque | `MOD-17` |
| Aging buckets | Due Today, Due This Week, Overdue, 90+ Days Outstanding | `MOD-17`, `MOD-22` |
| Reports | Receivable, Payable, Collection (by date/mode/customer), Payment (by date/mode/vendor) | `MOD-22` |
| Dashboard KPIs | Total/Overdue Receivable and Payable, Today's and This Month's Collection and Payments, Cash Balance, Bank Balance | `MOD-22` |
| Other transactions | Journal Entry, Contra Entry, Expense Entry | `MOD-17` |
| Financial statements | Trial Balance, P&L, Balance Sheet, Cash Flow, Day Book, Ledger Reports | `MOD-17` |

**Assessment:** this is the most valuable part of the material. The BRD's Finance coverage is comparatively thin, and the aging, collection and reconciliation detail here is specific enough to specify against.

**Unresolved (`TBD`):** aging bucket boundaries beyond those listed; reminder trigger timing and escalation; cheque lifecycle states (issued, presented, cleared, bounced); reconciliation matching tolerance; whether partial settlement allocates by invoice or by age.

## 2. PCB / BOM architecture — `NEW`

**Classification:** `PROPOSED`. The term "PCB" appears **zero times** in BRD v2.0. This is new scope, not detail.

Proposed as `MOD-29` pending an approved change decision:

| Component | Content |
| --- | --- |
| PCB Master | PCB category, specification (dimensions, layers, material, thickness, copper weight, voltage), drawings, documents |
| Revision control | Rev 1.0/1.1/2.0, revision history, change log, approval, engineering control |
| PCB BOM | Components with reference designator, description, make, package; quantity, unit, wastage %; revision-wise costing |
| Component Management | Component master (item code, MPN, value, package, rating, HSN), passive/active sub-types, approved vendors and alternates |
| PCB Production | Manufacturing order, material allocation and reservation, material issue, SMT → THT → assembly → soldering → programming → testing |
| Quality | QC pass/fail, rework loop, final QC before finished goods |
| PCB Inventory | PCB stock, WIP stock, finished PCB stock, stock movement |
| PCB Reports | BOM report, component usage, production report, defect report |

**BOM revision locking.** The material states: *"When PCB-K100 Rev 1.1 becomes the current revision, old production orders using Rev 1.0 should never automatically change."*

This is a substantive integrity rule, not a convenience. It is consistent in spirit with `DEC-009` (posted effects are not overwritten) and `CD-002` (lifecycle states are explicit and auditable): a production order must bind to the BOM revision in force when it was raised, and later revisions must not retroactively alter historical consumption, costing or traceability. It should be specified as a first-class invariant rather than a UI behaviour.

**Relationship to existing scope.** `MOD-10` Manufacturing already covers BOM, routing, work orders and job cards. PCB scope overlaps it and must not duplicate it: whether PCB is a specialisation of `MOD-10` or a distinct module is an open design question, recorded below.

**Unresolved (`TBD`):** whether PCB extends `MOD-10` or stands alone; component substitution approval rules; wastage percentage treatment in costing; how revision approval interacts with the shared approval engine (`SF-005`).

## 3. Module design roadmap — `DETAIL`, with a caveat

**Classification:** `PROPOSED`. A 12-phase build sequence (Foundation → CRM → Sales → Purchase → Inventory → Accounting → GST → Manufacturing → PCB → Payments → Reports).

This is a **delivery sequencing proposal**, not a requirement, and it does not map one-to-one onto the BRD's 28 modules or onto the repository's phase structure (Phase 0 requirements, Phase 1 architecture, Phase 2 PoC). It is useful as an implementation ordering input. It carries no requirement authority and must not be treated as a revised module inventory.

Noted defect in the source: the roadmap skips Phase 9, numbering 8 then 10.

## 4. Items that cannot be absorbed — `CONFLICT`

| # | Item | Conflicts with | Resolution required |
| --- | --- | --- | --- |
| C-1 | Product named **KELVIN 360** throughout | BRD names the product **KIYA 360** in 32 places; "Kelvin" appears once, as the client company *Kelvinotherm Induction LLP* | Confirm whether this is a rebrand. If so it is a change decision affecting the BRD, all of `docs/`, and the app names `kiya_core` / `kiya_demo`. Until confirmed, KIYA 360 stands. |
| C-2 | "SINGLE-ENTRY ACCOUNTING PRINCIPLE" | `MOD-17` mandates double-entry (`BRD-REQUIRED`, doc 31); `04-target-architecture.md` §7 rejects unbalanced postings | Resolved by pending `CD-004` as *single point of entry*. Source wording should be corrected. |
| C-3 | "Google Sheets as Database", "Google Drive for Documents" | Zero BRD mentions; zero architecture mentions. Contradicts Phase 1 platform architecture and the database-per-tenant isolation model (`ADR-005`) | Not absorbed. Appears only under the "CRM + ERP System — Module Connection Map" section, which reads as a separate, smaller product specification. Confirm whether that section belongs to this engagement at all. |
| C-4 | Named AI features (AI Sales Assistant, AI Quotation Generator, AI Chatbot, AI Inventory Forecast) | `MOD-25` AI & Automation exists in the BRD but these specific capabilities are not specified there | Treat as `PROPOSED` candidate scope under `MOD-25`. Gap analysis rates `MOD-25` as `Missing` in the reference baseline, so all of it is build. |

## 5. Open questions raised

| ID | Question | Blocking |
| --- | --- | --- |
| `OQ-016` | Is KELVIN 360 a rebrand of KIYA 360, and if so what is the scope of the rename? | Yes — affects product identity, documentation and app naming |
| `OQ-017` | Is PCB/BOM management approved as new scope, and does it extend `MOD-10` or stand as `MOD-29`? | Yes — blocks PCB specification and build |
| `OQ-018` | Does the "Module Connection Map" section (Google Sheets, Google Drive, Web + Android app) belong to this engagement? | Yes — it asserts a platform contradicting Phase 1 |
| `OQ-019` | What are the exact aging bucket boundaries, reminder timing and cheque lifecycle states? | No — detail, specifiable later |
| `OQ-020` | How does BOM revision locking interact with the shared approval engine (`SF-005`) and the audit ledger (`SF-008`)? | No — design detail once `OQ-017` resolves |

`OQ-003` through `OQ-015` remain open and unaffected.

## 6. What may proceed now

On the two recorded decisions, the following is specifiable without waiting on the open questions above:

1. Receivables and payables lifecycle, ledger posting, aging and reconciliation (§1), under double-entry with a single point of data entry.
2. The collection, payment, receivable and payable reports and their dashboard KPIs.

The following must wait: all PCB scope (`OQ-017`), any renaming (`OQ-016`), and anything derived from the Module Connection Map section (`OQ-018`).
