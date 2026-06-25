import os

file_path = 'templates/procurement/contractors.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace external images with local assets
# Card 1: Apex Structural
content = content.replace('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=600', '/static/assets/contractor1.jpg')
content = content.replace('Berlin, Germany', 'Accra, Ghana')

# Card 2: Stivo & Co
content = content.replace('https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=600', '/static/assets/contractor2.jpg')

# Card 3: K Quansah
content = content.replace('https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=600', '/static/assets/contractor3.jpg')

# Card 4: Modern Infra
content = content.replace('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=600', '/static/assets/conntractor4.png')

# Card 5: Power Dynamics
content = content.replace('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=600', '/static/assets/contractr5.png')

# Card 6: BuildSafe
content = content.replace('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=600', '/static/assets/contractor6.png')

# Update Header Image
content = content.replace('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=1600', '/static/assets/contractor1.jpg')

# Fix Localization
content = content.replace('global enterprise partners', 'leading Ghanaian enterprise partners')
content = content.replace('<option value=\"berlin\">Berlin, Germany</option>', '<option value=\"tema\">Tema, Ghana</option>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated contractors.html images and localization.')
