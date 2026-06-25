import glob
import os
import re

# Tender images
tender_images = [
    'https://images.unsplash.com/photo-1504307651254-35680f3366d4?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&q=80&w=600'
]

# Contractor images
contractor_images = [
    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?auto=format&fit=crop&q=80&w=600',
    'https://images.unsplash.com/photo-1506277886164-e25aa3f4ef7f?auto=format&fit=crop&q=80&w=600'
]

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Tender placeholders
    for i, img in enumerate(tender_images):
        cls = f'bg-img-{i+1}'
        content = content.replace(f'<div class=\"img-placeholder {cls}\"></div>', 
                                f'<div class=\"img-placeholder\"><img src=\"{img}\" alt=\"Tender\"></div>')
    
    # Replace Contractor placeholders
    for i, img in enumerate(contractor_images):
        cls = f'bg-grad-{i+1}'
        content = content.replace(f'<div class=\"card-image {cls}\">', 
                                f'<div class=\"card-image\"><img src=\"{img}\" alt=\"Contractor\" style=\"width:100%; height:100%; object-fit:cover;\">')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Replaced CSS placeholders with <img> tags.')
