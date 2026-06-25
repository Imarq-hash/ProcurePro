import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Correct hardcoded links to use Django URL tags
    content = content.replace('href=\"/contractor-profile/\"', 'href=\"{% url \"contractor_profile\" %}\"')
    content = content.replace('href=\"dashboard.html\"', 'href=\"{% url \"dashboard\" %}\"')
    content = content.replace('href=\"tenders.html\"', 'href=\"{% url \"tenders\" %}\"')
    content = content.replace('href=\"signin.html\"', 'href=\"{% url \"signin\" %}\"')
    content = content.replace('href=\"signup.html\"', 'href=\"{% url \"signup\" %}\"')
    
    # 2. Fix "View All" buttons that point to #
    content = content.replace('href=\"#\" class=\"btn btn-dark btn-sm\">View All', 'href=\"{% url \"tenders\" %}\" class=\"btn btn-dark btn-sm\">View All')
    
    # 3. Standardize Currency
    content = content.replace('GH?', 'GH?')
    content = content.replace('GH? ', 'GH? ')
    
    # 4. Standardize Logo links
    content = content.replace('<a href=\"#\" class=\"logo\">', '<a href=\"{% url \"home\" %}\" class=\"logo\">')
    content = content.replace('<a href=\"#\" class=\"logo dash-logo\">', '<a href=\"{% url \"home\" %}\" class=\"logo dash-logo\">')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Critically analyzed and synchronized all template links and currency.')
