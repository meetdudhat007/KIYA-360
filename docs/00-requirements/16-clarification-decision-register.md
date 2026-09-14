# KIYA 360 - Clarification Decision & Approval Framework

## 1. Purpose

This Phase 0B-1C framework controls the conversion of an unresolved business question into a traceable, reviewable, explicitly approved decision and, only then, a future requirement update. It prevents discussion, stakeholder input, agent recommendations, and proposed decisions from being treated as approved KIYA 360 behavior.

This is governance documentation. It does not answer an open question, expand a requirement, or authorize implementation.

## 2. Scope and Source of Truth

The existing hierarchy in `AGENTS.md` remains controlling: current approved BRD; approved requirements documentation; approved project decisions; current project state; phase-specific planning and handoff; implementation when authorized; and agent suggestions. Within clarification work, the following distinction applies:

1. **Authoritative BRD** - the approved baseline.
2. **Approved requirements and approved project decisions** - authoritative only within their documented applicability.
3. **Phase plans and decision records** - governance/context; authoritative only where a record is explicitly approved.
4. **Proposed decisions** - non-authoritative candidates for approval.
5. **Stakeholder input, informal discussion, and agent recommendations** - evidence or context only; never a decision by themselves.

An approved clarification decision may resolve only the stated gap and authorize a traceable requirements update. It does not supersede the BRD generally or automatically approve every affected requirement.

## 3. Controlled Lifecycle

`Open Question -> Clarification Planned -> Clarification In Progress -> Answer Captured -> Proposed -> Under Review -> Approved -> Requirement/Traceability Update`

Alternative terminal or holding paths are `Proposed/Under Review -> Rejected`, `Open/Answer Captured/Proposed/Under Review -> Deferred`, and `Approved -> Change Requested -> New Proposed Decision -> Approved -> original Superseded`.

The clarification-session record in `15-critical-clarification-plan.md` captures the session. A decision record is created only when an answer has sufficient evidence to be assessed as a candidate decision. A single question can produce more than one decision record if its parts must be independently approved; the related OQ IDs must then be recorded on each record.

## 4. Decision Status Definitions

| Status | Meaning and entry authority | Authoritative / downstream use | Required evidence | Next status |
| --- | --- | --- | --- | --- |
| OPEN | A consequential unknown exists; requirements analyst records it from the baseline. | No; no behavior or requirement change may rely on it. | Question, source gap, impact. | Clarification Planned, Deferred. |
| CLARIFICATION PLANNED | A session/group and requested evidence are identified. | No; planning only. | Related OQ and plan/session reference. | Clarification In Progress, Deferred. |
| CLARIFICATION IN PROGRESS | Evidence gathering or a scheduled/active session is underway. | No. | Session reference and retained discussion/evidence. | Answer Captured, Deferred. |
| ANSWER CAPTURED | One or more stakeholder statements have been recorded without interpretation as an approved outcome. | No; it may support analysis only. | Dated source, participant/authority type where known, and conflicts. | Proposed, Clarification In Progress, Deferred. |
| PROPOSED | A bounded candidate decision and impact analysis are documented. Requirements analysts may prepare it; AI assistance is recommendation only. | No; no baseline, behavior, or requirement approval may rely on it. | Captured input, BRD context, scope/impact, unresolved portions, proposed approver type. | Under Review, Rejected, Deferred. |
| UNDER REVIEW | An identified appropriate authority is assessing a proposed decision. | No. | Proposed record and review evidence. | Approved, Rejected, Deferred, Proposed. |
| APPROVED | An identified authority explicitly accepts the exact decision statement, with date and evidence recorded. | Yes, only for the stated scope; it may authorize a requirement update, not automatically approve it. | Complete approval gate and approval record. | Superseded. |
| REJECTED | The proposed decision was explicitly not accepted. | No; it is historical and not active. | Rejection evidence and rationale where supplied. | Clarification In Progress, Deferred, or new Proposed. |
| DEFERRED | Deliberate postponement; the underlying question remains unresolved. | No; affected unknowns remain TBD. | Deferral rationale, authority if available, revisit trigger/date if known. | Clarification Planned, Clarification In Progress, Proposed. |
| SUPERSEDED | A formerly approved decision was replaced by a later approved decision. | No as current authority; retained as history. | Link to later approved decision and change record. | None. |

