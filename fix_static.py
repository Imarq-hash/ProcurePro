import os
import glob
import re

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add {% load static %} if not present
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content
        
    # Replace css/styles.css
    content = re.sub(r'href=[\"\']css/styles.css[\"\']', 'href=\"{% static \'css/styles.css\' %}\"', content)
    
    # Replace js/script.js
    content = re.sub(r'src=[\"\']js/script.js[\"\']', 'src=\"{% static \'js/script.js\' %}\"', content)
    
    # Replace href="filename.html" with Django URL tags, this is trickier. Let's do it manually or skip for now.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print(f'Processed {len(html_files)} files.')
