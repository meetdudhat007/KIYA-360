# KIYA 360 - ERPNext / Frappe Framework Feasibility Assessment

## Status and boundary

**Assessment recommendation - not yet an approved KIYA 360 architecture decision.** This assessment is based on KIYA 360 BRD v2.0 (prepared 13 September 2026), its 28 modules, 238 baseline requirement records, three named flows, and current official Frappe/ERPNext materials. It creates no application design, does not resolve OQ-001 to OQ-015, and does not select a platform.

KIYA is an enterprise unified CRM + ERP + manufacturing + accounting + GST + BI/EPM platform, not a manufacturing-only product. The BRD requires one conceptual data model, multi-company/country/currency/language operation, and Customer-to-Cash, Procure-to-Pay, and Asset-to-Service flows. Detailed operating behavior remains unspecified in the current BRD where the OQ register says it is TBD.

## Evidence standard

**Verified** denotes an official document or upstream repository. **Partially verified** means the named capability is documented but KIYA-equivalence is not. **Inferred** is a bounded architectural conclusion. **Unknown / prototype required** means the available evidence cannot responsibly establish fitness. Feature-name similarity is not treated as equivalence.

## Verified platform facts

Frappe documents an application model in which apps are installed on a bench and sites are tenants. Its Sites guide describes each tenant as a site; the current Frappe architecture guide describes sites as separately database-backed, while apps can be shared across sites. The framework documents DocTypes, role-based document permissions, REST/RPC APIs, hooks for document events/permissions/method overrides, client/form scripts, migrations, and background jobs. This is a capable framework foundation, but also establishes the conventions that KIYA would need to own and operate.

ERPNext is a Frappe application whose official repository and documentation demonstrate mature ERP domains, including accounting, selling, buying, stock, manufacturing, quality, assets, projects, and HR-related ecosystem capability. This is **partially verified** fit for KIYA: the BRD’s detailed workflows, controls, mobile behavior, AI governance, and non-functional targets remain TBD and cannot be proven equivalent from module names.

## Cross-module flow assessment

| BRD flow | Evidence-based fit | Main boundary / uncertainty |
| --- | --- | --- |
| Customer-to-Cash | **B - Good fit with configuration/custom app.** ERPNext documents CRM/selling, stock, manufacturing, quality, accounting, and report capabilities that map to many named stages. | Reservation, availability/shortage behavior, MRP release, quality disposition, tax-country rules, approvals, and customer-history behavior are KIYA TBDs (OQ-002/003/005/007-009). A prototype must prove the actual orchestration rather than merely screen coverage. |
| Procure-to-Pay | **B.** Buying, supplier, receipt, quality, stock, accounting, and tax foundations are documented. | Supplier scorecard measures, inspection/NCR rules, tax jurisdiction/filing scope, approval rules, and integration behavior are not specified by KIYA. E-invoicing/e-way bill requires current jurisdiction-specific validation. |
| Asset-to-Service | **C - Significant customization.** Asset and maintenance foundations exist, with stock and accounting links available for reuse. | KIYA requires installation, warranty, technician dispatch, spare-parts, service invoicing/payment, and asset-history business rules; OQ-011 remains blocking. Field-service/mobile/offline details need a prototype. |

Shared workflow, documents, APIs, permissions, files, audit timeline, and scheduling are useful Frappe foundations. Their presence does not prove KIYA’s universal KIYA Engine workflow, omnichannel notifications, enterprise DMS, native offline apps, AI layer, or measurable 24/7/security targets.

## Unified data model and organization context

**Partially verified.** Frappe’s DocType/link model and ERPNext’s shared Company, Customer, Supplier, Item, Warehouse, Employee, Asset, Tax, Currency, and UOM concepts are compatible with KIYA’s intent to avoid duplicated masters. They do not guarantee KIYA’s final model: ownership, fields, lifecycle, validation, and cross-module semantics remain OQ-002. ERPNext’s Company and permission concepts provide a useful starting point for multi-company and role-based access, but branch/context policy and data-level rules require configuration and KIYA-specific validation.

## Future SaaS assessment

**Verified foundation, unproven product readiness.** Frappe documents multi-tenancy through sites and hostname routing, with separate site databases and shared bench apps. Frappe Cloud also documents site creation, backups, migration, and horizontal application-server scaling. This supports a credible site-per-tenant direction for independent-company isolation.

However, KIYA must not equate this with arbitrary-scale SaaS readiness. Tenant provisioning, billing, tenant-specific configuration, cross-tenant operations, application-version rollout, worker/queue isolation, file retention/export/deletion, disaster recovery, monitoring, support operations, domain policy, and regulatory residency need an explicit product/operations design. The BRD does not currently define these. A shared application codebase also makes upgrade testing and version compatibility an ongoing product obligation.

