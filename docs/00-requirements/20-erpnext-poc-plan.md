# KIYA 360 - ERPNext / Frappe Proof-of-Concept Plan

## Purpose and boundary

This is an experiment plan, not an authorization to install, configure, integrate, or implement KIYA 360. It exists because documentation cannot establish KIYA fit for workload, upgrade, tenant, mobile, and detailed-business behavior. No KIYA business question is answered by a PoC unless formal clarification/approval governance is separately followed.

## Priority experiments

| Priority | Question | Why uncertain | Prototype test | Success criteria |
| --- | --- | --- | --- | --- |
| P0 | Can one KIYA core flow be orchestrated without ERPNext core changes? | Module names do not prove C2C/P2P behavior or custom-app upgrade safety. | Model a source-supported, non-final slice using a custom app and supported extension points; document touched upstream contracts. | Demonstrates required links/audit/permissions without core modification; every unsupported KIYA rule remains TBD. |
| P0 | Can shared masters and multi-company permissions remain coherent? | OQ-002 and KIYA’s no-duplicate-master requirement are unresolved. | Exercise Customer, Supplier, Item, Warehouse, Company, Employee, Asset, Tax, Currency and UOM links across two company contexts. | No unintended duplicate master or unauthorized cross-context read/write; limitations explicitly recorded. |
| P0 | Is site-per-tenant operation viable for the intended SaaS model? | Site isolation is documented; lifecycle, operability and cost are not KIYA-proven. | Create disposable representative tenants in an isolated lab; assess provisioning, domain routing, app versioning, backup/restore, export and deletion runbooks. | Tenant database/files/access separation is demonstrated; documented operational gaps and recovery evidence meet later-defined targets. |
| P0 | Is the licensing/commercial model viable? | GPL implications depend on actual apps, modification/distribution and contract structure. | Inventory exact versions/licences and proposed delivery paths; obtain specialist legal review. | Written legal position and acceptable contribution/distribution boundaries; no technical inference substitutes for counsel. |
| P1 | Can mobile offline safely support selected Sales/Service/Inventory/Approvals tasks? | Frappe API availability does not prove native offline sync or conflict semantics. | Build a throwaway client/lab simulation for a bounded, source-supported transaction sequence and intentional conflicting edits. | Auth, queued sync, conflict outcome, data minimization, audit, push and recovery are demonstrable against approved future requirements. |
| P1 | Can custom apps survive an upstream upgrade? | Hooks/extensions exist; compatibility burden is environment-specific. | Implement a representative extension only in a disposable lab; upgrade between chosen supported versions and execute regression suite. | Migration succeeds, no core patch is required, regressions are detectable, and effort is acceptable to governance. |
| P1 | Can reporting/background workload meet KIYA expectations? | No BRD workload or NFR targets exist. | Run controlled transactional, reporting, queue, integration and file-load profiles after NFR targets are approved. | Targets are met with observed latency/error/recovery evidence; otherwise capacity/design risk is recorded. |
| P1 | Are India tax/e-invoice/e-way bill requirements current and deployable? | Compliance changes; OQ-005 is unresolved. | Validate only approved jurisdiction/scenario scope against current official government and ERPNext documentation in a non-production environment. | Traceable compliance evidence, exception handling, update ownership, and legal/tax sign-off path exist. |
| P2 | Are BI/EPM/AI/DMS needs better served in-platform or independently? | Documentation does not establish enterprise planning, AI or DMS equivalence. | Compare a bounded source-supported report/document/automation scenario with independent-service patterns. | Evidence-backed boundary recommendation; no AI model/provider or architecture decision is made by the experiment. |

## Experiment governance

- Run only in a disposable, non-production environment after explicit authorization.
- No KIYA application code, production data, or BRD requirement behavior is changed by this plan.
- Use synthetic/minimized data and record app/version/licence evidence.
- Capture assumptions, exact extension mechanisms, upstream dependencies, results, failures, and rollback/deletion evidence.
- Route business-rule findings through the OQ/CD governance; route an eventual platform choice through an authorized architecture/technology decision process.
- Define measurable success thresholds only after the relevant OQ-015/NFR decisions are approved; do not invent benchmarks.

## Exit record required for each PoC

Record question, scope, source requirements, environment, exact versions/licences, test data category, steps, observed evidence, failure modes, upgrade/operating implications, unresolved items, recommendation, and reviewer. A successful PoC is evidence for a later decision, not an architecture approval.
