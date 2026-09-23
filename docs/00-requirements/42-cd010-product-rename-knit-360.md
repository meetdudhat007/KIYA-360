# CD-010 — Product Rename to KNIT 360

## Document control

- **Document ID:** `42-cd010-product-rename-knit-360`
- **Decision ID:** `CD-010`
- **Status:** `APPROVED` — recorded on owner instruction, 23 September 2026
- **Supersedes:** `CD-005` (product named KNIT), recorded in document 40
- **Authority:** Repository owner, by direct instruction

## Decision

The product is named **KNIT 360**. The rename extends to code identifiers, not
only display strings — chosen explicitly by the owner after the cost of each
option was set out.

## Scope of the rename

| Area | Action |
| --- | --- |
| Display name | `KNIT` → `KNIT 360` in `app_title`, `app_publisher`, branding, page titles and prose. |
| Python packages | `knit_core` → `knit360_core`, `knit_demo` → `knit360_demo`. |
| Doctypes (61) | `KNIT Lead` → `KNIT 360 Lead`, and so on for all 61. |
| Doctype folders | `knit_lead` → `knit_360_lead`. Frappe derives the module path with `scrub()`, so the folder follows the doctype name, not the package name. |
| Controller classes | `KNITLead` → `KNIT360Lead`. Frappe derives the class name from the doctype with spaces removed. |
| Fields | `knit_business_status` → `knit360_business_status`; likewise `knit_approval_authority`, `knit_hsn_sac_code`. |
| Asset path | `/assets/knit_core/images/knit-logo.svg` → `/assets/knit360_core/images/knit360-logo.svg`. |
| Web route | `/knit` → `/knit360`. |
| `source/KIYA360_BRD.pdf` | **Not altered.** `AGENTS.md` forbids it; it remains the approved baseline under its original name. |
| `docs/` | **Not renamed**, for the same reason as `CD-005`: these are the historical record of decisions taken under earlier names, and rewriting them would destroy traceability. Documents 39–41 continue to say "KNIT"; read them as referring to this product under its former name. |
| Docker container names, bind-mount path (`/mnt/knit`) | **Not renamed.** Local development infrastructure, not the product. Renaming them would force container and symlink rework for no functional gain. |

Three naming conventions meet in this rename and do **not** produce the same
string — the package is `knit360_core`, the doctype folder is `knit_360_lead`,
and the field is `knit360_business_status`. Each follows its own framework
convention. The rename rules were generated from the doctype JSON on disk rather
than guessed, and applied longest-match-first, because a naive pass would have
let the field name `knit_business_status` eat the folder
`knit_business_status_log`.

## Consequence for the running site

Renaming doctypes renames their database tables. The existing site
`knit.localhost` therefore could not be migrated in place; a new site
`knit360.localhost` was created alongside it and left as the bench default. The
old site is untouched and still on disk. The data lost was test fixtures created
during seam verification — no real records existed.

## Defect found and fixed during the rename

`knit360_core.branding.apply` called `doc.save()` on **System Settings**. On a
site that has not been through the setup wizard, System Settings has no
`language` or `time_zone`, so the whole-document save failed its own mandatory
validation and took `after_install` down with it. This had never surfaced
because the app had only ever been installed onto an already-configured site.

Rewritten to use `frappe.db.set_single_value`, which writes only the fields that
belong to this module and does not validate the surrounding document. Proven by
the fresh install of `knit360.localhost`.

## Verification

| Check | Result |
| --- | --- |
| Rename pass | 154 files rewritten, 66 directories and 123 files renamed, **0 leftovers** under a scan for `\bKNIT\b(?! 360)`, `knit_`, `KNIT[A-Z]`. |
| Site-free test suite | 37 tests pass unchanged. |
| Fresh install | `knit360.localhost` created from empty; `install-app` and `migrate` both clean. |
| Schema | 61 `KNIT 360` doctypes, 61 `tabKNIT 360 …` tables, 0 stale `KNIT ` doctypes. |
| Branding | Login page reads `KNIT 360 - Login`, "Login to KNIT 360", `knit360-logo.svg`. |
| Seam | `/knit360` renders; `knit360_core.api.c2c` drives the full flow. |
| Flow | `LEAD-2026-0001` New → Contacted → Qualified → converted to customer *Shakti Forgings Pvt Ltd* + `OPP-2026-0002` → `QTN-2026-0003` → Pending Approval → Issued / Sent. |
| Docstatus boundary | Crossed once, `0 → 1` at `Issued / Sent`. |
| Illegal transition | Refused, naming the allowed set. |

## Decisions carried forward unchanged

`CD-001` through `CD-004`, `CD-006` through `CD-009`, and `DEC-001` through
`DEC-020` all remain in force. `OQ-021` (front-end technology) remains **OPEN**.
Only the product's name has changed.