## Product ownership and platform options

| Option | Benefit | Primary risk | Assessment |
| --- | --- | --- | --- |
| Full custom backend | Maximum domain, API, UX, AI, and tenant-model control. | Very High initial delivery and ERP correctness effort; mature ERP controls must be rebuilt and maintained. | Suitable only if KIYA’s differentiated model is so deep that reuse cannot be isolated. |
| ERPNext as primary backend | Fastest reuse of mature transactional ERP domains. | High coupling to ERPNext DocTypes, workflows, UX assumptions, upgrades, and GPL distribution analysis. | Strong for a single-company acceleration path; risky as the entire long-term product boundary. |
| Frappe + selective ERPNext capabilities | Reuses framework and high-value ERP domains while keeping KIYA custom applications intentional. | Still has Frappe conventions, operational, upgrade, and licence dependencies. | Best balanced candidate, subject to PoCs and legal review. |
| Frappe + mostly custom KIYA apps | Strong framework productivity and greater KIYA identity. | Rebuilds much of the ERP value, while retaining framework lock-in. | Consider when ERPNext model mismatch is demonstrated by PoCs. |

**ASSESSMENT RECOMMENDATION - NOT YET AN APPROVED KIYA 360 ARCHITECTURE DECISION:** investigate Frappe Framework with selective, isolated ERPNext reuse as the leading reversible option. Treat ERPNext as reusable domain capability, not KIYA’s product boundary. Use adapters/service boundaries and an independently owned KIYA API, tenant/control plane, product UX, domain rules, AI governance, analytics strategy, billing/subscription operations, observability, and security policy. Confidence: **Medium** because KIYA’s critical workflow/data/tax/mobile/NFR decisions are unresolved and the decisive integration/upgrade/load evidence requires PoCs.

## Customization, upgrades, API, and security

Frappe officially supports custom apps, DocTypes, form/client scripts, hooks, document-event handlers, custom permission logic, scheduler/background jobs, and whitelisted REST/RPC methods. These mechanisms make a no-core-modification strategy feasible **in principle**. Using them is preferable to editing upstream core. Overrides of core DocTypes or whitelisted methods are higher-risk because upstream changes can alter assumptions; every upstream upgrade needs migration rehearsal, regression testing of custom apps, and compatibility review.

Frappe’s documented REST/RPC APIs and extension hooks mean KIYA can expose KIYA-specific contracts. That is an **inference**, not a guarantee: avoid publishing raw ERPNext DocType contracts as the external product API, otherwise ERPNext internals become hard-to-change customer dependencies. Permissions, sessions, audit/timeline, and API primitives are verified framework capabilities; encryption, device controls, security monitoring, tenant operational isolation, and KIYA’s exact RBAC/data policy need configuration and additional security engineering. No security guarantee or performance benchmark is established here.

## Mobile, AI, BI/EPM, documents, integration, tax, and scale

- **Mobile/offline: U / prototype required.** Frappe web and APIs do not by themselves verify native mobile apps, offline stores, synchronization conflicts, or field-service execution needed by KIYA. Build or integrate a dedicated mobile layer only after a targeted PoC.
- **AI/automation: C.** Framework automation/background jobs are useful plumbing, not proof of AI insights, forecasting, RPA, anomaly detection, chat, or ML governance. KIYA should retain AI boundaries and data-access/human-review policy independently; external or separate AI services remain an assessment option, not a decision.
- **BI/EPM: C.** ERPNext/Frappe reporting/dashboards are useful transactional reporting foundations. Enterprise planning, scenario/consolidation, predictive analytics, high-concurrency BI, and a governed semantic model are not established as native equivalents; assess an independent analytics layer.
- **Documents: B/C.** File attachments, links, permissions, and timeline/audit are useful. Enterprise DMS versioning, e-signature, retention, search/preview, storage, and compliance behavior require capability-by-capability validation.
- **Integration: B.** REST/RPC, files, hooks, background jobs, and events support integrations. KIYA-specific API governance, counterparties, webhooks, failure handling, monitoring, and data contracts remain OQ-012.
- **India tax: B/U.** ERPNext has India-oriented tax/compliance materials and capabilities, but legal/tax compliance is time-sensitive. GST, e-invoice, e-way bill, filing, and each required jurisdiction must be verified against current official government and ERPNext materials before reliance.
- **Performance/scalability: U.** Frappe documents process separation, queues/caching, multi-site hosting, and horizontal application-server scaling. No KIYA workload, tenant count, throughput, latency, reporting volume, or recovery target exists; load, failure, and upgrade testing are mandatory.

## Licensing assessment

