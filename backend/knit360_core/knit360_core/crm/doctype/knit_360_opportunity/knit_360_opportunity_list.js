// Every CRM list's look (DEC-059): see public/js/crm_lists.bundle.js.
frappe.listview_settings["KNIT 360 Opportunity"] = {
	onload: (listview) => knit360.crm_list.setup(listview),
};
