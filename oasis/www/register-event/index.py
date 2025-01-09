import frappe
from frappe.model.document import Document

def get_context(context):

    context.upcomingevents = frappe.db.get_list('Events',
        filters={"upcoming_event" : "1"},  
        fields=['event_title', 'name'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    return context

@frappe.whitelist(allow_guest=True)
def validate_form(data):
    data = frappe.parse_json(data)
    form_submission = frappe.new_doc("Event Registration Form")

    form_submission.user_name = data.get("user_name")
    form_submission.org_name = data.get("org_name")
    form_submission.city = data.get("city")
    form_submission.email = data.get("email")
    form_submission.number = data.get("number")
    form_submission.event = data.get("event")

    form_submission.insert()
    return {"success": True}
    