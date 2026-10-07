"""Business status lifecycles (CD-002).

CD-002 states that exact status enumerations are defined per document type, not
globally. So this module holds a registry of lifecycles rather than one matrix.

DEFAULT is transcribed from the state diagram in
docs/02-architecture/04-target-architecture.md section 6.1, which is labelled
PROPOSED / ILLUSTRATIVE. LEAD and OPPORTUNITY are transcribed from the
candidate lifecycles in docs/00-requirements/31-customer-to-cash-detailed-requirements.md
(DR-C2C-001 and DR-C2C-002), both classified PROPOSED there.

None of these are ratified; document 03 still lists ratifying the transition
matrix as an open item. When it is ratified, change the lifecycles here and
nothing else.

Discrepancy, unresolved in the repository: the architecture diagram enumerates
nine states, while document 03 and RSK-02 describe an "8-state" model. DEFAULT
follows the diagram because it is the only explicit enumeration.

The diagram writes Pending_Approval and In_Progress with underscores because
mermaid requires it. Stored values use spaces.
"""

#: The field every governed doctype carries. Defined here, not in engine.py,
#: so it can be read without importing frappe.
FIELD = "knit360_business_status"

# --- DEFAULT lifecycle states (architecture doc section 6.1) ---
DRAFT = "Draft"
PENDING_APPROVAL = "Pending Approval"
APPROVED = "Approved"
REJECTED = "Rejected"
IN_PROGRESS = "In Progress"
PARTIALLY_COMPLETED = "Partially Completed"
COMPLETED = "Completed"
CLOSED = "Closed"
CANCELLED = "Cancelled"


class Lifecycle:
	"""A per-doctype state machine and its mapping onto Frappe's docstatus.

	draft_states     -> docstatus 0, nothing posted
	submitted_states -> docstatus 1, effects are live
	cancelling_states-> docstatus 2 if already submitted, else 0

	A doctype that is never submitted (a CRM Lead, say) declares every state as
	a draft state and leaves the other two empty.
	"""

	def __init__(self, name, initial, transitions, draft_states, submitted_states=(),
	             cancelling_states=(), happy_path=()):
		self.name = name
		self.initial = initial
		self.transitions = transitions
		self.draft_states = set(draft_states)
		self.submitted_states = set(submitted_states)
		self.cancelling_states = set(cancelling_states)
		#: The intended progression, in order, as the DR- record states it.
		#: Everything else is a branch -- lost, declined, cancelled. A user
		#: interface needs the difference to know which step to recommend;
		#: transitions alone is an unordered set and cannot say.
		self.happy_path = tuple(happy_path)

	@property
	def states(self):
		"""Declaration order, which is also display order."""
		return list(self.transitions)

	@property
	def terminal_states(self):
		return {s for s, nxt in self.transitions.items() if not nxt}

	def is_allowed(self, from_status, to_status):
		return to_status in self.transitions.get(from_status, set())

	def allowed_next(self, from_status):
		return sorted(self.transitions.get(from_status, set()))

	def forward_from(self, from_status):
		"""The next step along the happy path, if there is one and it is legal."""
		if from_status not in self.happy_path:
			return None
		index = self.happy_path.index(from_status)
		if index + 1 >= len(self.happy_path):
			return None
		nxt = self.happy_path[index + 1]
		return nxt if self.is_allowed(from_status, nxt) else None

	def locks_on(self, to_status, current_docstatus=0):
		"""True when reaching this status stops the document being editable."""
		return self.required_docstatus(to_status, current_docstatus) == 1

	def required_docstatus(self, to_status, current_docstatus):
		"""Map a target business status onto the docstatus Frappe must hold.

		Cancellation is deliberately contextual. Frappe cannot cancel a draft,
		so a document cancelled before it was ever submitted stays at docstatus
		0 and is cancelled in business terms only -- correctly, since it posted
		no ledger effect and so has nothing to reverse. Only a document that
		reached docstatus 1 goes to docstatus 2, where Frappe writes the
		reversing entries CD-002 requires of a cancellation.
		"""
		if to_status in self.draft_states:
			return 0
		if to_status in self.submitted_states:
			return 1
		if to_status in self.cancelling_states:
			return 2 if current_docstatus == 1 else 0
		raise ValueError(f"{self.name}: unknown business status: {to_status}")


