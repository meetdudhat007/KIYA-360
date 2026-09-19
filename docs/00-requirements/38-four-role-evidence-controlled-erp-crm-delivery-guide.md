# KIYA 360 — Four-Role, Evidence-Controlled ERP + CRM Delivery Guide

## Status and hard boundary

**PROPOSED delivery guide; not an approved architecture, implementation specification, UI specification, API contract, database schema, supplier decision, or legal opinion.** It translates the approved KIYA planning material and the verified ERPNext source assessment into a safe sequence of work for four delivery roles.

It deliberately does **not** name KIYA pages, buttons, API endpoints, database tables/columns, JSON contracts, MongoDB collections, AWS services, Razorpay, cloud provider, payment provider, or a technology stack as if they were requirements. The approved BRD does not specify those choices, and the current phase expressly defers them. Adding them here would be an unsupported design decision.

This guide is useful because it says exactly what evidence each role must obtain before those artifacts can be designed and built. The source baseline remains `source/KIYA360_BRD.pdf`, version 2.0. Existing open questions OQ-001 through OQ-015 remain unresolved.

## What is known, and what is not

| Topic | Verified KIYA position | Consequence |
| --- | --- | --- |
| Scope | The BRD defines 28 modules, 238 baseline requirement records, three named end-to-end flows, shared workflow/approval, audit, documents, integration, mobile, AI, BI/EPM and multi-entity capabilities. | Build planning must cover the whole platform, incrementally and with shared foundations first. |
| Business process detail | The BRD supplies broad capability scope for most modules; field rules, statuses, exceptions, approvals, notification events and detailed actors are mostly TBD. | Do not derive pages, buttons, database columns, JSON fields, backend calls or acceptance tests from ERP convention. Use a detailed-requirement record and decision gate first. |
| Application implementation | The KIYA repository currently contains no application code, database schema, API contract, UI specification, dependency manifest or deployment configuration. | There are no local components to extend or copy. |
| ERPNext reference | ERPNext/Frappe provides verified domain/component examples and extension mechanisms. Its exact inspected snapshot and reuse assessment are in document 37. | It is a research input and possible future reuse candidate, not KIYA’s approved design or product boundary. |
| Payment gateway | `FR-ECOM-005` requires a payment gateway. No provider, country, payment method, settlement behavior, refund/dispute handling, data-processing rule, or commercial contract is specified. | Razorpay is **TBD**, as is every other provider. Provider selection needs an approved requirement, security/privacy/legal review and procurement decision. |
| Cloud, database and data format | The BRD does not name AWS, any cloud provider, MariaDB, PostgreSQL, MongoDB, SQL tables, collections, or JSON API format. | All are **TBD** until an authorized architecture phase. No MongoDB schema should be created merely because it was requested. |
| ERPNext source mentions | The inspected source has Frappe DocType JSON metadata, Python controllers, REST/RPC mechanisms and a Razorpay help-link/logo reference in a Banking UI asset. | A source mention is not evidence that a provider is used, suitable, licensed for KIYA, or approved by KIYA. |

## Verified reference: how ERPNext/Frappe works

This is a concise reference model only. Full source evidence and reuse boundaries are in `37-erpnext-source-component-reuse-inventory.md`.

```text
User or integration
    -> Frappe REST document endpoint or whitelisted RPC method
    -> DocType metadata and document controller
    -> validation / submit / cancel lifecycle logic
    -> linked ERPNext domain records, accounting or stock effects where implemented
    -> audit/timeline, background work, realtime event or webhook where configured
```

