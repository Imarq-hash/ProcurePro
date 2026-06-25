import os, glob

for filepath in glob.glob('templates/procurement/*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'dash-nav-item logout' in content:
        content = content.replace("{% url 'signin' %}", "{% url 'logout' %}")
        content = content.replace("{% url 'admin_login' %}", "{% url 'logout' %}")
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated logout links in {filepath}")
