import frappe

def get_context(context):  
    context.partners = frappe.get_all('Partners',  
        fields=['partner_name', 'key_partner', 'logo', 'icon', 'url', 'description', 'contact'],
        order_by='creation asc'
    )

    casestudies = frappe.get_all('Case Studies', fields=['name', 'title', 'challenge', 'solution', 'category_tag', 'solution_partner'], order_by='creation asc')
    partner_id = [casestudy.solution_partner for casestudy in casestudies]
    partners = frappe.get_all('Partners', filters={'name': ['in', partner_id]}, fields=['partner_name', 'name', 'key_partner', 'logo', 'icon', 'url', 'description', 'contact'])
    partner_lookup = {partner.name: partner for partner in partners}

    get_partner = []
    for casestudy in casestudies:

        tools = frappe.get_all(
        'Tools Used',  
        filters={'parent': casestudy['name']},  
        fields=['tools_used']  
        )
        detailed_tools = []
        for tool in tools:  
            tool_details = frappe.get_value(
                'Case Study Tools',  
                tool['tools_used'],  
                ['name', 'logo', 'url']  
            )
            if tool_details:
                detailed_tools.append({
                    'name': tool_details[0],  
                    'logo': tool_details[1],  
                    'url': tool_details[2],  
                })

        casestudy['tools_used'] = detailed_tools
        partner = partner_lookup.get(casestudy['solution_partner'])
        if partner:
            get_partner.append({
                'name': casestudy['name'],
                'title': casestudy['title'],
                'challenge': casestudy['challenge'],
                'solution': casestudy['solution'],
                'category_tag': casestudy['category_tag'],
                'solution_partner': partner['logo'],
                'tools_used': casestudy['tools_used']
            })
        else:
            result.append({
                'name': casestudy['name'],
                'title': casestudy['title'],
                'challenge': casestudy['challenge'],
                'solution': casestudy['solution'],
                'category_tag': casestudy['category_tag'],
                'solution_partner': None,
                'tools_used': None
            })

    context.casestudies = get_partner


    context.cards = [ 
        {
            "background_color": "#FF94B8",
            "vector":"/assets/oasis/images/vector1.svg",
            "description":"Advocate FOSS technology adoption in the social sector via hands-on, evidence based showcasing of successful technology implementations.",
            "button_1":"case studies",
            "link_1":"",
            "button_2":"from oasis submit",
            "link_2":""
        },
        {
            "background_color": "#F5E253",
            "vector":"/assets/oasis/images/vector6.svg",
            "description":"Capacity and awareness building of FOSS technologies via workshops, training sessions, meetups, and technical demonstrations.",
            "button_1":"FOLLOW EVENTS",
            "link_1":"",
            "button_2":"WATCH A VIDEO",
            "link_2":""
        },
        {
            "background_color": "#85B4EF",
            "vector":"/assets/oasis/images/vector3.svg",
            "description":"Develop and disseminate educational resources, playbooks and case studies.",
            "button_1":"our forum",
            "link_1":"",
            "button_2":"read wiki", 
            "link_2":""
        },
        {
            "background_color": "#3CB645",
            "vector":"/assets/oasis/images/vector4.svg",
            "description":"Work with tech organisations and vendors to build easily usable, low-maintenance FOSS technologies tailor made for solving recurring problems in social sector organisations.",
            "button_1":"our forum",
            "link_1":"",
            "button_2":"read wiki",
            "link_2":""
        },
        {
            "background_color": "#FF6459",
            "vector":"/assets/oasis/images/vector5.svg",
            "description":"Engage with broader FOSS, technology, and social innovation communities and showcase opportunities in the social sector.",
            "button_1":"oru forum",
            "link_1":"",
            "button_2":"read wiki",
            "link_2":""
        },
    ]
        
    return context
