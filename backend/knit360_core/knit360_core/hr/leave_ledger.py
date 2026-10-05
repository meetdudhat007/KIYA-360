"""The leave ledger -- FR-HR-003. The only writer of KNIT 360 Leave Ledger Entry.

Why leave has a ledger at all.

The obvious design is a `leave_balance` field on the employee that goes up when
leave is granted and down when it is taken. It is wrong for the same reason it
is wrong in accounting: a stored total is a second copy of the truth, and the
moment it disagrees with the documents behind it there is no way to tell which
is right.

So a balance here is never stored. It is the sum of a ledger of signed entries:
an allocation writes a positive number, an approved application writes a
negative one, and the balance is what they add up to. That makes every balance
explainable -- you can always list the entries that produced it -- and it makes
a wrong balance impossible to have without a wrong document behind it.

This mirrors knit360_core.finance.ledger deliberately, including the parts that
look like restrictions:

  - entries are never edited and never deleted
  - a cancellation writes an equal and opposite entry and flags both
  - this module is the only thing that writes the table

The two ledgers stay separate modules rather than sharing a base class. They
answer different questions, their entries carry different fields, and a shared
abstraction between two tables with one writer each would be indirection
bought with nothing.
"""

import frappe
from frappe.utils import flt, getdate

LEDGER = "KNIT 360 Leave Ledger Entry"
LEAVE_TYPE = "KNIT 360 Leave Type"

#: Balances are in days and half-days are real, so comparisons allow for
#: floating point without allowing for a materially wrong figure.
TOLERANCE = 0.001


def post(voucher_type, voucher_no, employee, leave_type, company, posting_date,
         leaves, from_date=None, to_date=None, leave_period=None, remarks=None):
	"""Write one entry. Positive grants balance, negative consumes it.

	Returns the entry's name.
	"""
	leaves = flt(leaves)
	if not leaves:
		frappe.throw(
			f"{voucher_type} {voucher_no}: an entry of zero days moves nothing. "
			f"Nothing is written."
		)
	if existing(voucher_type, voucher_no):
		frappe.throw(
			f"{voucher_type} {voucher_no} has already been posted to the leave "
			f"ledger. Cancel it before posting again."
		)

	entry = frappe.get_doc(
		{
			"doctype": LEDGER,
			"employee": employee,
			"leave_type": leave_type,
			"company": company,
			"posting_date": getdate(posting_date),
			"leaves": leaves,
			"from_date": getdate(from_date) if from_date else None,
			"to_date": getdate(to_date) if to_date else None,
			"leave_period": leave_period,
			"voucher_type": voucher_type,
			"voucher_no": voucher_no,
			"is_cancelled": 0,
			"remarks": remarks,
		}
	).insert(ignore_permissions=True)
	return entry.name


def reverse(voucher_type, voucher_no, posting_date=None):
	"""Undo a voucher's effect by writing its opposite, not by deleting it.

	Both the original and the reversal are flagged cancelled, so a balance
	query ignores the pair while the history keeps them.
	"""
	originals = frappe.get_all(
		LEDGER,
		filters={"voucher_type": voucher_type, "voucher_no": voucher_no, "is_cancelled": 0},
		fields=["name", "employee", "leave_type", "company", "leaves", "from_date",
		        "to_date", "leave_period", "posting_date"],
	)
	if not originals:
		return []

	written = []
	for row in originals:
		contra = frappe.get_doc(
			{
				"doctype": LEDGER,
				"employee": row.employee,
				"leave_type": row.leave_type,
				"company": row.company,
				"posting_date": getdate(posting_date or row.posting_date),
				"leaves": -flt(row.leaves),
				"from_date": row.from_date,
				"to_date": row.to_date,
				"leave_period": row.leave_period,
				"voucher_type": voucher_type,
				"voucher_no": voucher_no,
				"is_cancelled": 1,
				"remarks": f"Reversal of {row.name}",
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value(LEDGER, row.name, "is_cancelled", 1, update_modified=False)
		written.append(contra.name)
	return written


@frappe.whitelist()
def balance(employee, leave_type, on_date=None, company=None):
	"""Days available: the sum of every live entry, and nothing else.

	`on_date` gives the balance as it stood on a date, which is what an
	application must check against -- not today's balance, but the balance on
	the day the leave starts.
	"""
	filters = {"employee": employee, "leave_type": leave_type, "is_cancelled": 0}
	if company:
		filters["company"] = company
	if on_date:
		filters["posting_date"] = ["<=", getdate(on_date)]

	total = frappe.db.get_value(LEDGER, filters, "sum(leaves)")
	return flt(total)


@frappe.whitelist()
def entries(voucher_type, voucher_no, include_cancelled=0):
	"""The ledger effect of one document, for showing on that document."""
	filters = {"voucher_type": voucher_type, "voucher_no": voucher_no}
	if not int(include_cancelled or 0):
		filters["is_cancelled"] = 0
	return frappe.get_all(
		LEDGER,
		filters=filters,
		fields=["name", "posting_date", "employee", "leave_type", "leaves",
		        "from_date", "to_date", "is_cancelled", "remarks"],
		order_by="posting_date, creation",
	)


def existing(voucher_type, voucher_no):
	"""Whether a voucher already has live entries. Guards double posting."""
	return frappe.db.exists(
		LEDGER,
		{"voucher_type": voucher_type, "voucher_no": voucher_no, "is_cancelled": 0},
	)


@frappe.whitelist()
def statement(employee, leave_type=None, company=None):
	"""Every live entry for an employee, with a running balance.

	FR-HR-007. This is the answer to "why is my balance what it is", which is
	the question a stored total can never answer.
	"""
	filters = {"employee": employee, "is_cancelled": 0}
	if leave_type:
		filters["leave_type"] = leave_type
	if company:
		filters["company"] = company

	rows = frappe.get_all(
		LEDGER,
		filters=filters,
		fields=["name", "posting_date", "leave_type", "leaves", "from_date", "to_date",
		        "voucher_type", "voucher_no", "remarks"],
		order_by="leave_type, posting_date, creation",
	)

	running = {}
	for row in rows:
		running[row.leave_type] = flt(running.get(row.leave_type, 0)) + flt(row.leaves)
		row["balance"] = running[row.leave_type]
	return rows


def check_can_consume(employee, leave_type, days, on_date=None, company=None):
	"""Refuse an application that exceeds the balance, unless the type allows it.

	Called from the application rather than from post(), because the refusal
	belongs where a person can still do something about it -- while the
	document is a draft -- and not at the moment it posts.
	"""
	if flt(days) <= 0:
		return

	available = balance(employee, leave_type, on_date=on_date, company=company)
	if flt(days) - available <= TOLERANCE:
		return

	if frappe.db.get_value(LEAVE_TYPE, leave_type, "allow_negative_balance"):
		return

	frappe.throw(
		f"{employee} has {available:g} day(s) of {leave_type} available and this "
		f"application is for {flt(days):g}. Allocate more leave, or allow a "
		f"negative balance on the leave type."
	)
