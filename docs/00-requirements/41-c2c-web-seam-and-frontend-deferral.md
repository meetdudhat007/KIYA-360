# Customer-to-Cash Web Seam, and the Deferred Front-End Technology Decision

## Document control

- **Document ID:** `41-c2c-web-seam-and-frontend-deferral`
- **Decision ID:** `CD-009`
- **Open question raised:** `OQ-021`
- **Status:** `CD-009` recorded; `OQ-021` **OPEN**
- **Date:** 23 September 2026
- **Implements:** `ADR-004` (Anti-Corruption Framework Insulation & Strategic Seams), seam 6 of 8 — **UX/Mobile**

## Context

`ADR-004` names UX/Mobile as a KNIT-owned strategic seam. Until now KNIT had no
user interface of its own: the 61 doctypes were reachable only through Frappe's
Desk, whose auto-generated forms are a framework artefact, not a KNIT product
surface. Desk was rebranded under `CD-005` but rebranding an admin interface does
not satisfy a seam.

## CD-009 — The web seam

**Decision.** A KNIT front end reaches the platform only through
`knit_core.api.c2c`. It does not call Frappe's generic `/api/resource/<DocType>`
endpoints.

**Rationale.** `/api/resource` exposes the doctype schema directly to the client.
Every field rename would become a front-end change, and the front end would be
coupled to the framework rather than to KNIT — which is precisely the coupling
`ADR-004` forbids. The seam speaks *stages* and *business statuses*; doctype
names, child-table shapes and `docstatus` stay behind it.

**Extent.** `CD-009` covers the Customer-to-Cash stages implemented so far —
`KNIT Lead` → `KNIT Opportunity` → `KNIT Quotation`. Later stages extend the same
module; they do not warrant a new decision.

**Consequences.**

| | |
| --- | --- |
| Lifecycle | The seam never writes `knit_business_status`. It calls `business_status.engine.transition`, so the `CD-002` matrix, the docstatus derivation and the audit log remain the single authority. |
| Field exposure | `create_lead` takes named arguments, not a document dict, so the web cannot set fields the seam does not offer. |
| Reachability | A doctype absent from `c2c.STAGES` is unreachable from the front end. |
| Schema drift | Field labels, line-item columns and lifecycle states are read from the Frappe meta and the lifecycle registry at request time, so adding a state or a column needs no front-end change. `knit_core/api/test_c2c_contract.py` fails the build if the seam's field list drifts from the doctype JSON. |

## OQ-021 — Front-end technology for the product UI (OPEN)

**Not decided here.** The page at `/knit` is framework-free HTML, CSS and
JavaScript served by Frappe as a website page. No framework, build step, package
manager or component library is introduced.

**Why it is deliberately deferred.** `AGENTS.md` bars an agent from taking
technology, architecture or UI decisions outside an authorised phase, and no ADR
covers the front-end stack. Committing the repository to React, Vue, Flutter or
Frappe UI would be exactly such a decision.

**What `/knit` therefore is and is not.** It proves the *seam*, not the *stack*:
that a KNIT-owned interface can run the whole flow without touching Frappe's
generic API, and without Desk. It is not the product UI. When `OQ-021` is
decided, the chosen client re-implements the screens against the same
`knit_core.api.c2c` methods; the seam is the part meant to survive.

**Depends on** `FR-MOB-001`–`007` / `SF-009`, since a native mobile client and a
web client should share one seam. Offline behaviour remains `OQ-013` / `PoC-04`.

## Finding recorded, no change made: `is_submittable`

None of the 61 doctypes set `is_submittable`. Eight of them nevertheless have
lifecycles whose states require `docstatus 1`. This was tested on the running
site rather than assumed:

- `frappe.get_meta("KNIT Sales Order").is_submittable` is `0`, yet `SO-2026-0002`
  holds `docstatus 1` — Frappe does not refuse `submit()` on such a doctype.
- Editing that submitted document raises `UpdateAfterSubmitError`. **The
  protection `CD-002` depends on is enforced by the docstatus value itself, not
  by the flag.**

Left unchanged, because the absent flag also removes Desk's own Submit and Cancel
buttons — which means Desk cannot bypass the business-status adapter. That is the
behaviour `CD-006` wants. Revisit only if amendment (`amended_from`) is required.

## Verification

| Check | Result |
| --- | --- |
| Site-free test suite | 37 tests pass (29 existing + 8 new contract tests). |
| `/knit` unauthenticated | Redirects to `/login`. |
| Full flow over HTTP | Lead created → `Contacted` → `Qualified` → converted (customer `Shakti Forgings Pvt Ltd` + `OPP-2026-0004`) → quotation raised → `Pending Approval` → `Issued / Sent` → `Accepted`. |
| Docstatus boundary | Crossed exactly once, `0 → 1` at `Issued / Sent`, as `QUOTATION.submitted_states` declares. |
| Illegal transition | `Qualified → Contacted` refused, with the allowed set named. |
| Post-submission edit | `set_items` on the submitted quotation refused. |
| Audit trail | Three rows for the lead, three for the quotation, each carrying `from_docstatus` / `to_docstatus`. |

## Open items this does not address

- Sales Order onward (`DR-C2C-005` and later stages) is not in the seam yet.
- Pricing is unpriced by construction: `unit_rate` is entered by hand because the
  price list master is BRD-DERIVED and TBD under `FR-SALES-004`.
- Whether raising a quotation should advance the Opportunity to `Proposal Sent`
  is not stated by `DR-C2C-002`; the seam leaves it to the user. Part of `OQ-018`.
