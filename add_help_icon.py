import glob
import os

with open('help_fragment.html', 'r', encoding='utf-8') as f:
    help_html = f.read()

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    if file_path.endswith('index.html') or file_path.endswith('help_center.html') or file_path.endswith('contractor_profile.html'):
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="notification-wrapper">' in content and 'help-btn-nav' not in content:
        content = content.replace('<div class="notification-wrapper">', help_html + '\n            <div class="notification-wrapper">')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Added help icon to dashboard templates.')
