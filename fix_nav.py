import re
import glob
import os

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

replacements = {
    r'href=[\"\']dashboard\.html[\"\']': 'href=\"{% url \'dashboard\' %}\"',
    r'href=[\"\']tenders\.html[\"\']': 'href=\"{% url \'tenders\' %}\"',
    r'href=[\"\']contractors\.html[\"\']': 'href=\"{% url \'contractors\' %}\"',
    r'href=[\"\']my_bids\.html[\"\']': 'href=\"{% url \'my_bids\' %}\"',
    r'href=[\"\']settings\.html[\"\']': 'href=\"{% url \'settings\' %}\"',
    r'href=[\"\']index\.html[\"\']': 'href=\"{% url \'home\' %}\"',
    r'href=[\"\']admin_dashboard\.html[\"\']': 'href=\"{% url \'admin_dashboard\' %}\"',
    r'href=[\"\']admin_post_tender\.html[\"\']': 'href=\"{% url \'admin_post_tender\' %}\"',
    r'href=[\"\']admin_manage_tenders\.html[\"\']': 'href=\"{% url \'admin_manage_tenders\' %}\"',
    r'href=[\"\']admin_contractors\.html[\"\']': 'href=\"{% url \'admin_contractors\' %}\"',
    r'href=[\"\']admin_review_bids\.html[\"\']': 'href=\"{% url \'admin_review_bids\' %}\"',
    r'href=[\"\']admin_reports\.html[\"\']': 'href=\"{% url \'admin_reports\' %}\"',
}

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated all internal navigation links.')
