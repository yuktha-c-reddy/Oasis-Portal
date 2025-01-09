import frappe
def get_context(context):

    context.upcomingevents = frappe.db.get_list('Events',
        filters={"upcoming_event" : "1"},  
        fields=['event_title', 'start_date', 'end_date', 'description', 'banner', 'upcoming_event', 'event_location', 'tag'],
        order_by='creation asc',
        limit_page_length=50
    )

    context.pastevents = frappe.db.get_list('Events',
        filters={"upcoming_event" : "0"},  
        fields=['event_title', 'start_date', 'end_date', 'description', 'banner', 'upcoming_event', 'event_location', 'tag'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    return context