import frappe
def get_context(context):
    context.whyjoin = [
        {
            "title": "Access to Expertise", "desc": "Engage with leading minds in FOSS and social innovation."
        },
        {
           "title": "Networking Opportunities", "desc": "Connect with like-minded individuals and organizations working towards similar goals."
        },
        {
            "title": "New Opportunities", "desc": "Explore collaborations, projects, and initiatives that align technology with social good."
        },
        {
            "title": "Knowledge & Resources", "desc": "Leverage curated educational materials, playbooks, and case studies to amplify your impact."
        },
        {
            "title": "Community Visibility", "desc": "Showcase your work and contributions to a global audience committed to open-source principles."
        }
    ]
    return context