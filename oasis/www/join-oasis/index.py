import frappe
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def validate_form(data):
    data = frappe.parse_json(data)
    form_submission = frappe.new_doc("join oasis")

    form_submission.name = data.get("name")
    form_submission.category = data.get("category")
    form_submission.city = data.get("city")
    form_submission.primary_contact = data.get("primary_contact")
    form_submission.email = data.get("email")
    form_submission.mobile_no = data.get("mobile_no")
    form_submission.website = data.get("website")
    form_submission.foss_usage_rate = data.get("foss_usage_rate")
    form_submission.expectations_oasis = data.get("expectations_oasis")
    form_submission.org_mission_allignment = data.get("org_mission_allignment")

    form_submission.insert()
    return {"success": True}