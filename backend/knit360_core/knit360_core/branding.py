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


def after_install():
	apply()


def after_migrate():
	apply()
