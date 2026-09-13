# KIYA 360 — Decision Register

Only recorded, source-supported decisions belong here. “Do Not Reverse Without Review” means a change requires explicit authorization and a traceable change record.

| Decision ID | Date | Decision | Status | Reason | Affected Area | Source | Do Not Reverse Without Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 13 September 2026 | BRD version 2.0 is the current source of truth. | Approved baseline | BRD document control identifies v2.0 and says it supersedes the earlier 12-module BRD. | All requirements | BRD; `09-phase-0a-review.md` | Yes |
| DEC-002 | 13 September 2026 | Phase 0 remains documentation/requirements focused and technology-neutral. | Approved baseline | Phase instructions and project state prohibit implementation/design decisions. | Phase 0 work | `01-master-requirements.md`; `10-detailed-requirements-strategy.md` | Yes |
| DEC-003 | 13 September 2026 | Phase 0A is complete with review status PASS WITH CORRECTIONS. | Completed | Formal review validated the baseline and corrected one unsupported flow mapping. | Phase 0A baseline | `09-phase-0a-review.md` | Yes |
| DEC-004 | 13 September 2026 | Phase 0B-0 is complete; its strategy, template, and status legend govern later detailed requirements work. | Completed | Governance artifacts were created and validated. | Requirements governance | `10`–`12` requirements documents | Yes |
| DEC-005 | 13 September 2026 | Technology decisions are deferred until an appropriate authorized architecture phase. | Approved baseline | BRD/Phase 0 documents are technology-neutral. | Architecture and implementation | `01-master-requirements.md`; `10-detailed-requirements-strategy.md` | Yes |
| DEC-006 | 13 September 2026 | KIYA 360 scope is the BRD's 28-module enterprise platform scope. | Approved baseline | BRD §3.1 and Phase 0A inventory. | Scope | BRD; `02-module-inventory.md` | Yes |
| DEC-007 | 13 September 2026 | A unified data model with no duplicate master data across CRM, ERP, and back-office systems is required. | BRD-REQUIRED | BRD NFR explicitly requires it. | Cross-module data concepts | BRD §10; `01-master-requirements.md` | Yes |
| DEC-008 | 13 September 2026 | Requirements use BRD-REQUIRED, BRD-DERIVED, PROPOSED, TBD, and OUT-OF-SCOPE classifications. | Approved governance | Prevents unsupported behavior from becoming baseline. | Requirements governance | `01-master-requirements.md`; `10-detailed-requirements-strategy.md` | Yes |
| DEC-009 | 13 September 2026 | Unspecified functionality is not automatically OUT-OF-SCOPE; it is TBD unless explicitly excluded. | Approved governance | BRD fidelity/anti-hallucination rule. | Scope management | `03-scope-boundaries.md`; `10-detailed-requirements-strategy.md` | Yes |
| DEC-010 | 13 September 2026 | No direct Customer Service-to-end-to-end-flow mapping is asserted. | Approved correction | BRD does not explicitly map Customer Service to a named flow. | Customer Service / flow traceability | `09-phase-0a-review.md`; `02-module-inventory.md` | Yes |
| DEC-011 | 13 September 2026 | Shared-foundation/dependency analysis consists of 15 SF records and 11 explicit critical/high dependency records. | Completed analysis | Mapping completed without detailed requirement expansion. | Phase 0B-1A | `13-shared-foundation-requirements-map.md`; `14-critical-requirement-dependencies.md` | Yes |
