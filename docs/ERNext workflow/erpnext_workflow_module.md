# 🔄 ERPNext — Workflow Module Guide
> A deep dive into the ERPNext Workflow engine, covering how documents move between different approval states.

---

## 🧭 MODULE OVERVIEW

The **Workflow** module in ERPNext allows you to define complex approval processes for any document (like Purchase Orders, Leave Applications, Sales Invoices). It controls who can approve a document at what stage, and what the next stage should be.

The system uses a state-machine logic driven by:
1. **Workflow State:** The current status of the document (e.g., Pending, Approved, Rejected).
2. **Workflow Action:** The button the user clicks to move to the next state (e.g., Approve, Reject, Review).
3. **Workflow Transition:** The rule connecting the Current State to the Next State via an Action.

---

# 🛠️ WORKFLOW MASTERS

## 1. 🔄 Workflow
This is the main setup document where you define the entire approval process for a specific DocType.

### Fields
| Field | Layman | Technical |
|---|---|---|
| **Workflow Name** ⭐ | Name of the process | e.g., "Purchase Order Approval" |
| **Document Type** ⭐ | Which document this applies to | e.g., "Purchase Order", "Leave Application" |
| **Is Active** ✅ | Turn the workflow on/off | Only one active workflow allowed per DocType |
| **Override Status** ✅ | Change the document's built-in status | Updates standard `status` field to match the workflow state |
| **Send Email Alert** ✅ | Notify users when action is needed | Auto-emails the next approvers |
| **Workflow State Field** ⭐ | Custom field to track the state | Usually `workflow_state` |
| **Document States (Table)** ⭐ | List of all possible states | See `Workflow Document State` below |
| **Transitions (Table)** ⭐ | The rules connecting the states | See `Workflow Transition` below |
| **Condition** | Optional code condition | e.g., `doc.grand_total > 50000` — workflow only applies if true |

---

## 2. 📍 Workflow State (Master)
**Layman:** The "labels" you can apply to a document in a workflow (e.g., Draft, Pending Approval, Approved).

### Fields
| Field | Layman | Technical |
|---|---|---|
| **Workflow State Name** ⭐ | e.g., "Pending HR Approval" | Name of the state |
| **Icon** | Visual icon | Shown in the document header |
| **Style** | Color coding | Success (Green), Warning (Orange), Danger (Red), Primary (Blue) |
| **Is Optional State** ✅ | Can be skipped | Used in sequential role assignments |

---

## 3. 📄 Workflow Document State (Child Table)
**Layman:** Inside the main Workflow, this defines what happens when the document is in a specific state.

### Fields
| Field | Layman | Technical |
|---|---|---|
| **State** ⭐ | The current state | Link to Workflow State master |
| **Doc Status** ⭐ | Draft / Submitted / Cancelled | 0 = Saved, 1 = Submitted, 2 = Cancelled |
| **Allow Edit For** ⭐ | Who can edit the document now | Select a Role (e.g., "HR Manager") |
| **Update Field** | Auto-update a specific field | e.g., `approved_by` |
| **Update Value** | The value to set | e.g., `session.user` |
| **Avoid Status Override** ✅ | Prevent standard status change | Disables status override just for this state |

---

## 4. 🔀 Workflow Transition (Child Table)
**Layman:** The "path" from one state to another. "If the document is Pending, and the Manager clicks Approve, it becomes Approved."

### Fields
| Field | Layman | Technical |
|---|---|---|
| **State** ⭐ | The starting state | e.g., "Pending Approval" |
| **Action** ⭐ | The button the user sees | e.g., "Approve" (Links to Workflow Action Master) |
| **Next State** ⭐ | The resulting state | e.g., "Approved" |
| **Allowed** ⭐ | Who is allowed to click this button | Select a Role (e.g., "Purchase Manager") |
| **Allow Self Approval** ✅ | Can the creator approve their own doc? | Uncheck to force 4-eyes principle |
| **Condition** | Python code condition | e.g., `doc.department == 'Sales'` |

---

## 5. ⚡ Workflow Action Master
**Layman:** A simple master list of all the buttons you can use in a workflow (e.g., Approve, Reject, Send Back, Review).

### Fields
| Field | Layman | Technical |
|---|---|---|
| **Action Name** ⭐ | Button label | e.g., "Approve" |

---

## 6. 📝 Workflow Action (Log)
**Layman:** A system log that records every time a workflow action is taken. Used internally for sending emails and tracking pending actions.

### Fields (Internal Use)
| Field | What it tracks |
|---|---|
| **Reference Doctype / Name** | Which document was acted upon |
| **Workflow State** | The state it was in |
| **Status** | Open / Completed |
| **User** | Who took the action |
| **Completed By System** | Background job completion flag |
| **Error Message / Action List / Email Msg** | Diagnostic tracking data |

---

## 🗺️ HOW IT ALL FITS TOGETHER (Example Workflow)

**Scenario:** Purchase Order Approval > $10,000

1. **States (Workflow Document State):**
   - **Draft:** `DocStatus=0`, Edit allowed for `Purchase User`
   - **Pending Manager:** `DocStatus=0`, Edit allowed for `Purchase Manager`
   - **Approved:** `DocStatus=1` (Submitted), Edit allowed for `Administrator`
   - **Rejected:** `DocStatus=2` (Cancelled), Edit allowed for `Administrator`

2. **Transitions (Workflow Transition):**
   - **Draft** → [Action: `Submit for Approval`] → **Pending Manager** (Allowed: `Purchase User`)
   - **Pending Manager** → [Action: `Approve`] → **Approved** (Allowed: `Purchase Manager`)
   - **Pending Manager** → [Action: `Reject`] → **Rejected** (Allowed: `Purchase Manager`)

**Layman Summary:** 
A normal user drafts the PO and clicks "Submit for Approval". The PO locks (they can't edit it anymore). The Manager logs in, sees it is "Pending Manager", and can edit it. The Manager clicks "Approve". The system automatically Submits the document (making it official) and changes the state to "Approved".
