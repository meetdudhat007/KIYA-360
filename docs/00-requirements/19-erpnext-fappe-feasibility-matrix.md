# KIYA 360 - ERPNext / Frappe Feasibility Matrix

**Assessment-only classification.** A/B/C/D/E/U describes assessed platform fit, not KIYA requirement approval. `TBD` means KIYA behavior is not specified in the BRD and must not be inferred.

## 28-module fit matrix

| # | KIYA module | ERPNext/Frappe evidence and fit | KIYA-specific gap / main risk |
| --- | --- | --- | --- |
| 01 | Platform & Administration | **B.** Frappe DocTypes, roles/permissions, sessions, form controls, APIs, files, and audit timeline are verified foundations. | KIYA’s exact MFA/device/IP/data-level/audit policy is TBD; security monitoring needs additional engineering. |
| 02 | CRM | **B.** ERPNext CRM domain is reusable. | Customer 360 semantics, lifecycle, and cross-suite history need validation. |
| 03 | Sales | **B.** Selling, quotation, order, invoicing, stock/accounting links are reusable. | Availability, reservations, pricing, exceptions, and approval behavior are OQ-003/007. |
| 04 | Marketing | **C.** Campaign-related capability exists in the ecosystem; evidence for full KIYA channel/event/analytics behavior is incomplete. | Do not infer digital marketing, events, or attribution behavior. |
| 05 | Customer Service | **C/U.** Ticket/service foundations may be available, but complete SLA/knowledge/feedback/escalation equivalence is not established. | No BRD flow mapping; validate separately. |
| 06 | Procurement | **B.** Buying, RFQ, supplier quotation, PO, receipt, returns, stock/accounting are strong reuse candidates. | KIYA approvals, sourcing rules, and exception behavior are TBD. |
| 07 | Supplier Management | **B/C.** Supplier master and purchasing relationships are reusable. | Classification, contracts, scorecard measures, and portal behavior require custom work (OQ-010). |
| 08 | Inventory | **B.** Item, stock, serial/batch, transfer, valuation foundations are reusable. | Reservation, shortage, valuation-policy behavior needs business decision and PoC. |
| 09 | Warehouse | **B/C.** Warehouse/stock operations are reusable. | KIYA bin, inbound/outbound, pick-pack-ship, and WMS execution detail is unspecified. |
| 10 | Manufacturing | **B/C.** BOM, routing, work-order and production functions are documented in ERPNext. | Shop-floor, costing, co-products, planning release and exceptions require validation. |
| 11 | MRP & Planning | **C.** Useful planning/manufacturing foundation exists. | Demand/capacity/supply/schedule behavior is OQ-008; fit cannot be assumed. |
| 12 | Quality | **B/C.** Quality-management foundation is documented. | Acceptance, disposition, NCR/CAPA lifecycle, and quality gates are OQ-009. |
| 13 | Asset Management | **B.** Asset/depreciation foundations are reusable. | KIYA classification, valuation, lifecycle detail needs fit review. |
| 14 | Maintenance & Field Service | **C.** Maintenance/asset/stock foundations are useful. | Dispatch, warranty, contracts, billing, field execution and mobile needs are OQ-011/013. |
| 15 | Logistics & Transportation | **C/U.** Delivery/stock foundations exist. | Freight, carriers, tracking, proof of delivery, and transport planning need evidence/PoC. |
| 16 | Projects | **B.** Project, time/expense, and accounting foundations are reuse candidates. | Resource, budget, billing, and analytics workflow detail is TBD. |
| 17 | Finance & Accounting | **A/B.** ERPNext’s core accounting domain is a principal reuse value. | KIYA accounting policy, reporting, controls, country scope, and approval design need validation. |
| 18 | Tax & Statutory Compliance | **B/U.** India-oriented ERPNext capabilities are relevant. | Every tax rule, e-invoice/e-way bill, statutory filing, and further country coverage must be current-verified (OQ-005). |
| 19 | HR & Payroll | **C/U.** HR-related functionality exists in Frappe ecosystem, but it is not assumed to satisfy KIYA. | Payroll/statutory calculations and country scope are OQ-006. |
| 20 | E-Commerce | **C/U.** Storefront/portal linkage may be reusable. | Catalog, cart, checkout, promotions, gateway, and customer experience require separate assessment. |
| 21 | Document Management | **C.** Frappe files, links, permissions, and timeline are useful. | Enterprise versioning, DMS workflow, e-signature, search/preview/retention are not proven equivalents. |
| 22 | Business Intelligence | **C.** Reports/dashboards are useful transactional BI foundations. | KPI, ad-hoc, predictive, mobile BI and workload scale require separate analytics design. |
| 23 | EPM / Budget / Forecast | **C/U.** Budget/financial controls offer partial reuse. | Forecasting, scenarios, consolidation, variance and enterprise planning equivalence not established. |
| 24 | Workflow & Approvals | **B/C.** Frappe workflows, permissions, notifications, hooks, and audit are strong primitives. | KIYA’s universal no-code engine, escalation/delegation/matrices/mobile rules are OQ-003/004. |
| 25 | AI & Automation | **C/U.** Jobs, automation primitives, APIs are useful plumbing. | AI insights, ML, RPA, chat, anomalies and governance are OQ-014 and should not be coupled by assumption. |
| 26 | Integration & API | **B.** Frappe REST/RPC, whitelisted methods, hooks, file upload and background jobs are verified. | Stable KIYA contract, counterparties, webhooks, sync/error/monitoring policy are OQ-012. |
| 27 | Mobile Application | **U.** APIs support a mobile client. | Native offline app, sync/conflicts/push, field workflows and dashboard behavior are not verified by framework documentation. |
| 28 | Audit, Security & Compliance | **B/C.** Role/document permissions, sessions, audit timeline and hooks are useful. | KIYA policy/risk/monitoring, tenant operations, encryption/device/IP controls need explicit security design. |