**Technical/licensing assessment only - legal counsel required before final commercialization structure.** Frappe’s current official licence/trademark policy identifies Frappe Framework as MIT and ERPNext as GPLv3; it also identifies newer applications such as Frappe CRM and Helpdesk as AGPLv3 and directs users to the applicable repository for other applications. Therefore each exact version, tag, and additional app must be inventoried before use. MIT is permissive, while GPL licensing does not itself prohibit paid internal use or hosted SaaS; distribution/conveyance of covered or derivative work can create source-availability and licence obligations. Whether KIYA custom apps are separate works, derivative works, or are distributed with covered components is fact-specific; hosted operation, customer deployment, redistribution, modifications, trademarks, third-party applications, and commercial terms need specialist legal review before the product model is chosen.

## Red flags and green flags

**Red flags:** potential GPL/commercialization structure; ERPNext data/workflow/API coupling; custom-app upgrade and migration burden; undefined tenant control-plane and operations; unproven offline mobile; incomplete proof for AI, EPM, enterprise DMS, and measurable NFRs; India compliance maintenance; and a specialised Frappe/ERPNext learning/hiring/operating burden.

**Green flags:** documented multi-site architecture; reusable ERP transactional domains; multi-company and permissions foundations; a linked DocType model compatible with a shared-master direction; mature extension points; REST/RPC APIs; migration tooling; background jobs; and documented cloud backup/migration/scaling operations.

## Decisions for a future SaaS direction

| Must decide now | Should design for now | Can defer | Must not decide yet |
| --- | --- | --- | --- |
| Product boundary, legal licensing review path, tenant-isolation model to validate, API ownership, and whether the first deployment must preserve a SaaS exit path. | Independent API contracts, no-core-modification rule, upgrade/test discipline, tenant lifecycle/control-plane boundaries, observability/security seams, and data export/portability. | Provider, final deployment topology, analytics/AI vendor, exact billing system, and performance targets until requirements/PoCs supply evidence. | Selecting ERPNext/Frappe/custom backend as approved architecture; precise schemas, framework versions, cloud, mobile technology, AI model, or implementation architecture. |

## Final answers

**Q1 - build all ERP from scratch?** Not the default: it maximizes control but discards substantial reusable ERP capability and creates very high time-to-first-deployment and maintenance risk.

**Q2 - simply adopt ERPNext as backend?** Not without boundaries: it is valuable reuse but likely creates excessive long-term coupling for KIYA’s differentiated SaaS ambition.

**Q3 - use Frappe with selective ERPNext reuse?** This is the leading assessment candidate, pending legal review and the PoCs in `20-erpnext-poc-plan.md`.

**Q4-Q7 - safest direction and ownership?** Keep KIYA’s tenant/product model, UX, API contracts, orchestration rules, AI/analytics strategy, integrations, billing, security policy, and observability independently owned; selectively reuse well-proven ERP accounting/stock/procurement/manufacturing/quality/assets/projects foundations.

**Q8 - legal review?** Exact upstream/app licences, deployment versus distribution, custom-app relationship, customer delivery model, source obligations, trademark, and third-party integrations.

**Q9 - proof before decision?** Flow orchestration, shared-master/multi-company permissions, site-per-tenant operations, mobile offline, upgrade/custom-app compatibility, workload/security isolation, tax compliance, BI/EPM, and API boundary.

## Sources

1. KIYA 360, `source/KIYA360_BRD.pdf`, v2.0, 13 September 2026 (internal baseline).
2. Frappe, [Sites](https://docs.frappe.io/framework/user/en/guides/basics/sites) and [Create a Site](https://docs.frappe.io/framework/user/en/tutorial/create-a-site) (multi-site concepts).
3. Frappe, [Architecture overview](https://docs.frappe.io/customer-guide/scalability/architecture-overview), [Hooks](https://docs.frappe.io/framework/user/en/python-api/hooks), [REST API](https://docs.frappe.io/framework/user/en/guides/integration/rest_api), and [Database migrations](https://docs.frappe.io/framework/user/en/database-migrations).
4. ERPNext, [official repository](https://github.com/frappe/erpnext), [GPL-3.0 license text](https://github.com/frappe/erpnext/blob/develop/license.txt), [Manufacturing](https://docs.frappe.io/erpnext/manufacturing), and [Quality Management](https://docs.frappe.io/erpnext/quality-management).
5. Frappe, [License and Trademark](https://docs.frappe.io/legal/others/license-and-trademark) and [What open source means](https://docs.frappe.io/customer-guide/about-frappe/what-open-source-mean-for-you) (current licence distinctions).
6. Frappe Cloud, [site backups](https://docs.frappe.io/cloud/sites/backups), [site migration](https://docs.frappe.io/cloud/site/site-migrations/introduction-to-site-migration), and [application-server horizontal scaling](https://docs.frappe.io/cloud/application-server-horizontal-scaling).
