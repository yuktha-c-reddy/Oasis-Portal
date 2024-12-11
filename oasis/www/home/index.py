import frappe

def clear_specific_cache(doc, method):
    if doc.doctype == 'Partners':
        cache_key = f'home_partners_data:{frappe.db.get_value("DocType", "Partners", "modified")}'
        frappe.cache().delete_value(cache_key)
    elif doc.doctype == 'Case Studies':
        cache_key = (
            f'home_cases_data:'
            f'{frappe.db.get_value("DocType", "Case Studies", "modified")}:'
            f'{frappe.db.get_value("DocType", "Case Study Tools", "modified")}'
        )
        frappe.cache().delete_value(cache_key)
    elif doc.doctype == 'Activities':
        cache_key = f'home_activities_data:{frappe.db.get_value("DocType", "Activities", "modified")}'
        frappe.cache().delete_value(cache_key)

def get_context(context):
    partners = get_cached_partners()
    casestudies = get_cached_casestudies()
    activities = get_cached_activities()
    tools = get_tools()
    
    context.update({
        'partners': partners,
        'casestudies': casestudies,
        'cards': activities,
        'tools': tools, 
    })
    return context

def get_tools():
    return [
        {"logo": f"/assets/oasis/images/tool{i}.png"} 
        for i in range(1, 17)
    ]

def get_cached_activities():
    cache_key = f'home_activities_data:{frappe.db.get_value("DocType", "Activities", "modified")}'
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        return cached_data

    activities = frappe.db.get_list('Activities',
        filters={},  
        fields=['background_color', 'illustration', 'content_summary', 'cta_button_1_label', 'cta_button_2_label', 'cta_button_1_link', 'cta_button_2_link'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    frappe.cache().set_value(cache_key, activities, expires_in_sec=3600)
    return activities

def get_cached_partners():
    cache_key = f'home_partners_data:{frappe.db.get_value("DocType", "Partners", "modified")}'
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        return cached_data

    partners = frappe.db.get_list('Partners', 
        filters={}, 
        fields=['partner_name', 'key_partner', 'logo', 'icon', 'url'],
        order_by='creation asc',
        limit_page_length=50
    )
    
    frappe.cache().set_value(cache_key, partners, expires_in_sec=3600)
    return partners

def get_cached_casestudies():
    cache_key = (
        f'home_cases_data:'
        f'{frappe.db.get_value("DocType", "Case Studies", "modified")}:'
        f'{frappe.db.get_value("DocType", "Case Study Tools", "modified")}'
    )
    cached_data = frappe.cache().get_value(cache_key)
    
    if cached_data:
        return cached_data
        
    casestudies = frappe.db.sql("""
        SELECT 
            cs.name, cs.title, cs.challenge, cs.solution, cs.subtitle,
            cs.category_tag, p.logo as solution_partner
        FROM `tabCase Studies` cs
        LEFT JOIN `tabpartners` p ON p.name = cs.solution_partner
        ORDER BY cs.creation desc
        LIMIT 4
    """, as_dict=True)

    case_names = [c.name for c in casestudies]
    tools = frappe.db.sql("""
        SELECT tu.parent, cst.name, cst.logo, cst.url
        FROM `tabTools Used` tu
        LEFT JOIN `tabCase Study Tools` cst ON cst.name = tu.tools_used
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
        'subtitle': cs.subtitle,
        'challenge': cs.challenge,
        'solution': cs.solution,
        'category_tag': cs.category_tag,
        'solution_partner': cs.solution_partner,
        'tools_used': tools_by_case.get(cs.name, []),
    } for cs in casestudies]
    
    frappe.cache().set_value(cache_key, casestudies, expires_in_sec=3600)
    return casestudies
