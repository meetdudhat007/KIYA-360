"""KNIT 360 Company — FR-PADM-1.1.1.

BRD descriptor: "Company Master -- company details, business type, legal entity, fiscal year, currency, tax registration"

Fields trace to that descriptor. The BRD specifies no further detail
(see docs/00-requirements/05-requirement-traceability.md), so anything
beyond it is marked TBD in the field description rather than invented.

A new company builds its own chart of accounts on insert. Until this hook
existed, only the demo and acceptance scripts called
finance.chart_of_accounts.setup(), so a company created through the normal
screen got no accounts at all -- and without a receivable account it cannot
raise an invoice. That left the first step of setting the product up for a
real client reachable only from a command line, which is no use to the person
doing the setting up.
"""

import frappe
from frappe.model.document import Document

from knit360_core.finance import chart_of_accounts


class KNIT360Company(Document):
	def after_insert(self):
		"""Give the company a chart of accounts, a cost centre and its defaults.

		setup() is idempotent by refusal, so this cannot double up on a company
		that already has a chart -- which is what makes it safe to call from a
		hook as well as by hand.
		"""
		chart_of_accounts.setup(self.name)
