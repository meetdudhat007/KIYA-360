"""Desk workspaces for KNIT 360 -- the module tiles and sidebar.

Frappe's Desk shows nothing for a module until a Workspace record exists for it.
ERPNext ships its own; KNIT 360 had none, so all 73 doctypes were reachable only
by typing a URL.

These are built from the DocType table rather than from a hand-written list, so
a doctype added to a module appears on its workspace at the next migrate and
cannot drift out of sync. Only the ordering, icons and which few doctypes earn a
shortcut are declared here.

Runs from after_migrate alongside branding.
"""

import json

import frappe

WORKSPACE = "Workspace"
PREFIX = "KNIT 360 "

#: module -> (icon, sequence, shortcut doctypes, named cards).
#: Icons are ids from Frappe's own sprite, without the "icon-" prefix.
#: Any doctype not placed in a named card falls into a default card.
MODULES = {
	"Platform": ("organization", 10, ["Company", "Location"], {}),
	"CRM": ("crm", 20, ["Lead", "Opportunity", "Customer"], {}),
	"Sales": ("sell", 30, ["Enquiry", "Quotation", "Sales Order", "Delivery Note"], {}),
	"Finance": ("accounting", 40, ["Sales Invoice", "Payment Entry", "Journal Entry", "Account"], {
		"Ledger": ["Account", "GL Entry", "Journal Entry", "Cost Center", "Fiscal Year"],
		"Receivables": ["Sales Invoice", "Payment Term", "Payment Terms Template"],
		"Payables": ["Supplier Invoice", "Payment Entry", "Mode of Payment"],
	}),
	"Tax": ("income", 50, ["Tax Template"], {}),
	"Procurement": ("buying", 60, ["Purchase Requisition", "Request for Quotation", "Purchase Order", "Goods Receipt"], {}),
	"Supplier Management": ("users", 70, ["Supplier", "Supplier Scorecard"], {}),
	"Inventory": ("stock", 80, ["Item", "Stock Ledger Entry", "Item Price"], {
		"Stock": ["Item", "Item Price", "Stock Ledger Entry", "Stock Reservation"],
		"Movements": ["Goods Receipt", "Delivery Note"],
	}),
	"Warehouse": ("retail", 90, ["Warehouse", "Bin", "Putaway Task"], {}),
	"MRP": ("milestone", 100, ["Material Plan"], {}),
	"Manufacturing": ("tool", 110, ["BOM", "Work Order"], {}),
	"Quality": ("quality", 120, ["Quality Inspection", "Non Conformance Report"], {}),
	"Asset Management": ("assets", 130, ["Asset"], {}),
	"Maintenance": ("support", 140, ["Service Request", "Field Work Order", "Service Contract"], {}),
	"HR": ("users", 145, ["Employee", "Leave Application", "Leave Allocation", "Leave Type"], {
		"People": ["Employee", "Designation", "Department"],
		"Leave": ["Leave Type", "Leave Period", "Leave Allocation", "Leave Application",
		          "Leave Ledger Entry"],
		"Calendar": ["Holiday List"],
	}),
	"Business Status": ("workflow", 150, ["Business Status Log"], {}),
}

#: The landing workspace, above the modules.
HOME = {
	"label": "KNIT 360",
	"icon": "getting-started",
	"module": "Platform",
	"sequence": 1,
	"shortcuts": [
		("URL", "/knit360", "Customer to Cash", "Green"),
		("DocType", PREFIX + "Lead", "Leads", "Blue"),
		("DocType", PREFIX + "Sales Order", "Sales Orders", "Blue"),
		("DocType", PREFIX + "Sales Invoice", "Sales Invoices", "Orange"),
	],
}


def _doctypes(module):
	"""Every non-child doctype in a module, alphabetically."""
	return sorted(
		frappe.get_all(
			"DocType",
			filters={"module": module, "istable": 0, "issingle": 0},
			pluck="name",
		)
	)


