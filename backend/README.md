# KNIT — backend

Two separate Frappe apps. Keep them separate.

| | `knit_core` | `knit_demo` |
|---|---|---|
| Purpose | The KNIT product | Client demo scaffolding |
| Runs on | Bare Frappe | Frappe + ERPNext + HRMS |
| Lifetime | Permanent | Throwaway after the pitch |
| Architecture | Candidate D (ADR-001 fallback) | Candidate C |

**The dependency runs one way: `knit_demo` may import `knit_core`. Never the reverse.**
If `knit_core` ever needs something from ERPNext, HRMS or `knit_demo`, that is a
design error — it means the product has become dependent on the demo.

## knit_core
- `brd_data.py` — values quoted from the BRD, plus clearly marked placeholders.
- `platform/` — BRD Module 01 enterprise context: `KNIT Company`, `KNIT Branch`,
  `KNIT Business Unit`, `KNIT Department`, `KNIT Division`, `KNIT Location`
  (`FR-PADM-1.1.1`..`1.1.6`). Every field traces to the BRD descriptor in its
  `description`; the BRD specifies no further detail, so gaps are marked TBD
  rather than invented.
- 15 module packages holding 61 doctypes, each field traced to a BRD or Phase 0B-2
  requirement ID in its `description`: `platform/`, `crm/`, `sales/`,
  `procurement/`, `supplier_management/`, `inventory/`, `warehouse/`,
  `manufacturing/`, `mrp/`, `quality/`, `asset_management/`, `maintenance/`,
  `finance/`, `tax/`.
- `business_status/` — the CD-002 lifecycle adapter. Framework-level; governs
  whatever doctype it is pointed at. `python -m unittest
  knit_core.business_status.test_business_status` runs without a site.
- `standalone/` — a no-Frappe preview of the lifecycle. `python run_preview.py`.

## knit_demo
- `demo_seed/` — seeds masters, the C2C and P2P chains, payroll, production,
  assets, an approval workflow and a dashboard. Every one of these touches
  ERPNext or HRMS doctypes.
- Run order: `seed.execute` → `operations.seed_production` → `flows.run_p2p` →
  `flows.run_c2c` → `platform.install_workflow` → `platform.install_dashboard`,
  then `verify.run` to check the result.

## Tests
`cd backend && python -m unittest discover -s knit_core -p "test_*.py" -t .`
runs 29 tests with no site. `test_link_targets_are_bare_frappe_safe` enforces
the rule above: a Link from `knit_core` to an ERPNext or HRMS doctype fails the
build.

## Status
Executed: the `knit_core` tests and the standalone preview. Not executed: the
doctypes have never been migrated onto a Frappe site, and everything in
`knit_demo` needs a real ERPNext site.

## Coverage, honestly

61 doctypes cover 58 of the 205 catalogued requirement IDs (28%). Not built:

- **No specifiable detail.** Marketing (04), Customer Service (05), Logistics (15),
  Projects (16), HR & Payroll (19), E-Commerce (20). The BRD names these
  requirements and no Phase 0B-2 record elaborates them. Building fields would
  mean inventing requirements, which `AGENTS.md` forbids.
- **Capabilities, not entities.** BI (22), EPM (23), Workflow (24), AI (25),
  Integration (26), Mobile (27), Audit/Security (28), Document Management (21).
  A doctype is the wrong shape for these; they are platform services.
- **Analytics requirements.** Every module's `* Analytics` requirement is a
  report, not a stored entity.
