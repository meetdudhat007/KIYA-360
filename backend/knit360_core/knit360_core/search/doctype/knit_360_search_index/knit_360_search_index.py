"""KNIT 360 Search Index.

A derived row, not a document anybody authors. It is written only by
knit360_core.search.index, and a row edited by hand would describe a document
that does not look like that -- until the next time that document is saved,
when the edit would silently vanish. So an edit is refused rather than lost.

The indexer identifies itself with a flag rather than by `is_new()`. The first
version of this guard used is_new(), and it refused the indexer's own insert:
Frappe clears the new-document marker before it runs on_update, so by then an
insert and an edit look identical. A flag is set in memory only and is never
stored, so nothing a person does through the interface can carry it.
"""

import frappe
from frappe.model.document import Document


class KNIT360SearchIndex(Document):
	def validate(self):
		if not self.flags.written_by_indexer:
			frappe.throw(
				"A search index row describes a document; it is not written or "
				"edited on its own. Change the document itself, or rebuild the "
				"index with knit360_core.search.index.rebuild."
			)
