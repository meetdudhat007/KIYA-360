"""One way in -- FR-FIN-001, CD-002, CD-006.

CD-002 makes the business status the lifecycle, and the adapter derives
docstatus from it. That holds only while the adapter is the *only* thing that
moves docstatus, and until now it was not: Frappe decides to run on_submit from
the docstatus transition alone, so a Desk user pressing Submit would post to the
general ledger with the business status left behind.

These handlers are registered on every doctype through doc_events["*"] and do
nothing at all unless the doctype has a registered lifecycle. For one that does,
submission and cancellation must carry the flag the engine sets, and there is no
way to set that flag except by going through engine.transition.

The effect is that a governed document has exactly one path to docstatus 1, and
the ledger posting hung on on_submit inherits that guarantee for free.
"""

import frappe

from knit360_core.business_status import model

#: Set by engine._apply_docstatus immediately before submit() or cancel().
FLAG = "knit360_lifecycle"


def _governed(doc):
	return doc.doctype in model.REGISTRY


def _refuse(doc, action):
	lifecycle = model.for_doctype(doc.doctype)
	frappe.throw(
		f"{doc.doctype} {doc.name or ''} cannot be {action} directly. "
		f"Its '{lifecycle.name}' lifecycle governs docstatus (CD-002), so move its "
		f"business status instead -- knit360_core.business_status.engine.transition. "
		f"Submitting around the lifecycle would post its effects with the status "
		f"left behind.".strip()
	)


def before_submit(doc, method=None):
	if _governed(doc) and not doc.flags.get(FLAG):
		_refuse(doc, "submitted")


def before_cancel(doc, method=None):
	if _governed(doc) and not doc.flags.get(FLAG):
		_refuse(doc, "cancelled")
