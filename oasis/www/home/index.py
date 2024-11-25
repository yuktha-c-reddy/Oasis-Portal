import frappe

def clear_specific_cache(doc, method):
    if doc.doctype == 'partners':
        cache_key = f'home_partners_data:{frappe.db.get_value("DocType", "partners", "modified")}'
        frappe.cache().delete_value(cache_key)
    elif doc.doctype == 'case studies':
        cache_key = (
            f'home_cases_data:'
            f'{frappe.db.get_value("DocType", "case studies", "modified")}:'
            f'{frappe.db.get_value("DocType", "case study tools", "modified")}'
        )
        frappe.cache().delete_value(cache_key)

def get_context(context):
    partners = get_cached_partners()
    casestudies = get_cached_casestudies()
    cards = [ 
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
            "vector":"/assets/oasis/images/vector2.svg",
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

    tools = [
        {
            "logo": "/assets/oasis/images/tools2.png"
        },
        {
            "logo": "/assets/oasis/images/tool2.png"
        },
        {
            "logo": "/assets/oasis/images/tool3.png"
        },
        {
            "logo": "/assets/oasis/images/tool4.png"
        },
        {
            "logo": "/assets/oasis/images/tool5.png"
        },
        {
            "logo": "/assets/oasis/images/tool6.png"
        },
        {
            "logo": "/assets/oasis/images/tool7.png"
        },
        {
            "logo": "/assets/oasis/images/tool8.png"
        },
        {
            "logo": "/assets/oasis/images/tool9.png"
        },
        {
            "logo": "/assets/oasis/images/tool10.png"
        },
        {
            "logo": "/assets/oasis/images/tool11.png"
        },
        {
            "logo": "/assets/oasis/images/tool12.png"
        },
        {
            "logo": "/assets/oasis/images/tool13.png"
        },
        {
            "logo": "/assets/oasis/images/tool14.png"
        },
        {
            "logo": "/assets/oasis/images/tool15.png"
        },
        {
            "logo": "/assets/oasis/images/tool16.png"
        }
    ]
    
    context.update({
        'partners': partners,
        'casestudies': casestudies,
        'cards': cards,
        'tools': tools, 
    })
    return context

def get_cached_partners():
    cache_key = f'home_partners_data:{frappe.db.get_value("DocType", "partners", "modified")}'
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        print("partners cached data",cache_key)
        return cached_data

    print("partners cached data gone",cache_key)
    partners = frappe.get_all('partners',  
        fields=['partner_name', 'key_partner', 'logo', 'icon', 'url'],
        order_by='creation asc'
    )
    
    frappe.cache().set_value(cache_key, partners, expires_in_sec=3600)
    return partners

def get_cached_casestudies():
    cache_key = (
        f'home_cases_data:'
        f'{frappe.db.get_value("DocType", "case studies", "modified")}:'
        f'{frappe.db.get_value("DocType", "case study tools", "modified")}'
    )
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        print("casestudies cached data",cache_key)
        return cached_data
        
    print("Cache MISS for case studies",cache_key)
    casestudies = frappe.db.sql("""
        SELECT 
            cs.name, cs.title, cs.challenge, cs.solution, 
            cs.category_tag, p.logo as solution_partner
        FROM `tabcase studies` cs
        LEFT JOIN `tabpartners` p ON p.name = cs.solution_partner
        ORDER BY cs.creation asc
    """, as_dict=True)

    case_names = [c.name for c in casestudies]
    tools = frappe.db.sql("""
        SELECT tu.parent, cst.name, cst.logo, cst.url
        FROM `tabtools used` tu
        LEFT JOIN `tabcase study tools` cst ON cst.name = tu.tools_used
        WHERE tu.parent IN %(cases)s
    """, {'cases': case_names}, as_dict=True)

    tools_by_case = {}
    for tool in tools:
        if tool.parent not in tools_by_case:
            tools_by_case[tool.parent] = []
        tools_by_case[tool.parent].append({
            'name': tool.name,
            'logo': tool.logo,
            'url': tool.url
        })
    colors = ["#FF94B8", "#94FFCD", "#94DBFF", "#FFB694"]

    casestudies = [{
        'name': cs.name,
        'title': cs.title,
        'challenge': cs.challenge,
        'solution': cs.solution,
        'category_tag': cs.category_tag,
        'solution_partner': cs.solution_partner,
        'tools_used': tools_by_case.get(cs.name, []),
    } for cs in casestudies]
    
    
    frappe.cache().set_value(cache_key, casestudies, expires_in_sec=3600)
    return casestudies

# def get_context(context):  
#     context.partners = frappe.get_all('partners',  
#         fields=['partner_name', 'key_partner', 'logo', 'icon', 'url'],
#         order_by='creation asc'
#     )

#     # 2. Use joins instead of multiple queries
#     casestudies = frappe.db.sql("""
#         SELECT 
#             cs.name, cs.title, cs.challenge, cs.solution, 
#             cs.category_tag, p.logo as solution_partner
#         FROM `tabcase studies` cs
#         LEFT JOIN `tabpartners` p ON p.name = cs.solution_partner
#         ORDER BY cs.creation asc
#     """, as_dict=True)

#     # 3. Batch fetch tools in a single query
#     case_names = [c.name for c in casestudies]
#     tools = frappe.db.sql("""
#         SELECT tu.parent, cst.name, cst.logo, cst.url
#         FROM `tabtools used` tu
#         LEFT JOIN `tabcase study tools` cst ON cst.name = tu.tools_used
#         WHERE tu.parent IN %(cases)s
#     """, {'cases': case_names}, as_dict=True)

#     # 4. Organize tools by case study
#     tools_by_case = {}
#     for tool in tools:
#         if tool.parent not in tools_by_case:
#             tools_by_case[tool.parent] = []
#         tools_by_case[tool.parent].append({
#             'name': tool.name,
#             'logo': tool.logo,
#             'url': tool.url
#         })

#     # 5. Build final case studies list
#     context.casestudies = [{
#         'name': cs.name,
#         'title': cs.title,
#         'challenge': cs.challenge,
#         'solution': cs.solution,
#         'category_tag': cs.category_tag,
#         'solution_partner': cs.solution_partner,
#         'tools_used': tools_by_case.get(cs.name, [])
#     } for cs in casestudies]

#     # casestudies = frappe.get_all('case studies', fields=['name', 'title', 'challenge', 'solution', 'category_tag', 'solution_partner'], order_by='creation asc')
#     # partner_id = [casestudy.solution_partner for casestudy in casestudies]
#     # partners = frappe.get_all('partners', filters={'name': ['in', partner_id]}, fields=['partner_name', 'name', 'key_partner', 'logo', 'icon', 'url', 'description', 'contact'])
#     # partner_lookup = {partner.name: partner for partner in partners}

#     # get_partner = []
#     # for casestudy in casestudies:

#     #     tools = frappe.get_all(
#     #     'tools used',  
#     #     filters={'parent': casestudy['name']},  
#     #     fields=['tools_used']  
#     #     )
#     #     detailed_tools = []
#     #     for tool in tools:  
#     #         tool_details = frappe.get_value(
#     #             'case study tools',  
#     #             tool['tools_used'],  
#     #             ['name', 'logo', 'url']  
#     #         )
#     #         if tool_details:
#     #             detailed_tools.append({
#     #                 'name': tool_details[0],  
#     #                 'logo': tool_details[1],  
#     #                 'url': tool_details[2],  
#     #             })

#     #     casestudy['tools_used'] = detailed_tools
#     #     partner = partner_lookup.get(casestudy['solution_partner'])
#     #     if partner:
#     #         get_partner.append({
#     #             'name': casestudy['name'],
#     #             'title': casestudy['title'],
#     #             'challenge': casestudy['challenge'],
#     #             'solution': casestudy['solution'],
#     #             'category_tag': casestudy['category_tag'],
#     #             'solution_partner': partner['logo'],
#     #             'tools_used': casestudy['tools_used']
#     #         })
#     #     else:
#     #         result.append({
#     #             'name': casestudy['name'],
#     #             'title': casestudy['title'],
#     #             'challenge': casestudy['challenge'],
#     #             'solution': casestudy['solution'],
#     #             'category_tag': casestudy['category_tag'],
#     #             'solution_partner': None,
#     #             'tools_used': None
#     #         })

#     # context.casestudies = get_partner


#     # context.cards = [ 
#     #     {
#     #         "background_color": "#FF94B8",
#     #         "vector":"/assets/oasis/images/vector1.svg",
#     #         "description":"Advocate FOSS technology adoption in the social sector via hands-on, evidence based showcasing of successful technology implementations.",
#     #         "button_1":"case studies",
#     #         "link_1":"",
#     #         "button_2":"from oasis submit",
#     #         "link_2":""
#     #     },
#     #     {
#     #         "background_color": "#F5E253",
#     #         "vector":"/assets/oasis/images/vector2.svg",
#     #         "description":"Capacity and awareness building of FOSS technologies via workshops, training sessions, meetups, and technical demonstrations.",
#     #         "button_1":"FOLLOW EVENTS",
#     #         "link_1":"",
#     #         "button_2":"WATCH A VIDEO",
#     #         "link_2":""
#     #     },
#     #     {
#     #         "background_color": "#85B4EF",
#     #         "vector":"/assets/oasis/images/vector3.svg",
#     #         "description":"Develop and disseminate educational resources, playbooks and case studies.",
#     #         "button_1":"our forum",
#     #         "link_1":"",
#     #         "button_2":"read wiki", 
#     #         "link_2":""
#     #     },
#     #     {
#     #         "background_color": "#3CB645",
#     #         "vector":"/assets/oasis/images/vector4.svg",
#     #         "description":"Work with tech organisations and vendors to build easily usable, low-maintenance FOSS technologies tailor made for solving recurring problems in social sector organisations.",
#     #         "button_1":"our forum",
#     #         "link_1":"",
#     #         "button_2":"read wiki",
#     #         "link_2":""
#     #     },
#     #     {
#     #         "background_color": "#FF6459",
#     #         "vector":"/assets/oasis/images/vector5.svg",
#     #         "description":"Engage with broader FOSS, technology, and social innovation communities and showcase opportunities in the social sector.",
#     #         "button_1":"oru forum",
#     #         "link_1":"",
#     #         "button_2":"read wiki",
#     #         "link_2":""
#     #     },
#     # ]
        
#     return context
