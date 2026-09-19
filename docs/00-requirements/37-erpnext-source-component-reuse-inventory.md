# KIYA 360 — ERPNext Source Component and Reuse Inventory

## Status, purpose, and boundary

**Assessment-only / PROPOSED reference.** This document supplements, but does not replace, the BRD baseline or the assessment in `18-erpnext-fappe-feasibility-assessment.md`, matrix `19-erpnext-fappe-feasibility-matrix.md`, and PoC plan `20-erpnext-poc-plan.md`.

It records what the KIYA repository currently contains, what was verified in an exact ERPNext source snapshot, how the verified ERPNext/Frappe components connect, and which components are plausible *candidates* for a later authorized reuse assessment. It is not a platform selection, implementation plan, licence conclusion, or approval to copy, install, configure, or modify upstream code.

The KIYA BRD remains authoritative. A same-named ERPNext component does not establish that it implements a KIYA requirement; KIYA’s detailed rules, data ownership, approval behavior, tax/payroll scope, mobile/offline behavior, AI governance, integrations, and measurable NFRs remain governed by OQ-001 through OQ-015.

## Evidence and snapshot

| Item | Evidence |
| --- | --- |
| KIYA requirements baseline | `source/KIYA360_BRD.pdf`, BRD v2.0; the user-provided pasted BRD text was also reviewed. The pasted-text hash differs from the PDF binary hash, as expected for text extraction; the approved PDF remains the source of truth. |
| KIYA implementation state | No application/source-code directories, build files, dependency manifests, or tests were found in the project. The repository contains the BRD, requirements/governance Markdown documents, and context records. |
| Upstream inspected | `https://github.com/frappe/erpnext.git`, shallow source snapshot cloned 13 September 2026. |
| Exact upstream revision | `fe25746febc8731bbbc0880dcb18d528dcf08a63`; commit time `2026-09-13T11:58:56+05:30`. Reassess against an approved, pinned release/tag before any experiment. |
| Upstream application version | `erpnext/__init__.py` reports `17.0.0-dev`; it is a development-line snapshot, not a KIYA-approved runtime version. |
| Framework coupling | ERPNext declares a Bench dependency on Frappe `>=17.0.0-dev,<18.0.0`. Frappe is a separate upstream framework repository and runtime. |
| Licence signal | ERPNext `package.json` and `license.txt` identify GPL-3.0. This is a technical evidence point only; legal review is required before any product/distribution decision. |
| Primary references | ERPNext source snapshot; official Frappe documentation for [DocTypes](https://docs.frappe.io/framework/user/en/basics/doctypes), [controllers](https://docs.frappe.io/framework/user/en/basics/doctypes/controllers), [hooks](https://docs.frappe.io/framework/user/en/python-api/hooks), [REST/RPC API](https://docs.frappe.io/framework/user/en/guides/integration/rest_api), [background jobs](https://docs.frappe.io/framework/user/en/api/background_jobs), and [webhooks](https://docs.frappe.io/framework/user/en/guides/integration/webhooks). |

## Current KIYA directory comparison

| Area | Current KIYA directory | ERPNext source | Reuse finding |
| --- | --- | --- | --- |
| Requirements and governance | 28 BRD modules, 238 baseline requirement records, 15 open questions, foundations/dependencies, feasibility work | Not applicable | KIYA documentation is the governing plan; preserve its terminology and traceability. |
| Transaction/domain code | None | Mature domain app with Accounts, CRM, Buying, Selling, Stock, Manufacturing, Quality, Assets, Projects, Maintenance and related modules | No local code can be reused today. Upstream components are candidates only after a legal/architecture decision and a bounded PoC. |
| Application framework/runtime | None | ERPNext runs on the separately supplied Frappe Framework | Introducing Frappe would be a new technology/architecture decision, currently deferred. |
| UI/mobile client | None | Frappe Desk/web UI; one `banking/` sub-application built with React; no evidence that this provides KIYA’s required native offline mobile suite | Do not treat the Banking React app as a general KIYA UI/mobile starter. |
| Tests and operations | No application tests or runtime | 524 Python test files found in the snapshot plus Frappe/Bench operational conventions | Upstream tests show useful regression assets, but cannot validate KIYA behavior without KIYA-owned acceptance tests. |

## What ERPNext is made of

ERPNext is an **application**, not a standalone general-purpose backend. Its business modules are installed into the Frappe Framework. Frappe supplies the generic application model; ERPNext supplies the ERP-specific DocTypes, controllers, reports, fixtures, integrations, regional rules, and desk assets.

```text
Browser / external client / integration
             |
             v
Frappe web/API layer ── REST document endpoints + whitelisted RPC methods
             |
             v
DocType metadata (JSON) ── fields, links, permissions, naming, workflow metadata
             |
             v
Python Document controller ── validate / submit / cancel lifecycle rules
             |
             +── ERPNext domain services ── stock ledger, GL, tax, planning, reports
             +── Frappe hooks ── permissions, document events, scheduled work
             +── background workers / realtime events / webhooks
             |
             v
Frappe-managed persistence and files
```

### Core Frappe mechanisms used by ERPNext

| Mechanism | How it works | ERPNext consequence / KIYA relevance |
| --- | --- | --- |
| DocType | Metadata defines a record type, fields, child tables, links, permissions and client behavior. A database-backed record is a Document. | ERPNext domain objects such as `Customer`, `Item`, `Sales Order`, and `Purchase Invoice` are DocTypes. Their links give useful master/transaction continuity, but KIYA’s final semantics remain TBD. |
| Controller lifecycle | A Python class derived from Frappe `Document` can run validation and lifecycle methods such as `validate`, `before_submit`, `on_submit`, and `on_cancel`. | This is where many ERP integrity effects are implemented: a submitted transaction may create ledger/accounting consequences; cancellation reverses them. Copying a screen or JSON definition without its controller logic would be unsafe. |
| Links and child tables | A DocType can refer to other documents and contain row-oriented child documents. | Typical flows link a customer/supplier/item/company/warehouse to a transaction and its line rows. This supports traceability, but not KIYA’s unapproved master ownership, status, or validation rules. |
| Permissions and company restrictions | Frappe roles and document permissions gate actions; ERPNext adds query/record permission handlers for selected shared masters such as Item, Customer, Supplier, and BOM. | Candidate foundation for SF-001–SF-003/SF-008. It does not prove KIYA’s device, IP, MFA, data-level, cross-company, or audit policy. |
| Hooks | `hooks.py` registers application lifecycle, boot, document events, permission handlers, scheduled work, regional overrides, assets and other extension points. | A KIYA custom app could use supported extension points in a future experiment; direct core edits and broad overrides have higher upgrade risk. |
| API | Frappe generates CRUD REST endpoints for DocTypes and exposes whitelisted Python methods as RPC. | Useful plumbing for SF-012, but raw DocType endpoints should not become KIYA’s external product contract without an approved API boundary. |
| Background/realtime/event integration | Frappe supports queued jobs, schedulers, realtime publish/subscribe, and configurable webhooks. | Useful for notifications, integrations, reconciliation, reporting jobs and automation. It is not proof of KIYA’s RPA, AI, integration monitoring, or delivery guarantees. |
| Reports/print/files/timeline | Frappe provides report, print/PDF, file attachment and timeline primitives used by ERPNext. | Candidate base for transactional reporting and attachments, not demonstrated equivalence for BI/EPM or enterprise DMS/retention/e-signature. |

## Verified ERPNext source topology

`erpnext/modules.txt` declares 21 desk modules: Accounts, CRM, Buying, Projects, Selling, Setup, Manufacturing, Stock, Support, Utilities, Assets, Portal, Maintenance, Regional, ERPNext Integrations, Quality Management, Communication, Telephony, Bulk Transaction, Subcontracting and EDI.

The source snapshot contains 549 JSON files under `doctype` folders (plus 96 chart-of-accounts JSON files). This is a useful indicator of breadth, **not** a KIYA feature-parity count. The largest business areas by DocType JSON file count are Accounts (291), Stock (82), Manufacturing (50), Setup (43), CRM (28), Assets (26), Selling (22), Buying (20), Quality Management (16), Projects (15), and Subcontracting (13).

| Source area | Principal verified components | What they do together | KIYA mapping / assessment |
| --- | --- | --- | --- |
| `erpnext/setup` | Company, Branch, Department, Employee, UOM, territory, defaults and master configuration | Provides enterprise context and frequently referenced masters. | Candidate foundations for SF-001/SF-003/SF-013; KIYA organization-context policy remains TBD. |
| `erpnext/crm` and `erpnext/selling` | Lead/Opportunity, Customer, Quotation, Sales Order, sales team and pricing-related records | Captures commercial activity and turns quotations/orders into downstream delivery/invoice actions. | Candidate for CRM/Sales and DEP-001/002/005; KIYA lead lifecycle/customer 360/order controls need specification. |
| `erpnext/buying` | Supplier, Supplier Quotation, Purchase Order and purchase-related records | Connects supplier sourcing and commitments to receipts and supplier invoices. | Candidate for Procurement/Supplier Management and DEP-005/006; scorecard/contract/portal behavior remains TBD. |
| `erpnext/stock` | Item, Warehouse, Bin, Batch, Serial No, Material Request, Purchase Receipt, Delivery Note, Stock Entry, Stock Ledger Entry, Quality Inspection | Tracks inventory movements and availability across inbound, internal and outbound steps. | Strong candidate for Inventory/Warehouse and customer/procure flows; reservation, valuation and exception policy are OQ-007. |
| `erpnext/manufacturing` and `erpnext/subcontracting` | BOM, Routing/Operations, Workstation, Work Order, Production Plan, subcontracting records | Explodes material/process requirements, plans work and produces stock movements. | Candidate for Manufacturing/MRP; demand/capacity/exception behavior is OQ-008. |
| `erpnext/quality_management` plus stock quality records | Quality goals/procedures/reviews/action components; `Quality Inspection` is used in stock transactions | Adds inspection/gate-related records around materials and production. | Candidate for Quality/DEP-004; acceptance, disposition, NCR and CAPA rules are OQ-009. |
| `erpnext/accounts` | Chart of Accounts, GL Entry, Sales Invoice, Purchase Invoice, payments, tax/accounting records, budgets | Financial posting and receivable/payable effects connect commercial and supply documents to accounting. | Highest-value candidate for Finance/Tax/DEP-005; accounting/tax policy and jurisdictions remain TBD. |
| `erpnext/assets` and `erpnext/maintenance` | Asset, depreciation/lifecycle records, maintenance schedules and visits | Associates equipment assets with maintenance planning/activity and financial asset treatment. | Candidate foundation for Asset Management; KIYA Asset-to-Service has material gaps in warranty, dispatch, spares, service billing and mobile (OQ-011/013). |
| `erpnext/projects` | Project, Task, Activity Type, project accounting/timesheet-related records | Organizes work and can connect activity/cost/billing to finance. | Candidate for Projects and DEP-008; KIYA resource/budget/billing details are TBD. |
| `erpnext/support`, `communication`, `telephony`, `portal` | Support, communication, phone and portal-oriented components | Offers possible service/customer interaction building blocks. | Partial evidence only for KIYA Customer Service, omnichannel communication and E-Commerce; validate independently. |
| `erpnext/regional`, `erpnext/erpnext_integrations`, `edi` | Country overrides and selected external/EDI integrations | Adjusts or connects specific upstream capabilities. | Do not reuse as a generic compliance/integration solution; applicability, current law, counterparty contracts and maintenance must be verified. |

## How the verified components connect in the three KIYA flows

The following is a **component relationship map**, not a claim that ERPNext exactly implements each BRD stage.

| BRD flow | Likely ERPNext component chain | Important effect and boundary |
| --- | --- | --- |
| Customer-to-Cash | CRM Lead/Opportunity → Customer/Quotation → Sales Order → Item/Warehouse/availability and, where needed, Material Request/Production Plan/Work Order → Quality Inspection → Stock Entry/Delivery Note → Sales Invoice → payment/GL entries | Selling, stock, manufacturing and accounts controllers link commercial documents to inventory and accounting. KIYA’s availability/reservation, production release, quality disposition, workflow, tax and customer-history rules must be proven/specifed first. |
| Procure-to-Pay | Supplier → Supplier Quotation → Purchase Order → Purchase Receipt → Quality Inspection → Stock/Stock Ledger → Purchase Invoice → payment/GL entries → supplier-related reporting | Buying, stock, quality and accounts link purchasing to receipt, valuation and accounts payable. KIYA approval, supplier-performance, compliance and exception rules remain unapproved. |
| Asset-to-Service | Asset → maintenance schedule/visit → parts through Item/Stock Entry → finance effects as applicable | The snapshot proves asset and maintenance modules, but not a complete KIYA chain for installation, warranty entitlement, request intake, technician dispatch, mobile/offline execution, service invoice/payment and full asset history. Treat this as a PoC/customization candidate, not a ready-made flow. |

## Concrete source-level flow evidence

Selected controller files contain lifecycle methods and/or helper calls for submit, cancel, validation, stock or accounting behavior:

- `erpnext/selling/doctype/sales_order/sales_order.py`
- `erpnext/buying/doctype/purchase_order/purchase_order.py`
- `erpnext/stock/doctype/purchase_receipt/purchase_receipt.py`
- `erpnext/stock/doctype/delivery_note/delivery_note.py`
- `erpnext/stock/doctype/stock_entry/stock_entry.py`
- `erpnext/manufacturing/doctype/bom/bom.py` and `work_order/work_order.py`
- `erpnext/stock/doctype/quality_inspection/quality_inspection.py`
- `erpnext/accounts/doctype/sales_invoice/sales_invoice.py` and `purchase_invoice/purchase_invoice.py`
- `erpnext/assets/doctype/asset/asset.py`
- `erpnext/projects/doctype/project/project.py`

This is why reuse must occur at a coherent domain/component boundary. A document’s JSON schema, controller, links, reports, hooks, permissions, fixtures, tests and upgrade migrations together form its operational behavior.

## Technologies observed in the inspected source

| Layer | Verified technology or dependency | Scope / caution |
| --- | --- | --- |
| Application framework | Frappe Framework 17 development line required by Bench dependency | Separate upstream application/framework dependency; no version has been approved for KIYA. |
| Backend/domain code | Python; source declares Python `>=3.14` for this development snapshot | Do not infer a supported production KIYA runtime from a development branch. |
| Data/application model | Frappe DocType JSON metadata, Python `Document` controllers and ORM | Frappe documentation describes MariaDB as default and Postgres support as beta; database selection is not made here. |
| ERP client | Frappe Desk assets plus ERPNext JavaScript/SCSS under `erpnext/public` | The source does not establish a KIYA UI/UX architecture. |
| Dedicated Banking UI | `banking/`: TypeScript, React 19, Vite 8, Tailwind 4, `frappe-react-sdk`, Jotai, TanStack Table/Virtual, React Hook Form, Radix, dnd-kit and other UI libraries | Isolated banking sub-application, not evidence that all ERPNext UI is React or that KIYA should adopt these technologies. |
| Asynchronous work | Frappe queues/scheduler; documentation identifies Python RQ background jobs and default short/default/long queues | Capacity, retries, idempotency, observability, SLAs and failure policy are KIYA TBD. |
| Realtime | Frappe realtime publish/subscribe; documentation identifies Node.js and Socket.IO | Candidate plumbing for user feedback/notifications, not a KIYA delivery guarantee. |
| Integration | Generated DocType REST endpoints, whitelisted RPC methods, webhooks, file endpoints and extension hooks | Needs KIYA-owned contract/version/auth/error/audit policy. |
| ERP package dependencies | Python: Unidecode, barcodenumber, rapidfuzz, holidays, Google Maps client, Plaid client, YouTube client, pypng, mt-940 and pdfplumber; JavaScript package declares `onscan.js` | Inspect transitive dependencies, licences, vulnerabilities, data processing and regional applicability before adoption. |
| Quality controls | Ruff configuration, pre-commit configuration, Semgrep configuration and 524 Python test files found | Useful upstream engineering practices, but KIYA needs an independent test/acceptance/security strategy. |

## Reuse recommendation by boundary

| Boundary | Recommendation | Reason / gate |
| --- | --- | --- |
| Frappe primitives: DocTypes, links, permissions, hooks, queued work, files, timelines, generated API | **Evaluate first in a disposable P0 lab** | They are generic foundations relevant to KIYA shared foundations. Confirm tenant/isolation, security, custom-app upgrade, API ownership and operations before reliance. |
| ERPNext accounting, buying, selling, stock, manufacturing, quality, assets and projects | **Selective domain reuse candidate** | Most useful established ERP value, but assess coherent flows, extension seams and accounting/compliance correctness; do not reuse isolated screens. |
| ERPNext master data | **Map before reuse** | KIYA requires no duplicate masters, but final ownership/lifecycle/status/field definitions are OQ-002. Never import/copy upstream masters as KIYA truth by default. |
| Workflows, notifications, audit and permissions | **Foundation candidate, gap analysis mandatory** | Frappe provides primitives; KIYA needs a suite-wide KIYA Engine, channel policy, escalation/delegation and comprehensive audit/security controls. |
| Support/portal/telephony/E-Commerce | **Separate assessment/PoC** | Source presence is not evidence of equivalence with KIYA Customer Service, Marketing or E-Commerce requirements. |
| Regional tax, EDI and integrations | **Use only after legal/current-regulation and counterpart validation** | Compliance and integration behavior change over time and is scope-dependent. |
| Banking React application | **Do not generalize** | It is an independently packaged feature UI with its own stack, not a platform-wide UI contract. |
| Native mobile, offline sync, AI/RPA/ML, EPM, enterprise DMS, SaaS control plane | **Build/buy/design later; no reuse conclusion** | The current source does not prove satisfaction of KIYA requirements. Follow the existing P1/P2 PoCs after authorization. |

## Safe investigation sequence before any implementation

1. Obtain explicit authorization for the technology/architecture evaluation and specialist GPL/trademark/commercial-model advice.
2. Pin released, compatible Frappe/ERPNext versions; do not base a decision on the inspected `17.0.0-dev` snapshot.
3. Execute the P0 experiments in `20-erpnext-poc-plan.md`: one bounded flow via a custom app, shared masters/multi-company permissions, site-per-tenant operation and licence review.
4. Establish a no-core-modification rule for the lab; catalogue every extension point, upstream contract and upgrade/migration impact.
5. Test the full lifecycle of each proposed component: create → validate → approval/workflow where applicable → submit → downstream ledger/event effect → cancel/amend → audit/report/integration behavior.
6. Convert results into evidence only. Route new business behavior through OQ/CD governance and a later authorized architecture decision; do not silently change BRD requirements.

## Validation performed

- Read the project Markdown documentation and the governing project-context records; reconciled the new assessment with the BRD-first, technology-neutral Phase 0 boundary.
- Confirmed the project has no application implementation to compare or harvest locally.
- Inspected ERPNext source layout, `modules.txt`, `hooks.py`, representative domain controller files, Python/JavaScript manifests, licence file, source version, module/DocType counts and test-file count at the recorded commit.
- Preserved all existing approved requirements and decisions. No code, dependency, architecture, API, UI, database, infrastructure, AI-model or platform decision has been made.
