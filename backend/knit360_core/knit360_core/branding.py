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

	frappe.db.commit()
	frappe.clear_cache()
	return {"app_name": APP_NAME, "logo": LOGO}


def after_install():
	apply()


def after_migrate():
	apply()
