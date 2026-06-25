import glob
import os
import re

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix Admin Portal link
    admin_pattern = re.compile(r'(>Admin Portal</a>)')
    if admin_pattern.search(content):
        # Find the <a> tag right before it
        content = re.sub(r'<a\s+href=[\"\']#[\"\']\s+style=[\"\'][^\"\']*?[\"\']>Admin Portal</a>', 
                        r'<a href="{% url \'admin_login\' %}" style="color: white; text-decoration: none;">Admin Portal</a>', 
                        content)

    # 2. Fix specific form actions
    if 'admin_post_tender.html' in file_path:
        content = content.replace('<form action=\"#\">', '<form action=\"{% url \'admin_manage_tenders\' %}\">')
    
    if 'submit_bid.html' in file_path:
        content = content.replace('<form id=\"bidForm\" action=\"#\" method=\"POST\">', '<form id=\"bidForm\" action=\"{% url \'my_bids\' %}\" method=\"GET\">')

    # 3. Clean up any remaining backslashes in URL tags (just in case)
    content = content.replace(r"\'", "'")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Final sweep completed: Fixed form actions, admin links, and cleaned up syntax.')
