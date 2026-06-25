import os

template_file = 'templates/procurement/tenders.html'
with open(template_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace titles and images
content = content.replace('Hospital Electrical Upgrade', 'Arena Electrical Upgrade')
content = content.replace('bg-img-1', 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&q=80&w=600')
content = content.replace('bg-img-2', 'https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=600')
content = content.replace('bg-img-3', 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=600')

with open(template_file, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated tenders.html with new images and titles.')