## 5. Decision Identification and Required Record

Use `CD-###` (for example, `CD-001`) for a clarification decision record. It is distinct from `OQ-###`, `FR-*`, `SF-###`, `DEP-###`, and business-flow IDs. Assign sequentially when a decision record is created; do not reuse an ID, delete a record, or renumber history.

Each record uses `17-clarification-decision-template.md` and contains: Decision ID; related OQ ID(s); title; status; priority; date created; clarification session; source/evidence; problem/ambiguity; BRD evidence; known facts; unknowns; stakeholder input; conflicting positions; proposed decision; impact analysis; affected requirements/modules/foundations/flows/dependencies/entities; risks; approval requirement and approver type; approval decision/date/evidence; requirement and traceability update states; supersession links; and notes.

`REQUIREMENT ID NOT YET ASSIGNED` is permitted where a future detailed requirement does not yet exist. It must not be replaced with an invented ID.

## 6. Proposed versus Approved, Evidence, and Approval

**Proposed** means a candidate formulation. **Approved** means the exact recorded formulation has explicit, evidenced acceptance by an identified appropriate authority. A stakeholder statement, meeting attendance, or AI-generated draft is not approval.

Before approval, the record must identify a generic approving authority type appropriate to the decision (for example, a Business Owner, Functional Owner, Requirements Approver, or Compliance Owner) unless approved ownership is already documented. Actual people and organizational routes remain TBD when not supplied. If no authority is known, the item cannot be approved and remains under review or deferred.

Approval evidence must identify the decision ID, precise outcome, approver/authority type, date, and durable source reference. Conflicting stakeholder positions are preserved with attribution; they cannot be silently reconciled. The authority resolves the conflict with recorded rationale, requests clarification, or rejects/defers the proposal. A partial answer creates a scoped proposed decision only for the answered part; every remaining part stays linked to the OQ as TBD/open.

## 7. Approval Gate: Proposed to Approved

- The decision statement is bounded and unambiguous.
- Related OQ ID(s), BRD evidence, captured input, and source/evidence are recorded.
- Affected requirements (or `REQUIREMENT ID NOT YET ASSIGNED`), modules, and applicable foundations, flows, and dependencies are identified.
- Known facts, unknowns, risks, and partial scope are visible.
- Conflicts are resolved by the approver or explicitly recorded; unresolved portions remain TBD.
- The approver type is identified and the approval is explicit, dated, and durably evidenced.
- Requirement/traceability implications and downstream restrictions are understood.

Failure of any gate item prevents approval; the record remains Proposed, Under Review, or Deferred.

## 8. Requirement Update and Open-Question Closure

An approved decision is valid evidence for future detailed-requirement expansion under `10-detailed-requirements-strategy.md`; it is not a requirement update itself. Before changing a requirement because of a decision, verify:

- the source CD record is Approved and applicable;
- the requirement ID exists, or its absence is explicitly recorded;
- the change impact and affected cross-module dependencies are checked;
- repository baseline/history is preserved under existing conventions;
- the updated requirement retains BRD and CD traceability and correct classification;
- unresolved portions remain TBD; and
- validation is recorded.

Close an OQ only when all material parts have approved decision coverage, associated requirement/traceability updates are recorded, and no linked material TBD remains. Otherwise keep the OQ open, partially answered, or deferred. Deferred is not closure.

## 9. Change Control, Auditability, and AI Governance

An approved decision is never silently edited. A change creates a new proposed CD record with impact analysis; after its approval, it records the predecessor as Superseded and links both records. Rejected, deferred, and superseded records remain in history.

