import os
import glob

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix Sidebar Profile link (remove nested links and fix href)
    content = content.replace('<a href=\"#\" class=\"dash-nav-item\">\n                    <i class=\"ph ph-user\"></i>\n                    <span><a href=\"/contractor-profile/\" style=\"color: inherit; text-decoration: none;\">Profile</a></span>\n                </a>', '<a href=\"/contractor-profile/\" class=\"dash-nav-item\">\n                    <i class=\"ph ph-user\"></i>\n                    <span>Profile</span>\n                </a>')
    
    content = content.replace('<a href=\"#\" class=\"dash-nav-item\">\n                    <i class=\"ph ph-user\"></i>\n                    <span>Profile</span>\n                </a>', '<a href=\"/contractor-profile/\" class=\"dash-nav-item\">\n                    <i class=\"ph ph-user\"></i>\n                    <span>Profile</span>\n                </a>')

    # Fix other common broken links
    content = content.replace('href=\"#\" class=\"view-profile-link\"', 'href=\"/contractor-profile/\" class=\"view-profile-link\"')
    
    # Final Currency fix
    content = content.replace('GH?', 'GH?')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Cleaned up navigation links and fixed currency again.')
