"""KNIT 360 branding for the Frappe Desk and login page.

Frappe resolves its branding in a fixed order (frappe/www/login.py and
navbar_settings.get_app_logo):

    login heading  = Website Settings.app_name
                     or System Settings.app_name
                     or "Frappe"
    logo           = Website Settings.app_logo
                     or Navbar Settings.app_logo
                     or the app_logo_url hook

Hooks alone are therefore not enough: if either Settings record carries a
value, it wins. This module writes the Settings records directly and runs from
after_install and after_migrate so a fresh site is branded without manual steps.

This rebrands Frappe's Desk. It does not replace it — see docs: the UX layer is
a KNIT 360-owned seam (ADR-004), and Desk is an admin interface, not the customer
product.
"""

import frappe

APP_NAME = "KNIT 360"
LOGO = "/assets/knit360_core/images/knit360-logo.svg"


#: Replaces the framework's default "Built on <vendor>" website footer.
FOOTER = APP_NAME


def apply():
	"""Set every branding value Frappe consults. Idempotent.

	Written with set_single_value rather than doc.save(), because this runs from
	after_install: on a site that has not been through the setup wizard yet,
	System Settings has no language or time zone, and saving the whole document
	fails its own mandatory-field validation. Only these fields need to change,
	so the surrounding document is not this module's business.
	"""
	frappe.db.set_single_value(
		"Website Settings",
		{
			"app_name": APP_NAME,
			"app_logo": LOGO,
			"favicon": LOGO,
			"splash_image": LOGO,
			"brand_html": f'<img src="{LOGO}" alt="{APP_NAME}" style="height:24px">',
			"title_prefix": APP_NAME,
		},
	)

	if frappe.get_meta("System Settings").has_field("app_name"):
		frappe.db.set_single_value("System Settings", "app_name", APP_NAME)

	frappe.db.set_single_value("Navbar Settings", "app_logo", LOGO)

	# Website Settings.footer_powered is empty by default, and the footer
	# template then falls through to templates/includes/footer/footer_powered.html,
	# which renders "Built on Frappe" linking to frappeframework.com. Any
	# non-empty value replaces it, so setting one is the supported way to
	# change it -- the template is not edited.
	frappe.db.set_single_value("Website Settings", "footer_powered", FOOTER)

	hidden = hide_vendor_navbar_items()

	frappe.db.commit()
	frappe.clear_cache()
	return {"app_name": APP_NAME, "logo": LOGO, "navbar_items_hidden": hidden}


#: Navbar entries that sell another vendor's services. Hiding one is a
#: presentation choice, not a licence question: Frappe is MIT, which asks that
#: the copyright and permission notice travel with the software, and that notice
#: lives in the source and in LICENSE, not in a support-sales link.
#:
#: "About" is deliberately NOT in this list. It carries Frappe's attribution and
#: version, and removing attribution is a different decision from removing an
#: advert -- it belongs to the owner, not to this file.
VENDOR_NAVBAR_ITEMS = ("Frappe Support",)


def hide_vendor_navbar_items():
	"""Hide another vendor's marketing links from the Help menu.

	Navbar Item carries its own `hidden` flag, so this sets a supported field
	rather than deleting a row Frappe reinstalls on migrate.
	"""
	hidden = []
	for label in VENDOR_NAVBAR_ITEMS:
		for name in frappe.get_all(
			"Navbar Item", filters={"item_label": label, "hidden": 0}, pluck="name"
		):
			frappe.db.set_value("Navbar Item", name, "hidden", 1, update_modified=False)
			hidden.append(label)
	return hidden


#: What a letterhead is built from. Every line comes off the Company record,
#: so a client who fills their own details in gets their own letterhead and
#: nobody has to edit HTML -- DEC-038.
LETTERHEAD_FIELDS = (
	"company_name", "legal_entity", "registered_address",
	"contact_phone", "contact_email", "tax_registration_number",
)


def letterheads():
	"""One Letter Head per company, from the company's own details.

	Rebuilt on every migrate so a corrected address reaches the documents,
	but only where this app wrote it: a letterhead somebody has edited by
	hand is left alone, because their version is the one they chose.
	"""
	made = {}
	marker = "<!-- built by knit360_core.branding -->"

	for name in frappe.get_all("KNIT 360 Company", pluck="name"):
		row = frappe.db.get_value("KNIT 360 Company", name, LETTERHEAD_FIELDS, as_dict=True)
		lines = [
			'<div style="font-family: Georgia, Times, serif; '
			'border-bottom: 1.5px solid #111; padding-bottom: 10px; margin-bottom: 4px;">',
			'<div style="font-size: 16pt; letter-spacing: 1px;">'
			+ (row.company_name or name)
			+ "</div>",
		]
		detail = [
			row.legal_entity,
			" ".join((row.registered_address or "").split()) or None,
			row.contact_phone,
			row.contact_email,
			f"Tax registration {row.tax_registration_number}"
			if row.tax_registration_number else None,
		]
		detail = [part for part in detail if part]
		if detail:
			lines.append(
				'<div style="font-size: 9pt; color: #444; margin-top: 3px;">'
				+ " &middot; ".join(detail)
				+ "</div>"
			)
		lines.append("</div>")
		content = marker + "".join(lines)

		existing = frappe.db.get_value(
			"Letter Head", name, ["content", "is_default"], as_dict=True
		)
		if existing and marker not in (existing.content or ""):
			made[name] = "edited by hand, left alone"
			continue
		if existing:
			if existing.content != content:
				frappe.db.set_value("Letter Head", name, "content", content,
				                    update_modified=False)
				made[name] = "refreshed"
			continue

		frappe.get_doc(
			{
				"doctype": "Letter Head",
				"letter_head_name": name,
				"source": "HTML",
				"content": content,
				"is_default": 0 if frappe.db.exists("Letter Head", {"is_default": 1}) else 1,
			}
		).insert(ignore_permissions=True)
		made[name] = "created"

	return made


def after_install():
	apply()
	letterheads()


def after_migrate():
	apply()
	letterheads()
