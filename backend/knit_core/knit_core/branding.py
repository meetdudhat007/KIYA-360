"""KNIT branding for the Frappe Desk and login page.

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
a KNIT-owned seam (ADR-004), and Desk is an admin interface, not the customer
product.
"""

import frappe

APP_NAME = "KNIT"
LOGO = "/assets/knit_core/images/knit-logo.svg"


def apply():
	"""Set every branding value Frappe consults. Idempotent."""
	website = frappe.get_single("Website Settings")
	website.app_name = APP_NAME
	website.app_logo = LOGO
	website.favicon = LOGO
	website.splash_image = LOGO
	website.brand_html = f'<img src="{LOGO}" alt="{APP_NAME}" style="height:24px">'
	website.title_prefix = APP_NAME
	website.save(ignore_permissions=True)

	system = frappe.get_single("System Settings")
	if hasattr(system, "app_name"):
		system.app_name = APP_NAME
		system.save(ignore_permissions=True)

	navbar = frappe.get_single("Navbar Settings")
	navbar.app_logo = LOGO
	navbar.save(ignore_permissions=True)

	frappe.db.commit()
	frappe.clear_cache()
	return {"app_name": APP_NAME, "logo": LOGO}


def after_install():
	apply()


def after_migrate():
	apply()
