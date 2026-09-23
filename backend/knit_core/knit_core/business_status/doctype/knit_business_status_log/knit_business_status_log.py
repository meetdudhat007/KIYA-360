"""Append-only record of every business status transition.

SF-008 requires an immutable audit entry per transition. Enforced here rather
than by permissions alone, so code paths using ignore_permissions cannot
rewrite history either.
"""

import frappe
from frappe.model.document import Document


class KNITBusinessStatusLog(Document):
	def validate(self):
		if self.get_doc_before_save():
			frappe.throw("Business status log entries are append-only and cannot be edited.")

	def on_trash(self):
		frappe.throw("Business status log entries cannot be deleted.")
