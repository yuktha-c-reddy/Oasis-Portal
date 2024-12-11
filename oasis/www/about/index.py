import frappe
def get_context(context):
    context.members = [
        {
            "name": "Akhila Somanath", "title": "Co-Founder, Tech4Good Community", "profile": "/assets/oasis/images/image (1).png"
        },
        {
            "name": "Kailash Nadh", "title": "Co-Founder, Tech4Good Community", "profile": "/assets/oasis/images/image (2).png"
        },
        {
            "name": "Kuldeep Dantewadia", "title": "Co-Founder, Reap Benefit", "profile": "/assets/oasis/images/image (3).png"
        },
        {
            "name": "Moosa Mehar MP", "title": "Co-Founder, TinkerHub", "profile": "/assets/oasis/images/image (4).png"
        },
        {
            "name": "Poruri Sai Rahul", "title": "CEO, FOSS United", "profile": "/assets/oasis/images/image (5).png"
        },
        {
            "name": "Shemeer Babu", "title": "Co-Founder, Aikyam Fellows", "profile": "/assets/oasis/images/image (6).jpeg"
        },
        {
            "name": "Vinay Kumar", "title": "Software Engineer, Zerodha", "profile": "/assets/oasis/images/image (7).png"
        },
        {
            "name": "Vishnu Sudhakaran", "title": "Software Engineer, Zerodha", "profile": "/assets/oasis/images/image (8).png"
        }
    ]

    context.partners = frappe.db.get_list('Partners', 
        filters={}, 
        fields=['partner_name', 'key_partner', 'logo', 'icon', 'url', 'description'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    return context