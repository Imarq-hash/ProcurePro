import os

file_path = 'templates/procurement/tenders.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace placeholders with local assets
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #202040 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/school_block.png\" alt=\"School Block\"></div>')
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #204020 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/road_repair.png\" alt=\"Road Repair\"></div>')
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #402020 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/hospital_electrical.png\" alt=\"Electrical Upgrade\"></div>')
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #204040 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/building.jpg\" alt=\"Construction Work\"></div>')
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #404020 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/road.jpg\" alt=\"Road Work\"></div>')
content = content.replace('<div class=\"img-placeholder\" style=\"background: linear-gradient(135deg, #111 0%, #402030 100%);\"></div>', '<div class=\"img-placeholder\"><img src=\"/static/assets/hardhat_hero.png\" alt=\"Contractor Site\"></div>')

# Fix Budget symbols
content = content.replace('Budget: ', 'Budget: GH? ')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated tenders.html images.')