The register and linked records must allow a reviewer to determine the triggering question, evidence, authority, approval date, affected requirements/modules/foundations/flows, and predecessor decision. AI agents may capture evidence, identify traceability, draft a clearly labelled proposal, and validate completeness. They cannot self-approve a business decision, infer approval from discussion, or implement behavior from non-approved material. Agents must read the current register, decisions, state, handoff, and relevant source before acting, then update the register, traceability, state/handoff, and changelog when authorized work changes them.

## 10. Decision-State Matrix

| State | Authoritative? | Can affect approved requirements? | Can AI implement behavior from it? | Requires evidence? | Can be changed? | Next possible states |
| --- | --- | --- | --- | --- | --- | --- |
| OPEN | No | No | No | Yes | Yes | Clarification Planned, Deferred |
| PROPOSED | No | No | No | Yes | Yes | Under Review, Rejected, Deferred |
| UNDER REVIEW | No | No | No | Yes | Yes | Approved, Rejected, Deferred, Proposed |
| APPROVED | Yes, scoped | May authorize an update only | Only after authorized downstream work and requirement update | Yes | Only through change control | Superseded |
| REJECTED | No | No | No | Yes | Historical; new proposal may be created | Clarification In Progress, Deferred, new Proposed |
| DEFERRED | No | No | No | Yes | Yes | Clarification Planned, Clarification In Progress, Proposed |
| SUPERSEDED | No, historical only | No | No | Yes | No silent edits | None |

Decision status is not requirement status. An approved CD may enable requirements work; it does not change the Phase 0B requirement lifecycle or approve a detailed requirement by itself.

## 11. Current Register

The following clarification decisions have been formally created and approved in accordance with this governance framework. Remaining questions OQ-003 through OQ-015 remain open.

| Related OQ | Decision ID | Status | Decision statement / approval evidence | Source |
|---|---|---|---|---|
| `OQ-001` | `CD-001` | **APPROVED** | Adopt a HYBRID scope-expansion approach: fully detail core business flows (C2C, P2P, A2S) for Phase 0B-2; use proven ERP-standard behavior as traceable reference baseline for standard non-specified features; zero automatic ERPNext coupling; explicit KIYA differentiators and documented exceptions. Approved 14 Sept 2026. | `docs/00-requirements/29-cd001-scope-expansion-hybrid-model.md`; Stakeholder Direction CS-CG01-01 |
| `OQ-002` | `CD-002` | **APPROVED** | Use BUSINESS STATUS as the primary transactional lifecycle/status model representing operational progress. Explicitly reject ERPNext's technical dual docstatus (Draft/Submitted/Cancelled) model. Do not invent detailed status values yet; define progressively during Phase 0B-2. Approved 14 Sept 2026. | `docs/00-requirements/30-cd002-transactional-lifecycle-business-status.md`; Stakeholder Direction CS-CG01-01 |
| `OQ-003` to `OQ-015` | `NOT YET CREATED` | OPEN - clarification planned | Awaiting scheduled stakeholder clarification sessions (CG-02 through CG-07) | `06-open-questions.md`; `15-critical-clarification-plan.md` |

## 12. Hypothetical Lifecycle Example

This non-business example does not describe KIYA 360 behavior: `OQ-XXX -> clarification session -> stakeholder answer captured -> CD-XXX proposed -> impact analysis -> explicit approval -> CD-XXX approved -> affected requirement updated later -> traceability updated`. Until approval is recorded, the item remains non-authoritative.

## 13. Exit Criteria and Governance Rules

This phase is complete when the lifecycle, status meanings, evidence/approval gates, conflict/partial/deferred/supersession handling, requirement-update gate, traceability, AI governance, decision register, and reusable template exist. The 15 questions remain unresolved until their own records meet the closure rule.

1. No informal discussion becomes an approved decision automatically.
2. No proposed decision becomes authoritative until explicitly approved.
3. Every approved decision has traceable evidence and affected requirements.
4. Conflicts are preserved and formally resolved; deferred questions remain unresolved.
5. Superseded decisions remain historical records.
6. AI agents cannot self-approve business decisions.
7. Requirement changes caused by a decision remain traceable.
8. The BRD remains authoritative unless formally superseded through project governance.