def _exists(doctype):
	"""Whether a doctype is installed, regardless of which module owns it."""
	return bool(frappe.db.exists("DocType", doctype))


def _short(name):
	return name[len(PREFIX):] if name.startswith(PREFIX) else name


def _block(kind, data):
	# The id only has to be unique within the page; Frappe generates random
	# ones, but a stable id keeps the JSON diffable between migrations.
	data = dict(data)
	seed = f"{kind}-{sorted(data.items())}"
	return {"id": f"knit{abs(hash(seed)) % 10**10}", "type": kind, "data": data}


def _content(shortcut_labels, card_labels):
	blocks = []
	if shortcut_labels:
		blocks.append(_block("header", {"text": "<span class='h4'><b>Shortcuts</b></span>", "col": 12}))
		blocks += [_block("shortcut", {"shortcut_name": label, "col": 3}) for label in shortcut_labels]
	if card_labels:
		blocks.append(_block("header", {"text": "<span class='h4'><b>Documents</b></span>", "col": 12}))
		blocks += [_block("card", {"card_name": label, "col": 4}) for label in card_labels]
	return json.dumps(blocks)


def _upsert(label, icon, module, sequence, shortcuts, cards):
	"""shortcuts: [(type, link_to, label, color)]. cards: {card label: [doctype]}."""
	if frappe.db.exists(WORKSPACE, label):
		doc = frappe.get_doc(WORKSPACE, label)
		doc.links = []
		doc.shortcuts = []
	else:
		doc = frappe.new_doc(WORKSPACE)
		doc.label = label

	doc.title = label
	doc.icon = icon
	doc.module = module
	doc.public = 1
	doc.sequence_id = sequence
	doc.is_hidden = 0

	for kind, link_to, shortcut_label, color in shortcuts:
		row = {"type": kind, "label": shortcut_label, "color": color}
		if kind == "URL":
			row["url"] = link_to
		else:
			row["link_to"] = link_to
		doc.append("shortcuts", row)

	for card_label, doctypes in cards.items():
		doc.append("links", {
			"type": "Card Break", "label": card_label, "link_count": len(doctypes),
		})
		for doctype in doctypes:
			doc.append("links", {
				"type": "Link", "label": _short(doctype),
				"link_type": "DocType", "link_to": doctype, "link_count": 0,
			})

	doc.content = _content([s[2] for s in shortcuts], list(cards))
	doc.save(ignore_permissions=True)
	return doc.name


def build():
	"""Create or refresh every KNIT 360 workspace. Idempotent."""
	built = []

	built.append(_upsert(
		HOME["label"], HOME["icon"], HOME["module"], HOME["sequence"],
		HOME["shortcuts"],
		{"Customer to Cash": [PREFIX + n for n in
		                      ("Lead", "Opportunity", "Enquiry", "Quotation", "Sales Order",
		                       "Delivery Note", "Sales Invoice")]},
	))

	for module, (icon, sequence, shortcut_names, named_cards) in MODULES.items():
		doctypes = _doctypes(module)
		if not doctypes:
			continue

		placed, cards = set(), {}
		for card_label, wanted in named_cards.items():
			# A named card may reach into another module. HR needs Employee,
			# which lives in Platform because the BRD traces it to FR-PADM-1.4.4
			# rather than to FR-HR-001. Linking to it is cheaper and more honest
			# than moving a doctype away from the requirement it came from.
			rows = [PREFIX + n for n in wanted if _exists(PREFIX + n)]
			if rows:
				cards[card_label] = rows
				placed.update(rows)
		rest = [d for d in doctypes if d not in placed]
		if rest:
			cards.setdefault(module, []).extend(rest)

		shortcuts = [
			("DocType", PREFIX + n, _short(PREFIX + n), "Blue")
			for n in shortcut_names
			if _exists(PREFIX + n)
		]
		built.append(_upsert(module, icon, module, sequence, shortcuts, cards))

	frappe.db.commit()
	frappe.clear_cache()
	return built


def after_migrate():
	build()