DEFAULT = Lifecycle(
	name="Default",
	initial=DRAFT,
	transitions={
		DRAFT: {PENDING_APPROVAL, CANCELLED},
		PENDING_APPROVAL: {APPROVED, REJECTED, CANCELLED},
		APPROVED: {IN_PROGRESS, CANCELLED},
		REJECTED: {DRAFT},
		IN_PROGRESS: {PARTIALLY_COMPLETED, COMPLETED, CANCELLED},
		PARTIALLY_COMPLETED: {COMPLETED},
		COMPLETED: {CLOSED},
		CLOSED: set(),
		CANCELLED: set(),
	},
	draft_states={DRAFT, PENDING_APPROVAL, REJECTED},
	submitted_states={APPROVED, IN_PROGRESS, PARTIALLY_COMPLETED, COMPLETED, CLOSED},
	cancelling_states={CANCELLED},
)

# DR-C2C-001: "New -> Contacted -> Qualified -> Converted (or Disqualified / Lost)".
# The happy path is quoted. Which active states may branch to Disqualified or
# Lost is inferred, since the source gives the branch without placing it.
# A Lead posts no ledger or stock effect, so it is never submitted.
LEAD = Lifecycle(
	name="Lead",
	initial="New",
	transitions={
		"New": {"Contacted", "Disqualified", "Lost"},
		"Contacted": {"Qualified", "Disqualified", "Lost"},
		"Qualified": {"Converted", "Disqualified", "Lost"},
		"Converted": set(),
		"Disqualified": set(),
		"Lost": set(),
	},
	draft_states={"New", "Contacted", "Qualified", "Converted", "Disqualified", "Lost"},
	happy_path=("New", "Contacted", "Qualified", "Converted"),
)

# DR-C2C-002: "Open -> In Negotiation -> Proposal Sent -> Won (or Lost)".
OPPORTUNITY = Lifecycle(
	name="Opportunity",
	initial="Open",
	transitions={
		"Open": {"In Negotiation", "Lost"},
		"In Negotiation": {"Proposal Sent", "Lost"},
		"Proposal Sent": {"Won", "Lost"},
		"Won": set(),
		"Lost": set(),
	},
	draft_states={"Open", "In Negotiation", "Proposal Sent", "Won", "Lost"},
	happy_path=("Open", "In Negotiation", "Proposal Sent", "Won"),
)

# DR-C2C-003: "Received -> Under Review -> Feasibility Confirmed -> Quoted
# (or Declined / Regret)". An Enquiry posts no ledger or stock effect.
ENQUIRY = Lifecycle(
	name="Enquiry",
	initial="Received",
	transitions={
		"Received": {"Under Review", "Declined / Regret"},
		"Under Review": {"Feasibility Confirmed", "Declined / Regret"},
		"Feasibility Confirmed": {"Quoted", "Declined / Regret"},
		"Quoted": set(),
		"Declined / Regret": set(),
	},
	draft_states={"Received", "Under Review", "Feasibility Confirmed", "Quoted", "Declined / Regret"},
	happy_path=("Received", "Under Review", "Feasibility Confirmed", "Quoted"),
)

# DR-C2C-004: "Draft -> Pending Approval -> Issued / Sent -> Accepted -> Ordered
# (or Expired / Declined)".
# Expired and Declined stay submitted rather than cancelling: a quotation posts
# no ledger effect, so there is nothing to reverse, and the issued document
# must remain on record.
QUOTATION = Lifecycle(
	name="Quotation",
	initial="Draft",
	transitions={
		"Draft": {"Pending Approval"},
		"Pending Approval": {"Issued / Sent", "Draft"},
		"Issued / Sent": {"Accepted", "Expired", "Declined"},
		"Accepted": {"Ordered", "Expired"},
		"Ordered": set(),
		"Expired": set(),
		"Declined": set(),
	},
	draft_states={"Draft", "Pending Approval"},
	submitted_states={"Issued / Sent", "Accepted", "Ordered", "Expired", "Declined"},
	happy_path=("Draft", "Pending Approval", "Issued / Sent", "Accepted", "Ordered"),
)

