import re
import glob
import os

with open('notif_fragment.html', 'r', encoding='utf-8') as f:
    notif_html = f.read()

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

pattern = re.compile(r'<button class=\"notif-btn.*?\">.*?</button>', re.DOTALL)

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if pattern.search(content):
        content = pattern.sub(notif_html, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Injected new notification system into all templates.')
