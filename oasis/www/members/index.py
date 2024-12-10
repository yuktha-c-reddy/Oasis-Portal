import frappe
def get_context(context):

    context.partners = frappe.db.get_list('partners', 
        filters={}, 
        fields=['partner_name', 'key_partner', 'logo', 'icon', 'url', 'description'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    return context