import frappe
def get_context(context):

    context.cards = frappe.db.get_list('Activities',
        filters={},  
        fields=['background_color', 'illustration', 'content_summary', 'cta_button_1_label', 'cta_button_2_label', 'cta_button_1_link', 'cta_button_2_link'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    return context