"""Warranty and contract cover -- FR-MFS-006, DR-A2S-003.

Answers one question: on a given day, what did a unit's agreements cover?

Cover is judged from each contract's own dates, not from its status label. A
label is moved by a person or by the nightly job below and can lag the
calendar; a date cannot. The status still matters at its two ends: a Draft has
not been agreed, and a Voided / Terminated contract has been withdrawn, so
neither covers anything. An Expired contract still covered the days inside its
dates, and a fault reported on one of those days is judged on that day.

Where two agreements cover the same thing, a warranty wins over a paid
contract, because a fault the maker must fix free is not the customer's
contract's to absorb. Which repairs a warranty excludes -- misuse, tampering --
is the client's policy and is not built (`OQ-011`); the service invoice is
raised as a draft so the office can correct a line before it posts.
"""

import frappe
from frappe.utils import getdate, nowdate

CONTRACT = "KNIT 360 Service Contract"

ACTIVE = "Active / In Coverage"
EXPIRING = "Expiring Soon"
EXPIRED = "Expired"
IN_FORCE = (ACTIVE, EXPIRING, EXPIRED)

WARRANTY_TYPES = ("Standard Warranty", "Extended Warranty")

BILLABLE = "Billable to Customer"
WARRANTY = "Warranty Covered"
CONTRACT_COVERED = "Contract Covered"

PART, LABOUR, TRAVEL = "Spare Part", "Labour", "Travel"

#: Which tick box on the contract decides each kind of line.
BOX = {PART: "parts_covered", LABOUR: "labor_covered", TRAVEL: "travel_covered"}


def contracts_on(asset, on_date=None):
	"""The agreements that covered `asset` on `on_date`, latest-ending first."""
	if not asset:
		return []
	day = getdate(on_date or nowdate())
	return frappe.get_all(
		CONTRACT,
		filters={
			"asset": asset,
			"knit360_business_status": ["in", IN_FORCE],
			"start_date": ["<=", day],
			"end_date": [">=", day],
		},
		fields=["name", "contract_type", "parts_covered", "labor_covered", "travel_covered",
		        "start_date", "end_date"],
		order_by="end_date desc",
	)


def cover_for(line_type, contracts):
	"""Warranty Covered, Contract Covered or Billable to Customer for one line."""
	box = BOX.get(line_type)
	if not box:
		return BILLABLE
	for contract in contracts:
		if contract.contract_type in WARRANTY_TYPES and contract.get(box):
			return WARRANTY
	for contract in contracts:
		if contract.contract_type not in WARRANTY_TYPES and contract.get(box):
			return CONTRACT_COVERED
	return BILLABLE


def summary(asset, on_date=None):
	"""A one-line description of the cover, and the contract giving it."""
	contracts = contracts_on(asset, on_date)
	if not contracts:
		return "Not covered", None
	first = contracts[0]
	covers = [label for label, box in (("parts", "parts_covered"), ("labour", "labor_covered"),
	                                   ("travel", "travel_covered")) if first.get(box)]
	what = ", ".join(covers) if covers else "nothing ticked"
	return f"{first.contract_type} to {first.end_date.strftime('%d-%m-%Y')}: {what}"[:140], first.name


@frappe.whitelist()
def cover(asset, on_date=None):
	"""What a unit's agreements cover on a day, for a screen to show."""
	frappe.get_doc("KNIT 360 Asset", asset).check_permission("read")
	label, contract = summary(asset, on_date)
	return {"label": label, "contract": contract}


def expire_contracts():
	"""Move contracts whose end date has passed to Expired. Runs daily.

	Cover does not depend on this -- it is judged from dates -- but a list that
	shows a lapsed warranty as in force misleads whoever reads it.
	"""
	from knit360_core.business_status import engine

	names = frappe.get_all(
		CONTRACT,
		filters={
			"knit360_business_status": ["in", (ACTIVE, EXPIRING)],
			"end_date": ["<", getdate(nowdate())],
		},
		pluck="name",
	)
	for name in names:
		engine.transition(CONTRACT, name, EXPIRED, reason="The end date has passed.")
	frappe.db.commit()
	return names
