import frappe
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def validate_form(data):
    data = frappe.parse_json(data)
    form_submission = frappe.new_doc("Join Us Form")

    form_submission.organization_name = data.get("organization_name")
    form_submission.category = data.get("category")
    form_submission.contact_person = data.get("contact_person")
    form_submission.email = data.get("email")
    form_submission.phone = data.get("phone")
    form_submission.web_link = data.get("web_link")
    form_submission.primary_sector_of_work = data.get("primary_sector_of_work")
    form_submission.challenges_with_technology = data.get("challenges_with_technology")
    form_submission.current_use_of_technology = data.get("current_use_of_technology")
    form_submission.expectations_or_ideas = data.get("expectations_or_ideas")
    form_submission.specialization = data.get("specialization")
    form_submission.experience_with_foss = data.get("experience_with_foss")
    form_submission.motivation_to_work_with_social_sector = data.get("motivation_to_work_with_social_sector")
    form_submission.additional_information = data.get("additional_information")

    form_submission.insert()
    return {"success": True}