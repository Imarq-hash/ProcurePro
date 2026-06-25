import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=600', '/static/assets/school_block.png')
    content = content.replace('https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=600', '/static/assets/road_repair.png')
    content = content.replace('https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=600', '/static/assets/hospital_electrical.png')
    content = content.replace('GH?', 'GH?')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated all templates with local assets and fixed currency.')
