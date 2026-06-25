import os

file_path = 'templates/procurement/contractor_profile.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Location
content = content.replace('Berlin, Germany', 'Accra, Ghana')
content = content.replace('Europe and Africa', 'the West African region')

# Fix Currency
content = content.replace('GH?', 'GH?')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated contractor_profile.html.')
