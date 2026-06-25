import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Final Currency fix
    content = content.replace('GH?', 'GH?')
    content = content.replace('GH? ', 'GH? ')
    
    # Fix any potentially broken grid layouts
    content = content.replace('left-align', 'text-left') # Standardizing classes

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Final polish complete.')
