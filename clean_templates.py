import glob
import os

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the escaped quotes with single quotes
    content = content.replace(r"\'", "'")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Cleaned up escaped quotes in all templates.')
