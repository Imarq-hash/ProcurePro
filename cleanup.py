import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix GH? issue (encoding artifact)
    content = content.replace('GH?', 'GH?')
    content = content.replace('GH? ', 'GH? ')
    
    # Fix Arena naming
    content = content.replace('City Hospital Electrical Upgrade', 'Arena Electrical Upgrade')
    content = content.replace('Hospital Electrical Upgrade', 'Arena Electrical Upgrade')
    
    # Fix malformed footer from add_modal script
    content = content.replace('\\n</body>', '</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Cleaned up encoding and naming artifacts.')
