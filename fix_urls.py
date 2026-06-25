import os
import glob

templates_dir = r'c:\Users\Irene\Desktop\PROJECT\Codes sys\templates\procurement'

for filepath in glob.glob(os.path.join(templates_dir, '*.html')):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Admin templates (e.g., admin_dashboard, admin_contractors, etc.)
    if 'admin_' in os.path.basename(filepath):
        content = content.replace('{% url "contractor_profile" %}', "{% url 'settings' %}")
        content = content.replace("{% url 'contractor_profile' %}", "{% url 'settings' %}")
        # Except if it's admin_contractors.html where they might iterate over contractors
        if os.path.basename(filepath) == 'admin_contractors.html':
            # Actually, in admin_contractors.html there are action-icons linking to the profile.
            # We should probably pass the contractor.pk. Let's fix that specifically.
            content = content.replace("{% url 'settings' %}\" class=\"action-icon\"", "{% url 'contractor_profile' contractor.pk %}\" class=\"action-icon\"")

    # Contractor templates
    elif os.path.basename(filepath) in ['dashboard.html', 'my_bids.html', 'settings.html', 'project_details.html']:
        replacement = "{% if request.user.is_authenticated and request.user.is_contractor %}{% url 'contractor_profile' request.user.contractor_profile.pk %}{% else %}#{% endif %}"
        content = content.replace('{% url "contractor_profile" %}', replacement)
        content = content.replace("{% url 'contractor_profile' %}", replacement)
    
    # Public index.html
    elif os.path.basename(filepath) == 'index.html':
        content = content.replace("{% url 'contractor_profile' %}", "{% url 'contractors' %}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done fixing templates!')
