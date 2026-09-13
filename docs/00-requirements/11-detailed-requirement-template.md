# KIYA 360 — Detailed Requirement Template

Use one copy of this template for each future Phase 0B detailed requirement. Replace bracketed placeholders only with supported or approved information. A field may be **TBD — The BRD does not specify this detail**. When a clarification decision informs this record, cite its approved `CD-###` identifier and approval evidence in the source/traceability fields. A proposed, under-review, deferred, rejected, or superseded decision is not valid evidence for a requirement update.

## Requirement Identity

| Field | Value |
| --- | --- |
| Detailed requirement ID | `[TBD]` |
| Phase 0A requirement ID | `[FR-…]` |
| Module | `[BRD module name]` |
| Sub-module | `[BRD capability, if stated]` |
| Requirement title | `[BRD-supported title]` |
| Classification | `[BRD-REQUIRED / BRD-DERIVED / PROPOSED / TBD / OUT-OF-SCOPE]` |
| BRD source | `[BRD section/page/requirement]` |
| Related business objective | `[BRD-supported objective or TBD]` |
| Status | `[See 12-requirement-status-legend.md]` |

## Requirement Statement

`[State only the supported business requirement. Do not add a technical solution.]`

## Context and Behavior

| Field | Value |
| --- | --- |
| Actor(s) | `[BRD-supported actor(s) or TBD]` |
| Trigger | `[BRD-supported trigger or TBD]` |
| Preconditions | `[BRD-supported preconditions or TBD]` |
| Inputs | `[BRD-supported inputs or TBD]` |
| Main behavior | `[Explicit behavior; derived behavior must be labelled]` |
| Outputs | `[BRD-supported outputs or TBD]` |
| Business rules | `[Explicit rules / BRD-DERIVED rationale / TBD]` |
| Validations | `[BRD-supported validations or TBD]` |
| Status / lifecycle | `[BRD-supported lifecycle or TBD]` |
| Approval requirements | `[BRD-supported approval requirement or TBD]` |
| Notifications | `[BRD-supported notification requirement or TBD]` |
| Exception handling | `[BRD-supported exception behavior or TBD]` |

## Cross-Module and Data Context

| Field | Value |
| --- | --- |
| Business flow | `[Customer-to-Cash / Procure-to-Pay / Asset-to-Service / TBD]` |
| Upstream dependencies | `[Requirement IDs or TBD]` |
| Downstream dependencies | `[Requirement IDs or TBD]` |
| Shared master data concepts | `[BRD conceptual terms or TBD]` |
| Transaction data concepts | `[BRD conceptual terms or TBD]` |
| Workflow / audit / security considerations | `[BRD-supported detail or TBD]` |
| Mobile considerations | `[BRD-supported detail or TBD]` |
| AI considerations | `[BRD-supported detail or TBD]` |

## Acceptance and Governance

| Field | Value |
| --- | --- |
| Acceptance criteria | `[Observable, source-supported criteria or TBD]` |
| Open questions / TBDs | `[OQ IDs and/or TBD description]` |
| Related requirements | `[BRD / Phase 0A / detailed IDs]` |
| Traceability references | `[BRD → Phase 0A → detailed requirement]` |
| Change-control reference | `[If applicable; otherwise N/A]` |

## Evidence and Review

| Field | Value |
| --- | --- |
| Evidence / rationale | `[Exact BRD or approved-decision evidence]` |
| Reviewer | `[TBD]` |
| Review decision | `[TBD]` |
| Decision source and date | `[TBD]` |

### Template Use Rules

- Do not convert placeholders into assumed facts.
- Mark a logically necessary inference as BRD-DERIVED and cite its parent requirement.
- Label a recommendation PROPOSED and state that it is not a confirmed BRD requirement.
- Use OUT-OF-SCOPE only for explicit BRD exclusions.
- Do not add API, UI, data-model, technology, or implementation design.