ERPNext models records with **DocTypes**. Their JSON metadata describes fields, links, child rows, permission metadata and form behavior; Python controllers implement lifecycle logic. For example, ERPNext connects commercial records (Customer, Quotation, Sales Order), inventory records (Item, Warehouse, Delivery Note/Stock Entry) and financial records (Sales Invoice, Payment/GL records). These are useful verified *examples* of connected domain components, but are not KIYA schemas or approved KIYA processes. [Frappe DocTypes](https://docs.frappe.io/framework/user/en/basics/doctypes), [controllers](https://docs.frappe.io/framework/user/en/basics/doctypes/controllers), [REST/RPC APIs](https://docs.frappe.io/framework/user/en/guides/integration/rest_api)

Frappe also documents hooks, document-event handlers, scheduler/background jobs and configurable webhooks. These are framework capabilities; they do not determine KIYA’s workflow, integration, notification, AI, or security behavior. [Hooks](https://docs.frappe.io/framework/user/en/python-api/hooks), [background jobs](https://docs.frappe.io/framework/user/en/api/background_jobs), [webhooks](https://docs.frappe.io/framework/user/en/guides/integration/webhooks)

## The four roles

The roles are workstream responsibilities, not a claim about future job titles, headcount, tools or organization. They can be performed by different people or a governed team, but their outputs must be reviewed together.

| Role | Owns | Must not decide alone | Primary output |
| --- | --- | --- | --- |
| 1. Product and Domain Requirements Lead | BRD traceability, stakeholder clarification, process scope, priorities and acceptance evidence | Technology, database, UI, supplier or legal conclusions | Approved detailed requirements and approved clarification decisions |
| 2. Shared Data, Workflow and Integration Analyst | Cross-module concepts, dependencies, lifecycle evidence, integration/notification/API requirements and data-governance questions | Tables/columns, data store, endpoint format, workflow conditions, vendor selection | Conceptual data and dependency records; approved behavior needed for later contracts |
| 3. Experience and Application Delivery Lead | Page/action inventory, implementation decomposition, component boundary options and accessibility/usability evidence after requirements approval | Inventing buttons, screens, API calls, frontend/backend stack, or copying ERPNext material without licence review | Reviewable page/action and implementation backlog, each traceable to approved requirements |
| 4. Quality, Security, Legal and Operations Lead | Verification strategy, privacy/security/compliance review, licence controls, supplier due diligence, release/operating evidence | Business requirements, acceptance outcomes, tax/payroll rules, architecture selection without authority | Test/security/legal/operational evidence and release gate decision |

## Step-by-step delivery sequence

### Step 0 — Create the controlled evidence baseline

**All four roles participate.**

1. Record the exact BRD requirement(s), related `SF-*` shared foundations, `DEP-*` dependencies, and named flow for every proposed work item.
2. Read the relevant OQ record. If its answer is necessary, do not start detailed design; capture stakeholder input through the CD lifecycle in documents 15–17.
3. Label every statement: BRD-REQUIRED, BRD-DERIVED, PROPOSED, TBD, or OUT-OF-SCOPE. Do not use the last classification unless the BRD explicitly excludes it.
4. Keep a source log: BRD section, approved decision, official upstream document/source revision, and independent KIYA work product.
5. Gate: Role 1 confirms a reviewable requirement exists; Role 4 confirms that no unlicensed material or personal/production data is being introduced.

**Output:** an approved or clearly `Needs Clarification` detailed-requirement record using document 11’s template. No code, schema, page or API is created in this step.

### Step 1 — Specify the shared foundations before module screens

**Lead: Role 1 and Role 2; review: Roles 3 and 4.**

Work through these existing KIYA foundations together, because a module screen cannot safely define them independently:

| Foundation | BRD-backed conceptual scope | Key unresolved control |
| --- | --- | --- |
| Enterprise context | Company, Branch, Business Unit, Department, Division, Location; multi-company/country/currency/language | Context-selection and multi-entity access policy |
| Identity and access | Users, roles, permissions, authentication, device/session controls and encryption | Role model, MFA/device/IP policy and data-level access |
| Shared masters | Customer, Supplier, Item, Employee, Asset, Tax, Currency and UOM concepts | Ownership, lifecycle, fields and cross-module validation |
| Workflow, approvals and notifications | Workflow builder, approval matrix, escalation, delegation and communication channels | Conditions, limits, approvers, timing, recipients and templates |
| Audit, documents and security | Record/login audit, attachments/documents, policy/risk/security monitoring | Retention, signatures, review and security-operation policies |
| Integration, mobile, AI and analytics | API/data sync/webhooks; native mobile/offline; AI/automation; BI/EPM | Data scope, conflict handling, governance, measures and measurable NFRs |

**Output:** approved behavior and terminology at conceptual level. This is deliberately **not** an ER diagram, SQL schema, MongoDB collection design or API specification.

### Step 2 — Expand one complete, approved business slice at a time

**Lead: Role 1; coordination: Role 2; planned delivery: Role 3; verification: Role 4.**

Use the BRD’s flow order. Do not build a complete Sales screen before agreeing its upstream and downstream behavior.

| Slice | BRD sequence to analyze together | Existing dependency records |
| --- | --- | --- |
| Customer-to-Cash | Lead → Opportunity → Enquiry → Quotation → Sales Order → Availability Check → Inventory → MRP/Planning → Production → Quality Check → Warehouse → Dispatch → Invoice → Tax → Payment → Accounting → Profitability → Customer History | DEP-001–005 |
| Procure-to-Pay | Supplier → RFQ/RFP → Supplier Quotation → Purchase Order → Goods Receipt → Quality Check → Inventory → Supplier Invoice → Tax → Payment → Accounting → Supplier Performance | DEP-005–006 |
| Asset-to-Service | Asset/Machine → Installation → Warranty → Service Request → Technician Assignment → Spare Parts → Work Order → Maintenance → Service Invoice → Payment → Asset History | DEP-007 |
| Shared every-slice behavior | Workflow/approvals, notification, document, audit/security, integration, mobile and BI/EPM | DEP-009–011 and relevant SF records |

For each stage, Role 1 must establish from the BRD/approved decision: actor, trigger, permitted action, inputs, business validation, lifecycle, expected output, exception, approval, notification, audit and dependent masters. Any absent value is **TBD**—not inferred from ERPNext.

**Output:** a flow-ready set of approved detailed requirements, with open decisions explicitly blocking the next design step.

### Step 3 — Produce the page and action register only after behavior is approved

**Lead: Role 3; approval/evidence: Roles 1, 2 and 4.**

The BRD says records can have common create/edit/view/duplicate, search/filter/sort and approve/reject/cancel capabilities. It does **not** say which page exists, where a button appears, what it is called, what fields it has, or which roles can use it. Therefore, use this register for every future proposed page/action; do not populate unsupported cells.

| Required register field | Populate only from | Status today |
| --- | --- | --- |
| Page/view purpose and linked detailed requirement | Approved detailed requirement | TBD for all future pages |
| Actor and authorization | Approved role/permission decision | TBD |
| Record data displayed/edited | Approved data requirements | TBD |
| User action/button | Approved business action and lifecycle rule | TBD |
| Validation/error/confirmation behavior | Approved requirement and exception policy | TBD |
| Server operation/API contract | Approved architecture and API requirement | TBD |
| Audit, notification, workflow and mobile effect | Approved shared-foundation requirement | TBD |
| Accessibility, localization and responsive/offline behavior | Approved NFR/mobile requirements | TBD |
| Acceptance test | Approved observable criterion | TBD where behavior is not specified |

ERPNext DocType forms and source pages can be studied for usability patterns only. Do not copy their JSON, client scripts, HTML, CSS, labels, layouts, button behavior or code into KIYA unless GPL-compatible reuse is explicitly authorized.

### Step 4 — Create the API and backend-operation catalog after architecture approval

**Lead: Role 2; implemented by Role 3; assured by Role 4.**

Frappe provides generated DocType REST endpoints and whitelisted RPC methods. That is a verified framework capability, not a KIYA API contract. KIYA must not expose upstream internal DocType structures as its product API by default.

For each approved user/system action, prepare a catalog record with these fields, but leave each substantive field TBD until the required decision exists:

| Catalog field | Why it is required |
| --- | --- |
| Requirement and flow traceability | Prevents an endpoint from becoming an invented feature |
| Initiator, authorization and company/context scope | Links API behavior to security and multi-entity decisions |
| Command/query intent and input/output business concepts | Defines behavior before transport/format choices |
| Transaction, idempotency, concurrency and error policy | Required for reliable state-changing operations; current KIYA behavior is TBD |
| Workflow, audit, notification, integration and mobile-sync effects | Makes cross-cutting behavior testable |
| External contract version, authentication, privacy and retention | Required before a third party or mobile app can rely on it |
| Technology/endpoint/JSON/schema implementation | **TBD pending architecture and detailed requirements** |

**Backend implementation rule:** a state-changing operation must be traced through validation, workflow/approval, persistence, downstream effects, audit, notification and integration consequences. This is a process-control rule, not an assertion of a particular API, transaction manager, queue or database.

### Step 5 — Design data schemas only when the data decision is approved

**Lead: Role 2; implementation: Role 3; assurance: Role 4; business approval: Role 1.**

At present, the BRD supplies conceptual data only. The following concepts are permitted as a **conceptual inventory**, not tables, collections, properties, IDs, indexes, JSON shapes or relationships:

| Concept group | BRD-mentioned concepts |
| --- | --- |
| Enterprise/master | Company, Branch, Business Unit, Department, Division, Location, User, Role, Customer, Supplier, Item, Employee, Tax, Currency, UOM, Warehouse, Asset |
| Core transactions | Lead, Opportunity, Enquiry, Quotation, Sales Order, Purchase Requisition, RFQ/RFP, Supplier Quotation, Purchase Order, Goods Receipt, Work Order, Inspection, Dispatch, Invoice, Payment, Service Request, Maintenance Work Order |
| Shared records | Approval, notification, document, audit event, integration event and analytics concepts are required at capability level; their field/lifecycle/storage details are TBD |

Before a schema is allowed, create a data-decision record for: business owner, purpose, authoritative master, lifecycle, uniqueness, relationships, company/context scope, data classification, retention, audit, access, integration ownership, migration/import rules, deletion/export needs, reporting use and approval evidence. Then select a data technology during the authorized architecture phase.

**MongoDB/JSON status:** no KIYA source or BRD evidence selects MongoDB. JSON is used by ERPNext/Frappe DocType metadata in the inspected source; that does not make JSON metadata, JSON APIs or a document database a KIYA requirement.

### Step 6 — Evaluate external and paid services through a supplier gate

**Lead: Role 4; requirements evidence: Role 1; technical fit: Roles 2 and 3.**

No external service may be added merely because it is common in ERP products or appears in ERPNext source. Apply the following gate separately to payment, cloud hosting, SMS/WhatsApp/email, maps, e-signature, analytics, tax/e-invoicing, identity, storage, monitoring and AI services.

| Supplier-gate question | Current KIYA answer |
| --- | --- |
| Which BRD requirement and approved behavior requires it? | Only the broad capability may be known; provider behavior is usually TBD. |
| Is a named provider required? | No provider is named in the BRD. |
| What countries, currencies, data categories, service level, support, cost and exit/portability terms are required? | TBD; obtain stakeholder decisions and procurement evidence. |
| What security, privacy, data-residency, subprocessor, retention and incident requirements apply? | TBD; requires security/privacy/legal review. |
| What payment/financial/tax/regulatory obligations apply? | TBD; requires current jurisdictional and specialist review. |
| Is the provider SDK/API licence compatible with KIYA’s delivery model? | TBD; inventory exact version and terms before adoption. |
| Is an alternative/exit path required? | TBD; decide in architecture/operations governance. |

**Named examples:** Razorpay and AWS are not selected. The BRD does name an E-Commerce payment-gateway capability, but its provider is TBD. Do not treat the source snapshot’s Razorpay asset/help reference as selection or adoption evidence. No AWS provider requirement was found in the BRD baseline.

### Step 7 — Build, test and release only after the preceding gates pass

**Role 3 builds; Role 4 verifies; Roles 1 and 2 accept requirement/data/flow evidence.**

For an authorized implementation increment, the minimum evidence chain is:

```text
Approved BRD requirement
  -> approved clarification decision where required
  -> detailed requirement and flow/dependency record
  -> approved page/action, API and data decisions
  -> implementation change
  -> automated and scenario evidence
  -> security/privacy/licence/operations review
  -> controlled release approval
```

The test set must verify the whole cross-module behavior, not only a page: authorization, validation, lifecycle transition, data change, downstream effect, workflow/approval, audit, notification, integration failure/retry, reporting/analytics effect, mobile/offline behavior where applicable, and cancel/amend/reversal behavior. Expected outcomes remain TBD until the business requirement defines them.

## Scope allocation across the four roles

Every named BRD module needs Role 1 requirement ownership, Role 2 dependency/data review, Role 3 delivery planning after approval, and Role 4 assurance. Lead focus is allocated below only to sequence analysis; it does not create requirements.

| Work group | KIYA modules | Primary lead |
| --- | --- | --- |
| Shared platform | Platform & Administration; Workflow & Approvals; Document Management; Integration & API; Mobile Application; Audit, Security & Compliance | Roles 1 + 2, with Role 4 gate |
| CRM and commercial flow | CRM; Sales; Marketing; Customer Service; E-Commerce | Role 1 |
| Supply and operations flow | Procurement; Supplier Management; Inventory; Warehouse; Manufacturing; MRP & Planning; Quality; Logistics & Transportation | Roles 1 + 2 |
| Financial/service/people flow | Asset Management; Maintenance & Field Service; Projects; Finance & Accounting; Tax & Statutory Compliance; HR & Payroll | Roles 1 + 2 with Role 4 specialist review |
| Intelligence and automation | Business Intelligence; EPM/Budget/Forecast; AI & Automation | Roles 1 + 2 with Role 4 governance review |

## ERPNext source study protocol and copyright controls

### What may be learned

- High-level ideas and independently developed business concepts, such as using a linked customer/order/invoice lifecycle or ensuring an inventory event affects availability, can inform questions and requirements research.
- Publicly documented Frappe mechanisms—DocTypes, controllers, REST/RPC, hooks, background jobs and webhooks—can be evaluated as potential platform capabilities.
- The repository structure, component names and test coverage can inform a future PoC scope.

### What must not happen without GPL-compatible authorization

- Copying, adapting, translating, reformatting or pasting ERPNext/Frappe GPL-covered source code, DocType JSON, client scripts, templates, CSS, tests, migrations, reports or derived artifacts into proprietary KIYA code.
- Treating a close, line-by-line or structure-by-structure rewrite as an independent implementation.
- Reusing ERPNext trademarks, branding, logos or documentation assets without checking the applicable terms.
- Assuming that a separately packaged KIYA extension is automatically outside the GPL when it is distributed with or depends intimately on ERPNext; obtain specialist advice for the actual structure.

ERPNext is GPL-3.0. GPL permits use, modification and commercial distribution, but distributed modified/combined works have licence and corresponding-source obligations. Whether KIYA code is a separate work or derivative in a particular delivery model is fact-specific legal analysis, not something this guide can decide. [ERPNext licence](https://github.com/frappe/erpnext/blob/develop/license.txt), [GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.en.html), [Frappe licence/trademark information](https://docs.frappe.io/legal/others/license-and-trademark)

### Mandatory provenance controls

1. Maintain an upstream-material register: repository, commit/tag, file path, licence, intended use and reviewer.
2. Keep KIYA design notes tied first to the BRD and approved decisions, not to copied ERPNext source.
3. Require peer review for any code with an upstream-derived idea; reject pasted or mechanically transformed GPL source from a proprietary path.
4. Run licence/dependency inventory and source/provenance scanning before every release.
5. Obtain qualified legal advice before choosing Frappe/ERPNext reuse, distributing a custom app, delivering on-premise software, or representing compatibility with ERPNext/Frappe.

## Decision gates that block the requested implementation detail

| Requested detail | Why it cannot truthfully be specified now | Required evidence before creating it |
| --- | --- | --- |
| Every page and button | Actors, fields, action applicability, lifecycle, approval and exception behavior are not specified for most capabilities | Approved detailed requirements and role/workflow decisions |
| Backend calls/endpoints | KIYA API boundary, authentication, integration counterparties, data sync and error policy are OQ-012/TBD | Approved architecture/API/integration requirements |
| SQL tables, JSON contracts or MongoDB collections | No data technology or detailed data attributes/relationships are approved | Approved master/data/lifecycle/security/retention decisions plus architecture authorization |
| AWS/cloud/deployment services | No cloud/provider/availability/recovery/region/cost policy is approved | Measurable NFRs (OQ-015), security/privacy/operations and procurement decisions |
| Razorpay/payment integration | Only a broad payment-gateway requirement is stated; provider/country/payment/refund/settlement rules are unspecified | E-commerce/payment requirements, jurisdiction/compliance, provider due diligence and contract approval |
| Exact ERPNext component copying | GPL, upgrade, architecture and KIYA-fit implications are unresolved | Legal review, platform decision, pinned version and authorized PoC evidence |

## Next safe action

Start stakeholder clarification group CG-01 (OQ-001/OQ-002) using document 15. It establishes scope and shared-master meaning, without which page inventories, backend calls and schemas would be speculation. In parallel, the existing document 20 P0 ERPNext/Frappe PoC plan may be considered only after explicit authorization and legal review.

## Validation performed

- Reconciled this guide against the BRD-first, technology-neutral detailed-requirement strategy and current clarification/decision controls.
- Confirmed the BRD specifies a payment gateway but names no provider, and specifies no AWS, MongoDB, database, cloud or API technology.
- Confirmed the inspected ERPNext source has Frappe DocType metadata and a Razorpay help/link-logo reference, but treated neither as KIYA product/provider evidence.
- Used only the existing approved KIYA requirement records, exact ERPNext source-assessment findings, and official Frappe/GNU reference material cited above.
- Created no KIYA code, schema, vendor integration, API, UI, technology choice, external account, payment service, deployment, or approved decision.