## Shared-foundation fit

| KIYA foundation | Frappe capability | ERPNext contribution | Extension / limitation | Risk |
| --- | --- | --- | --- | --- |
| Organization / multi-company | Sites, roles, DocTypes | Company/accounting context | Branch/context policy must be configured and tested | Medium |
| Identity/RBAC | Users, roles, document permissions, hooks | Business-domain roles | KIYA data policy/security controls TBD | Medium-High |
| Shared masters | Linked DocTypes | Customer, Supplier, Item, etc. | Shared semantic ownership must be enforced by KIYA design | Medium |
| Workflow/notifications | Workflow primitives, scripts, hooks/jobs | Domain documents | Universal KIYA Engine behavior not automatically supplied | High |
| Documents/audit | File linkage, timelines | Domain-linked records | Not proven enterprise DMS/compliance suite | Medium-High |
| API/integration | REST/RPC, whitelisted methods, hooks | ERP transactions | Avoid exposing internal DocType contracts | Medium |
| Mobile/offline | Web/API basis | Transaction endpoints | Offline sync and native UX unproven | High |
| AI/automation | Jobs, events, APIs | Transaction data context | AI governance/model boundaries not native fit | High |
| BI/EPM | Reports/dashboards | Financial/transaction data | Planning/consolidation/high-scale analytics uncertain | High |

## Reuse versus build map

| KIYA capability | Reuse ERPNext | Reuse Frappe | Build KIYA-specific | External service | Unknown |
| --- | --- | --- | --- | --- | --- |
| Core accounting, AP/AR, stock, buying, manufacturing, quality, assets, projects | High candidate | Foundation | Boundary/adapters | Optional | Fit per OQ |
| Shared master/entity framework | Domain masters | DocTypes/links/permissions | Semantic ownership/governance | No default | Final fields/lifecycle |
| KIYA workflow engine | Partial document workflows | Hooks, jobs, permissions | Cross-module rules/orchestration | Notification channels as needed | OQ-003/004 |
| External API | Domain services behind adapter | REST/RPC | KIYA versioned contract | API gateway/monitoring candidate | OQ-012 |
| Mobile/offline | Transaction services | APIs/auth | Native client, sync/conflicts | Push/maps/device services candidate | OQ-013 |
| AI/analytics | Transaction data | Jobs/events | KIYA policies/orchestration | AI/warehouse/BI candidate | OQ-014/015 |
| Tenant/billing/control plane | No default product boundary | Sites/bench | Lifecycle/entitlements/operations | Billing/monitoring candidate | SaaS model |
| Documents/compliance | Attachments/context | Files/permissions | DMS controls/retention/audit policy | E-signature/storage/search candidate | Exact DMS scope |

## Core ownership map

KIYA should independently own product identity, tenant model and tenancy policy, customer experience, external API contracts, orchestration/domain rules that differentiate it, AI data/governance boundaries, analytics semantics, integration contracts, subscription/billing policy, observability, security policy, configuration model, and extension governance. ERPNext/Frappe should remain replaceable implementation capability behind these boundaries where practical.

## Transparent option matrix

Scores are qualitative directional assessments (1 weak/unfavourable; 5 strong/favourable), not measurements. They weight KIYA’s single-company acceleration and future SaaS independence equally; scores change if requirements/PoCs provide new evidence.

| Criterion | A Full custom | B ERPNext primary | C Frappe + selective ERPNext | D Frappe + mostly custom |
| --- | ---: | ---: | ---: | ---: |
| Development speed / ERP reuse | 1 | 5 | 4 | 2 |
| Control / data-model flexibility | 5 | 2 | 4 | 4 |
| KIYA differentiation / API/UI/AI independence | 5 | 2 | 4 | 4 |
| Cross-module transactional foundation | 2 | 5 | 4 | 3 |
| SaaS potential / tenant isolation basis | 4 | 3 | 4 | 4 |
| Upgrade and dependency risk | 4 | 2 | 3 | 3 |
| Licensing/commercialization simplicity | 4 | 2 | 2 | 2 |
| Team learning / operating burden | 2 | 3 | 2 | 2 |
| Long-term independent evolution | 5 | 2 | 4 | 4 |
| Overall assessment | 3 | 3 | **4** | 3 |

Option C leads because it retains material ERP reuse without treating ERPNext as KIYA’s public product boundary. It remains conditional on legal review and the PoCs; the licensing score reflects uncertainty, not a conclusion.

## Sources

See the source register in `18-erpnext-fappe-feasibility-assessment.md`; core evidence is the KIYA BRD, official Frappe Sites/Architecture/Hooks/API/Migrations documentation, official ERPNext repository/Manufacturing/Quality documentation, and official Frappe Cloud operational documentation.
