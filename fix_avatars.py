import os
import glob

search_str = "{% if request.user.is_authenticated and request.user.is_contractor %}{% url 'contractor_profile' request.user.contractor_profile.pk %}{% else %}#{% endif %}"
replace_str = "{% url 'settings' %}"

for file in glob.glob('c:/Users/Irene/Desktop/PROJECT/Codes sys/templates/procurement/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if search_str in content:
        content = content.replace(search_str, replace_str)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {file}')
