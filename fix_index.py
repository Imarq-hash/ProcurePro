import os

template_file = 'templates/procurement/index.html'
with open(template_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix images to use local assets for better reliability
content = content.replace('https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=600', '/static/assets/school_block.png')
content = content.replace('https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=600', '/static/assets/road_repair.png')
content = content.replace('https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=600', '/static/assets/hospital_electrical.png')

# Fix encoding issue
content = content.replace('GH?', 'GH?')

with open(template_file, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html with local assets and fixed currency.')
