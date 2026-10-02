# Capabilities Clients May Expect That the BRD Does Not Name

## Document control

- **Document ID:** `44-client-interest-outside-the-brd`
- **Date:** 3 October 2026
- **Status:** Assessment. Raises `OQ-023`. **Takes no scope decision.**
- **Method:** Each item below was checked against the 238-requirement inventory
  in `02-module-inventory.md` by text search before being listed. Items the BRD
  already names are listed separately in §3 so they are not mistaken for gaps.

`AGENTS.md` forbids inventing requirements and forbids classifying unspecified
functionality as OUT-OF-SCOPE. Nothing here is a requirement. These are
candidates for a conversation with the owner, recorded so the choice is explicit.

## 1. Verified absent from the BRD

Each term below returns **zero** matches in the 238-requirement inventory.

| # | Capability | Why a client may expect it | Likely demand |
| --- | --- | --- | --- |
| 1 | **Barcode / QR scanning** at goods receipt, picking and dispatch | Keying item codes by hand is the single largest source of stock error in a warehouse. Expected as standard in any system with bins. | High |
| 2 | **Customer credit limit and credit hold** | Stops an order being taken from a customer already over their limit. A finance controller will ask for this in the first demo. | High |
| 3 | **Credit notes and debit notes** | `FR-SALES-006 Returns` and `FR-SALES-007 Credit Memos` exist as names, but the accounting instruments are never defined. Without them a return cannot be settled. | High |
| 4 | **Landed cost** — freight, duty and insurance apportioned onto item cost | An importer's true item cost is wrong without it, which makes margin reporting wrong. | High for importers |
| 5 | **Warranty tracking** on sold equipment | The Asset-to-Service flow in BRD §6.3 names warranty as a *stage*, yet no requirement defines warranty terms, expiry or claim handling. | High |
| 6 | **Sales commission** for staff, agents or channel partners | Common where a sales team is incentivised. Affects payroll and margin. | Medium |
| 7 | **Dealer / distributor management** — tiered pricing, territory protection, dealer stock visibility | Nothing in the BRD covers indirect sales. If the business sells through dealers, the whole channel is unmodelled. | Depends on channel |
| 8 | **Export documentation** — packing list, commercial invoice, certificate of origin, shipping bill | Required to ship outside India. Not named anywhere. | High if exporting |
| 9 | **Weighbridge integration** | Directly relevant to a foundry or metals business weighing scrap and castings in and out. | Sector-specific |
| 10 | **Recurring / subscription billing** | For AMCs and service contracts. `KNIT 360 Service Contract` exists but nothing bills it on a cycle. | Medium |
| 11 | **Multi-currency revaluation** at period close | Any company holding foreign-currency balances needs this to close the books correctly. | Medium |
| 12 | **Data migration tooling** — opening balances, item and customer import | Every client arrives with existing data. Without this, onboarding is manual and slow. **This blocks the first customer, not the tenth.** | Certain |
| 13 | **Multilingual interface** | Shop-floor and warehouse staff often do not read English comfortably. | Depends on workforce |
| 14 | **Quality certificates** (mill certificates, test reports) issued with despatch | Routine in metals and engineering supply. `FR-QLTY-*` covers inspection but not the certificate issued to the customer. | Sector-specific |

## 2. `OQ-023` — Which of these enter scope? (OPEN)

Items 3, 5 and 12 deserve attention ahead of the rest, for reasons that are
structural rather than commercial:

- **Credit and debit notes (3)** — the BRD *names* Returns and Credit Memos as
  requirements, so these are arguably already in scope and merely unspecified.
  `FR-SALES-006` and `FR-SALES-007` are recorded elsewhere in this repository as
  unspecifiable for exactly this reason.
- **Warranty (5)** — BRD §6.3 names warranty as a stage of a core flow. A flow
  stage with no requirement behind it is a hole in a BRD-required flow, not an
  extra.
- **Data migration (12)** — no client can go live without it.

The rest are genuine additions and should be priced and scheduled as such.

## 3. Checked and already in the BRD — not gaps

Listed so they are not re-raised. Each **is** named in the 238:

| Capability | Requirement |
| --- | --- |
| E-invoicing and E-Way Bill | `FR-TAX-005` |
| Tax returns and statutory reports | `FR-TAX-006`, `FR-TAX-007` |
| Withholding tax (TDS/TCS) | `FR-TAX-004` |
| SLA management and escalations | `FR-CSVC-004`, `FR-CSVC-006` |
| Knowledge base | `FR-CSVC-003` |
| Shop-floor execution | `FR-MFG-005` |
| Production costing | `FR-MFG-006` |
| By-products and co-products | `FR-MFG-007` |
| Payment gateway | `FR-ECOM-005` |
| Customer portal | `FR-ECOM-007` |
| Supplier portal | `FR-SUPM-006` |
| Offline mobile sync | `FR-MOB-004` |
| Mobile approvals | `FR-MOB-007` |
| Digital signatures | `FR-DOCM-007` |
| Budget consolidation | `FR-EPM-005` |
| Predictive analytics | `FR-BI-006`, `FR-AIAU-002` |
| Anomaly detection | `FR-AIAU-006` |

An earlier draft of this assessment was going to list e-invoicing and the
customer portal as gaps. They are not. The list above was produced by searching
the inventory rather than by recollection, and that is why.

## 4. What this does not cover

Pricing, effort and sequencing for any of the above. None of these items is
authorised, scheduled or designed. `OQ-023` stays open until the owner decides
which, if any, enter scope.
