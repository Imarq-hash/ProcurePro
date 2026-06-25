import os
import glob

replacements = {
    '$ ': 'GH? ',
    '$': 'GH?',
    'Los Angeles, CA': 'Accra, Ghana',
    'San Francisco, CA': 'Kumasi, Ghana',
    'San Diego, CA': 'Takoradi, Ghana',
    'California': 'Ghana',
    'New York': 'Accra',
    'London': 'Kumasi',
    'Paris': 'Tamale'
}

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated currency and locations to Ghana.')
