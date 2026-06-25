import re
import glob
import os

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to replace typical hrefs
    content = re.sub(r'href=[\"\']index\.html[\"\']', 'href=\"{% url \'home\' %}\"', content)
    content = re.sub(r'href=[\"\']signin\.html[\"\']', 'href=\"{% url \'signin\' %}\"', content)
    content = re.sub(r'href=[\"\']signup\.html[\"\']', 'href=\"{% url \'signup\' %}\"', content)
    content = re.sub(r'href=[\"\']dashboard\.html[\"\']', 'href=\"{% url \'dashboard\' %}\"', content)
    content = re.sub(r'href=[\"\']tenders\.html[\"\']', 'href=\"{% url \'tenders\' %}\"', content)
    content = re.sub(r'href=[\"\']project_details\.html[\"\']', 'href=\"{% url \'project_details\' %}\"', content)
    content = re.sub(r'href=[\"\']submit_bid\.html[\"\']', 'href=\"{% url \'submit_bid\' %}\"', content)
    content = re.sub(r'href=[\"\']contractors\.html[\"\']', 'href=\"{% url \'contractors\' %}\"', content)
    content = re.sub(r'href=[\"\']my_bids\.html[\"\']', 'href=\"{% url \'my_bids\' %}\"', content)
    content = re.sub(r'href=[\"\']settings\.html[\"\']', 'href=\"{% url \'settings\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_login\.html[\"\']', 'href=\"{% url \'admin_login\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_dashboard\.html[\"\']', 'href=\"{% url \'admin_dashboard\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_post_tender\.html[\"\']', 'href=\"{% url \'admin_post_tender\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_manage_tenders\.html[\"\']', 'href=\"{% url \'admin_manage_tenders\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_contractors\.html[\"\']', 'href=\"{% url \'admin_contractors\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_review_bids\.html[\"\']', 'href=\"{% url \'admin_review_bids\' %}\"', content)
    content = re.sub(r'href=[\"\']admin_reports\.html[\"\']', 'href=\"{% url \'admin_reports\' %}\"', content)
    
    # also replace action="..." for forms
    content = re.sub(r'action=[\"\']index\.html[\"\']', 'action=\"{% url \'home\' %}\"', content)
    content = re.sub(r'action=[\"\']signin\.html[\"\']', 'action=\"{% url \'signin\' %}\"', content)
    content = re.sub(r'action=[\"\']dashboard\.html[\"\']', 'action=\"{% url \'dashboard\' %}\"', content)
    content = re.sub(r'action=[\"\']admin_dashboard\.html[\"\']', 'action=\"{% url \'admin_dashboard\' %}\"', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print('Updated internal links to Django tags.')
