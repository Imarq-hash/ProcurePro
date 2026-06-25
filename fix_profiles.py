import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix Profile link in sidebar
    content = content.replace('<span>Profile</span>', '<span><a href=\"/contractor-profile/\" style=\"color: inherit; text-decoration: none;\">Profile</a></span>')
    content = content.replace('<span><i class=\"ph ph-user\"></i> Profile</span>', '<span><i class=\"ph ph-user\"></i> <a href=\"/contractor-profile/\" style=\"color: inherit; text-decoration: none;\">Profile</a></span>')
    
    # Ensure user avatar is clickable
    content = content.replace('<div class=\"user-avatar\"', '<a href=\"/contractor-profile/\" class=\"user-avatar\" style=\"text-decoration: none; display: flex; align-items: center; justify-content: center;\"')
    content = content.replace('</div>\n        </div>\n    </nav>', '</a>\n        </div>\n    </nav>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated profile links and avatar clickability.')
