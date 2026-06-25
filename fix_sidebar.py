import re
import glob
import os

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

replacements = [
    (r'<span>Dashboard</span>\s*</a>', r'<span>Dashboard</span>\n                </a>', 'Dashboard'),
    (r'<span>Browse Tenders</span>\s*</a>', r'<span>Browse Tenders</span>\n                </a>', 'Browse Tenders'),
    (r'<span>My Bids</span>\s*</a>', r'<span>My Bids</span>\n                </a>', 'My Bids'),
    (r'<span>Settings</span>\s*</a>', r'<span>Settings</span>\n                </a>', 'Settings'),
    (r'<span>Contractors</span>\s*</a>', r'<span>Contractors</span>\n                </a>', 'Contractors'),
]

# Mapping text to URL names
url_map = {
    'Dashboard': 'dashboard',
    'Browse Tenders': 'tenders',
    'My Bids': 'my_bids',
    'Settings': 'settings',
    'Contractors': 'contractors',
    'Post Tender': 'admin_post_tender',
    'Manage Tenders': 'admin_manage_tenders',
    'Review Bids': 'admin_review_bids',
    'Reports': 'admin_reports'
}

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target <a> tags that contain the specific <span> text
    for text, url_name in url_map.items():
        # Match <a href="..." ...> ... <span>Text</span> ... </a>
        pattern = re.compile(r'(<a\s+[^>]*?href=)[\"\']#[\"\']([^>]*?>\s*<i[^>]*?></i>\s*<span>' + re.escape(text) + r'</span>\s*</a>)', re.DOTALL)
        content = pattern.sub(r'\1"{% url \'' + url_name + r'\' %}"\2', content)

    # Special case for "Dashboard" in admin templates where the URL might be admin_dashboard
    if 'admin_' in file_path:
        content = content.replace('{% url \'dashboard\' %}', '{% url \'admin_dashboard\' %}')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated all sidebar navigation links based on text labels.')