# DR-C2C-005: "Draft -> Confirmed / Booked -> In Fulfillment -> Delivered ->
# Closed (or On Hold / Cancelled)". Branch placement is inferred; the source
# gives the branches without stating which states they leave from.
SALES_ORDER = Lifecycle(
	name="Sales Order",
	initial="Draft",
	transitions={
		"Draft": {"Confirmed / Booked", "Cancelled"},
		"Confirmed / Booked": {"In Fulfillment", "On Hold", "Cancelled"},
		"In Fulfillment": {"Delivered", "On Hold", "Cancelled"},
		"On Hold": {"In Fulfillment", "Cancelled"},
		"Delivered": {"Closed"},
		"Closed": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft"},
	submitted_states={"Confirmed / Booked", "In Fulfillment", "On Hold", "Delivered", "Closed"},
	cancelling_states={"Cancelled"},
)

# DR-C2C-012: "Draft -> Dispatched / In Transit -> Delivered (or Return
# Initiated / Cancelled)". A Delivery Note moves stock, so it submits.
DELIVERY_NOTE = Lifecycle(
	name="Delivery Note",
	initial="Draft",
	transitions={
		"Draft": {"Dispatched / In Transit", "Cancelled"},
		"Dispatched / In Transit": {"Delivered", "Return Initiated", "Cancelled"},
		"Delivered": {"Return Initiated"},
		"Return Initiated": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft"},
	submitted_states={"Dispatched / In Transit", "Delivered", "Return Initiated"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Dispatched / In Transit", "Delivered"),
)

# DR-P2P-001 (Supplier): A master; it posts nothing.
SUPPLIER = Lifecycle(
	name="Supplier",
	initial="Prospect / Draft",
	transitions={
		"Prospect / Draft": {"Under Compliance Review"},
		"Under Compliance Review": {"Approved / Active", "Deactivated / Blacklisted"},
		"Approved / Active": {"Deactivated / Blacklisted", "Suspended / On Hold"},
		"Suspended / On Hold": {"Approved / Active", "Deactivated / Blacklisted"},
		"Deactivated / Blacklisted": set(),
	},
	draft_states={"Prospect / Draft", "Under Compliance Review", "Approved / Active", "Suspended / On Hold", "Deactivated / Blacklisted"},
)

# DR-P2P-002 (Sourcing Project): A qualification project; it posts nothing.
SOURCING_PROJECT = Lifecycle(
	name="Sourcing Project",
	initial="Initiated",
	transitions={
		"Initiated": {"Rejected / Ineligible", "Supplier Discovery"},
		"Supplier Discovery": {"Evaluation / Auditing", "Rejected / Ineligible"},
		"Evaluation / Auditing": {"Qualified", "Rejected / Ineligible"},
		"Qualified": set(),
		"Rejected / Ineligible": set(),
	},
	draft_states={"Initiated", "Supplier Discovery", "Evaluation / Auditing", "Qualified", "Rejected / Ineligible"},
)

# DR-P2P-003 (Request for Quotation): Published solicitations are locked from edit.
RFQ = Lifecycle(
	name="Request for Quotation",
	initial="Draft",
	transitions={
		"Draft": {"Cancelled", "Published / Sent"},
		"Published / Sent": {"Bidding Open", "Cancelled"},
		"Bidding Open": {"Bidding Closed", "Cancelled"},
		"Bidding Closed": {"Cancelled", "Evaluated"},
		"Evaluated": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft"},
	submitted_states={"Bidding Closed", "Bidding Open", "Evaluated", "Published / Sent"},
	cancelling_states={"Cancelled"},
)

# DR-P2P-004 (Supplier Quotation): A received bid; it posts nothing. Rejected and Expired are terminal, not cancellations.
SUPPLIER_QUOTATION = Lifecycle(
	name="Supplier Quotation",
	initial="Draft / Received",
	transitions={
		"Draft / Received": {"Under Evaluation"},
		"Under Evaluation": {"Expired", "Rejected", "Shortlisted"},
		"Shortlisted": {"Awarded", "Expired", "Rejected"},
		"Awarded": set(),
		"Rejected": set(),
		"Expired": set(),
	},
	draft_states={"Draft / Received", "Under Evaluation", "Shortlisted", "Awarded", "Rejected", "Expired"},
)

# DR-P2P-005 (Purchase Order): An approved PO is a commitment.
PURCHASE_ORDER = Lifecycle(
	name="Purchase Order",
	initial="Draft",
	transitions={
		"Draft": {"Cancelled", "Pending Approval"},
		"Pending Approval": {"Approved / Ordered", "Cancelled", "Draft"},
		"Approved / Ordered": {"Cancelled", "Completed / Closed", "On Hold", "Partially Received"},
		"Partially Received": {"Cancelled", "Completed / Closed", "On Hold"},
		"On Hold": {"Approved / Ordered", "Cancelled"},
		"Completed / Closed": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft", "Pending Approval"},
	submitted_states={"Approved / Ordered", "Completed / Closed", "On Hold", "Partially Received"},
	cancelling_states={"Cancelled"},
)

# DR-P2P-006 (Goods Receipt): Receipt moves stock, so it posts.
GOODS_RECEIPT = Lifecycle(
	name="Goods Receipt",
	initial="Draft / Gate Logged",
	transitions={
		"Draft / Gate Logged": {"Cancelled", "Received in Bay", "Rejected at Gate"},
		"Received in Bay": {"Cancelled", "Pending Inspection"},
		"Pending Inspection": {"Accepted & Staged", "Cancelled", "Rejected at Gate"},
		"Accepted & Staged": set(),
		"Rejected at Gate": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft / Gate Logged"},
	submitted_states={"Accepted & Staged", "Pending Inspection", "Received in Bay", "Rejected at Gate"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft / Gate Logged", "Received in Bay", "Pending Inspection",
	            "Accepted & Staged"),
)

# DR-P2P-007 (Quality Inspection): An inspection record; it posts nothing itself.
QUALITY_INSPECTION = Lifecycle(
	name="Quality Inspection",
	initial="Pending Inspection",
	transitions={
		"Pending Inspection": {"Quarantined", "Under Testing"},
		"Under Testing": {"Accepted", "Accepted with Concession", "Quarantined", "Rejected"},
		"Quarantined": {"Rejected", "Under Testing"},
		"Accepted": set(),
		"Rejected": set(),
		"Accepted with Concession": set(),
	},
	draft_states={"Pending Inspection", "Under Testing", "Quarantined", "Accepted", "Rejected", "Accepted with Concession"},
)

# DR-P2P-008 (Putaway Task): A warehouse task; the stock move is posted by the receipt.
PUTAWAY_TASK = Lifecycle(
	name="Putaway Task",
	initial="Task Generated",
	transitions={
		"Task Generated": {"Assigned", "Cancelled"},
		"Assigned": {"Cancelled", "Moving"},
		"Moving": {"Cancelled", "Completed / Binned"},
		"Completed / Binned": set(),
		"Cancelled": set(),
	},
	draft_states={"Task Generated", "Assigned", "Moving", "Completed / Binned", "Cancelled"},
)

# DR-P2P-009 (Supplier Invoice): Approval creates the payable, so it posts.
SUPPLIER_INVOICE = Lifecycle(
	name="Supplier Invoice",
	initial="Draft",
	transitions={
		"Draft": {"Cancelled", "Matched & Approved", "On Hold / Variance Pending"},
		"On Hold / Variance Pending": {"Cancelled", "Matched & Approved"},
		"Matched & Approved": {"Cancelled", "Paid in Full", "Partially Paid"},
		"Partially Paid": {"Cancelled", "Paid in Full"},
		"Paid in Full": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft", "On Hold / Variance Pending"},
	submitted_states={"Matched & Approved", "Paid in Full", "Partially Paid"},
	cancelling_states={"Cancelled"},
)

# DR-P2P-011 (Payment Entry): Disbursement moves cash, so it posts.
PAYMENT_ENTRY = Lifecycle(
	name="Payment Entry",
	initial="Draft",
	transitions={
		"Draft": {"Cancelled", "Pending Bank Authorization"},
		"Pending Bank Authorization": {"Cancelled", "Disbursed / Cleared", "Rejected / Bounced"},
		# A cleared payment can still be reversed: a cheque bounces after it
		# cleared, a receipt is matched to the wrong customer. Cancelling
		# writes the mirror entry and the invoice it settled goes back to
		# owing -- DEC-022. Sales Invoice allows the same from its posted
		# states, and a payment that could never be undone would be the only
		# posting in the system with no way back.
		"Disbursed / Cleared": {"Cancelled"},
		"Rejected / Bounced": set(),
		"Cancelled": set(),
	},
	draft_states={"Draft", "Pending Bank Authorization"},
	submitted_states={"Disbursed / Cleared", "Rejected / Bounced"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Pending Bank Authorization", "Disbursed / Cleared"),
)

# DR-P2P-012 (Supplier Scorecard): An analytics period; it posts nothing.
SUPPLIER_SCORECARD = Lifecycle(
	name="Supplier Scorecard",
	initial="Period Open",
	transitions={
		"Period Open": {"Calculating"},
		"Calculating": {"Published / Rated"},
		"Published / Rated": {"Archived"},
		"Archived": set(),
	},
	draft_states={"Period Open", "Calculating", "Published / Rated", "Archived"},
)

# DR-A2S-001 (Asset): The installed-base registry. Capitalisation and depreciation are MOD-17's postings, not this record's.
ASSET = Lifecycle(
	name="Asset",
	initial="Registered",
	transitions={
		"Registered": {"Commissioned / Operational", "Scrapped"},
		"Commissioned / Operational": {"Decommissioned", "Degraded / Limited", "Under Maintenance"},
		"Under Maintenance": {"Commissioned / Operational", "Decommissioned", "Degraded / Limited"},
		"Degraded / Limited": {"Decommissioned", "Under Maintenance"},
		"Decommissioned": {"Scrapped"},
		"Scrapped": set(),
	},
	draft_states={"Registered", "Commissioned / Operational", "Under Maintenance", "Degraded / Limited", "Decommissioned", "Scrapped"},
)

# DR-A2S-003 (Service Contract): A coverage agreement; billing posts separately.
SERVICE_CONTRACT = Lifecycle(
	name="Service Contract",
	initial="Draft",
	transitions={
		"Draft": {"Active / In Coverage", "Voided / Terminated"},
		"Active / In Coverage": {"Expired", "Expiring Soon", "Voided / Terminated"},
		"Expiring Soon": {"Expired", "Voided / Terminated"},
		"Expired": set(),
		"Voided / Terminated": set(),
	},
	draft_states={"Draft", "Active / In Coverage", "Expiring Soon", "Expired", "Voided / Terminated"},
)

# DR-A2S-005 (Service Dispatch): A dispatch record; it posts nothing.
SERVICE_DISPATCH = Lifecycle(
	name="Service Dispatch",
	initial="Unassigned",
	transitions={
		"Unassigned": {"Assigned"},
		"Assigned": {"Dispatched / En Route", "Reassigned", "Rescheduled"},
		"Dispatched / En Route": {"On Site", "Reassigned", "Rescheduled"},
		"On Site": {"Rescheduled", "Work Started"},
		"Work Started": set(),
		"Reassigned": {"Assigned"},
		"Rescheduled": {"Assigned"},
	},
	draft_states={"Unassigned", "Assigned", "Dispatched / En Route", "On Site", "Work Started", "Reassigned", "Rescheduled"},
)

# FR-FIN-001. No DR- record specifies a journal entry lifecycle, so this is the
# minimum a manual posting needs: it is drafted, it may be reviewed, it posts,
# and a posted entry is reversed rather than edited. PROPOSED.
JOURNAL_ENTRY = Lifecycle(
	name="Journal Entry",
	initial="Draft",
	transitions={
		"Draft": {"Pending Approval", "Posted", "Cancelled"},
		"Pending Approval": {"Posted", "Draft", "Cancelled"},
		"Posted": {"Cancelled"},
		"Cancelled": set(),
	},
	draft_states={"Draft", "Pending Approval"},
	submitted_states={"Posted"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Pending Approval", "Posted"),
)

# FR-FIN-003. Accounts Receivable. Posted / Unpaid is where the receivable comes
# into existence, so that is the first submitted state. Partly Paid, Paid and
# Overdue stay submitted: settlement changes what is outstanding, not whether
# the invoice was issued. PROPOSED -- the BRD gives no enumeration.
SALES_INVOICE = Lifecycle(
	name="Sales Invoice",
	initial="Draft",
	transitions={
		"Draft": {"Pending Approval", "Posted / Unpaid", "Cancelled"},
		"Pending Approval": {"Posted / Unpaid", "Draft", "Cancelled"},
		"Posted / Unpaid": {"Partly Paid", "Paid", "Overdue", "Cancelled"},
		"Partly Paid": {"Paid", "Overdue", "Cancelled"},
		"Overdue": {"Partly Paid", "Paid", "Cancelled"},
		# Paid is not the end of the road. A receipt can be cancelled -- a
		# cheque bounces, a payment was matched to the wrong customer -- and
		# the invoice then owes again. Settlement moves it back to whichever
		# of these the ledger says is true. DEC-022.
		"Paid": {"Partly Paid", "Posted / Unpaid", "Overdue", "Cancelled"},
		"Cancelled": set(),
	},
	draft_states={"Draft", "Pending Approval"},
	submitted_states={"Posted / Unpaid", "Partly Paid", "Paid", "Overdue"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Pending Approval", "Posted / Unpaid", "Partly Paid", "Paid"),
)

# --- HR -------------------------------------------------------------------
#
# FR-HR-003 is recorded in the BRD as "Attendance & Leave" with the detail
# "TBD -- The BRD does not specify this detail." Both lifecycles below are
# therefore BRD-DERIVED under CD-001's ERP-standard-baseline rule, the same
# basis as every other lifecycle here whose source gives a name and no states.
# They are inferred, not quoted, and OQ-024 asks the owner to confirm them.

LEAVE_ALLOCATION = Lifecycle(
	name="Leave Allocation",
	initial="Draft",
	transitions={
		"Draft": {"Allocated", "Cancelled"},
		"Allocated": {"Cancelled"},
		"Cancelled": set(),
	},
	draft_states={"Draft"},
	submitted_states={"Allocated"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Allocated"),
)

# Rejected returns to Draft rather than ending the document, matching DEFAULT:
# a rejected request is usually re-dated and re-submitted, not re-typed. It is
# a draft state because a rejected application must not touch the ledger.
LEAVE_APPLICATION = Lifecycle(
	name="Leave Application",
	initial="Draft",
	transitions={
		"Draft": {"Pending Approval", "Cancelled"},
		"Pending Approval": {"Approved", "Rejected", "Draft"},
		"Approved": {"Cancelled"},
		"Rejected": {"Draft"},
		"Cancelled": set(),
	},
	draft_states={"Draft", "Pending Approval", "Rejected"},
	submitted_states={"Approved"},
	cancelling_states={"Cancelled"},
	happy_path=("Draft", "Pending Approval", "Approved"),
)


REGISTRY = {
	"KNIT 360 Journal Entry": JOURNAL_ENTRY,
	"KNIT 360 Sales Invoice": SALES_INVOICE,
	"KNIT 360 Lead": LEAD,
	"KNIT 360 Opportunity": OPPORTUNITY,
	"KNIT 360 Enquiry": ENQUIRY,
	"KNIT 360 Quotation": QUOTATION,
	"KNIT 360 Sales Order": SALES_ORDER,
	"KNIT 360 Delivery Note": DELIVERY_NOTE,
	"KNIT 360 Supplier": SUPPLIER,
	"KNIT 360 Sourcing Project": SOURCING_PROJECT,
	"KNIT 360 Request for Quotation": RFQ,
	"KNIT 360 Supplier Quotation": SUPPLIER_QUOTATION,
	"KNIT 360 Purchase Order": PURCHASE_ORDER,
	"KNIT 360 Goods Receipt": GOODS_RECEIPT,
	"KNIT 360 Quality Inspection": QUALITY_INSPECTION,
	"KNIT 360 Putaway Task": PUTAWAY_TASK,
	"KNIT 360 Supplier Invoice": SUPPLIER_INVOICE,
	"KNIT 360 Payment Entry": PAYMENT_ENTRY,
	"KNIT 360 Supplier Scorecard": SUPPLIER_SCORECARD,
	"KNIT 360 Asset": ASSET,
	"KNIT 360 Service Contract": SERVICE_CONTRACT,
	"KNIT 360 Service Dispatch": SERVICE_DISPATCH,
	"KNIT 360 Leave Allocation": LEAVE_ALLOCATION,
	"KNIT 360 Leave Application": LEAVE_APPLICATION,
}


def for_doctype(doctype):
	"""The lifecycle governing a doctype, or DEFAULT if it declares none."""
	return REGISTRY.get(doctype, DEFAULT)


# --- Module-level aliases for the DEFAULT lifecycle. ---
# Callers that are not doctype-aware keep working against the default.
STATES = DEFAULT.states
TRANSITIONS = DEFAULT.transitions
TERMINAL_STATES = DEFAULT.terminal_states
DRAFT_BACKED = DEFAULT.draft_states
SUBMITTED_BACKED = DEFAULT.submitted_states


def is_allowed(from_status, to_status):
	return DEFAULT.is_allowed(from_status, to_status)


def required_docstatus(to_status, current_docstatus):
	return DEFAULT.required_docstatus(to_status, current_docstatus)
