# CD-005 — Product Rename to KNIT

## Document control

- **Document ID:** 40-cd005-product-rename-knit
- **Decision ID:** `CD-005` (`DEC-020`)
- **Status:** `APPROVED` — recorded on owner instruction, 23 September 2026
- **Resolves:** `OQ-016` (KELVIN / KIYA naming), raised in document 39
- **Authority:** Repository owner, by direct instruction

## Decision

The product is named **KNIT**. Neither "KIYA 360" nor "KELVIN 360" is the product name going forward.

## Scope of the rename

| Area | Action | Rationale |
| --- | --- | --- |
| Application code under `backend/` | Renamed. `kiya_core` → `knit_core`, `kiya_demo` → `knit_demo`, doctype prefix `KIYA ` → `KNIT `, field `kiya_business_status` → `knit_business_status`, and all imports, classes and UI strings. | Code is KNIT-owned and carries no external authority. |
| `source/KIYA360_BRD.pdf` | **Not altered.** | `AGENTS.md` forbids altering the BRD. It remains the approved requirements baseline under its original name. |
| `docs/` requirement and architecture documents | **Not renamed.** | They are the historical record of decisions taken under the previous name. Rewriting them would destroy traceability. Document filenames such as `24-erpnext-kiya-gap-analysis.md` therefore keep their original names, and code may cite them as written. |
| Repository directory `KIYA-360` | Not renamed in this decision. | Cosmetic; can follow separately without affecting the build. |

## Consequence

References to "KIYA 360" in documents dated before 23 September 2026 should be read as referring to this product under its former name. The BRD's 28-module baseline, the 238 requirement records, and decisions `CD-001` through `CD-004` all remain in force unchanged — only the product's name has changed.

## Verification

The rename rewrote 141 files, 63 directories and 122 filenames under `backend/`. The full `knit_core` test suite (29 tests) passes afterwards, including the bare-Frappe link-safety check and the lifecycle-drift check, and both applications compile. No `KIYA` identifier remains in code; the only surviving occurrence is a citation of a `docs/` filename, which is correct.

## Related decisions recorded the same day

| Ref | Decision | Detail |
| --- | --- | --- |
| `CD-006` | Sales Order approval uses the **KNIT business status adapter**, not Frappe's Workflow doctype. | Resolves the conflict recorded in `knit_core/business_status/engine.py`. The Workflow engine drives `docstatus`, which `CD-002` rejects. `knit_demo.demo_seed.platform.install_workflow` must not be run on a site where the adapter governs Sales Order. |
| `CD-007` | The `Default` lifecycle retains **nine** states. | Resolves the 8-vs-9 discrepancy between `04-target-architecture.md` §6.1 and documents 03 / `RSK-02`. The architecture diagram is authoritative; the "8-state" wording in the other documents is an error and should be read as nine. |
| `CD-008` | Database engine: **MariaDB**. | Frappe's primary supported engine and its default. PostgreSQL support exists but is less exercised across Frappe apps. Recorded here because `AGENTS.md` bars agents from unilateral technology decisions; this one was taken on explicit owner instruction. |
