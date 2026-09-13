# KIYA 360 - Clarification Decision Template

Use one record for each candidate clarification decision. A blank or `TBD` field is not permission to infer an answer. Stakeholder input, proposed decision, and approved decision are deliberately separate.

| Field | Record |
| --- | --- |
| Decision ID | `CD-[###]` |
| Related Open Question ID(s) | `[OQ-...]` |
| Title | `[TBD]` |
| Status | `[OPEN / CLARIFICATION PLANNED / CLARIFICATION IN PROGRESS / ANSWER CAPTURED / PROPOSED / UNDER REVIEW / APPROVED / REJECTED / DEFERRED / SUPERSEDED]` |
| Priority / blocking | `[Existing OQ classification]` |
| Date created | `[TBD]` |
| Clarification session | `[Session ID / NOT YET AVAILABLE]` |
| Source / evidence | `[Dated durable reference]` |
| Problem / ambiguity | `[Restate unknown; do not answer it]` |
| BRD evidence | `[BRD section / requirement ID]` |
| Known facts | `[Source-supported facts only]` |
| Unknowns | `[TBDs remaining]` |
| Stakeholder input | `[Attributed captured statements; not an approved decision]` |
| Conflicting positions | `[TBD / recorded positions and source]` |
| Proposed decision | `[Candidate only; NOT APPROVED unless status is APPROVED with evidence below]` |
| Impact analysis | `[Scope and effect; no implementation design]` |
| Affected requirements | `[FR IDs / BRD section / REQUIREMENT ID NOT YET ASSIGNED]` |
| Affected modules | `[Existing module names]` |
| Affected foundations / flows / dependencies | `[SF / named flow / DEP IDs, where applicable]` |
| Affected conceptual entities | `[BRD terminology only, if applicable]` |
| Risks / unresolved portions | `[TBDs and constraints]` |
| Approval required | `[Yes / No - normally Yes for business decision]` |
| Approver type | `[TBD or approved generic authority type]` |
| Approval decision | `[NOT YET AVAILABLE / Approved / Rejected]` |
| Approval date | `[TBD]` |
| Approval evidence | `[Durable evidence reference]` |
| Requirement update required? | `[TBD]` |
| Requirement update status | `[Not started / TBD]` |
| Traceability update status | `[Not started / TBD]` |
| Supersedes / superseded by | `[None / CD-###]` |
| Notes | `[TBD]` |

Before moving from Proposed to Approved, apply the approval gate in `16-clarification-decision-register.md`. Do not remove rejected, deferred, or superseded records.
