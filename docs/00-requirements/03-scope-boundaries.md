# KIYA 360 — Scope Boundaries

## 1. In Scope

The BRD explicitly includes the 28 modules catalogued in [the module inventory](02-module-inventory.md), their listed functional requirements, the three end-to-end flows, and the shared enablers: Workflow & Approvals, Document Management, AI & Automation, Integration & API, Mobile Application, and Audit, Security & Compliance. It also explicitly includes multi-company, multi-country, multi-currency, multi-language, 24/7 operations, scalable architecture, data security, and role-based access as global capabilities.

The BRD's common features include notifications/reminders (email, SMS, WhatsApp, push, and in-app), calendar, approval workflow, audit trail, document linking, web-mobile sync, RBAC, create/edit/view/duplicate, approve/reject/cancel, search/filter/sort, automatic numbering, attachments, PDF generation/print/share, Excel/PDF export, and a company/branch context switcher.

## 2. Explicitly Out of Scope

| Item | Classification | BRD basis |
| --- | --- | --- |
| Country-specific payroll/statutory calculations beyond India and one additional reference country | OUT-OF-SCOPE | BRD §3.2, Phase 1 |
| Deep industry-specific configurators, such as process/recipe manufacturing, beyond discrete/BOM-based manufacturing | OUT-OF-SCOPE | BRD §3.2, Phase 1 |
| Marketplace-specific storefront integrations beyond the native E-Commerce module | OUT-OF-SCOPE | BRD §3.2, Phase 1 |
| Data migration/cutover services from legacy Oracle/SAP/NetSuite instances | OUT-OF-SCOPE | BRD §3.2; separate implementation SOW |

## 3. TBD

- Detailed design depth for modules 02–28: the BRD states that these sub-module requirements should be expanded during detailed design.
- Field definitions, validation rules, status values, approval conditions, calculations, notification triggers, exception handling, permissions, and numbering formats: TBD — The BRD does not specify this detail.
- Integration counterparties, interfaces, data mappings, and operational behavior: TBD — The BRD does not specify this detail.
- AI decision boundaries, model governance, and evaluation: TBD — The BRD does not specify this detail.
- Tax-country coverage beyond Phase 1 India and one reference country: TBD — The BRD does not specify this detail.

## 4. Proposed

No recommendations are introduced in this Phase 0A baseline. Any later recommendation must be labelled **PROPOSED — Not a confirmed BRD requirement.**
