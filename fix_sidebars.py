import os

def fix_dashboard():
    path = 'templates/procurement/dashboard.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove accidental admin links if present
    content = content.replace('<span>Reports</span>', '<span>Documents</span>') # Just to be safe, revert changes
    
    # Redo the clean sidebar for contractor
    sidebar_start = '<aside class=\"dash-sidebar\">'
    sidebar_end = '</aside>'
    new_sidebar = '''<aside class=\"dash-sidebar\">
            <nav class=\"dash-nav\">
                <a href=\"{% url 'dashboard' %}\" class=\"dash-nav-item active\">
                    <i class=\"ph ph-house\"></i>
                    <span>Dashboard</span>
                </a>
                <a href=\"{% url 'tenders' %}\" class=\"dash-nav-item\">
                    <i class=\"ph ph-file-text\"></i>
                    <span>Tenders</span>
                </a>
                <a href=\"{% url 'my_bids' %}\" class=\"dash-nav-item\">
                    <i class=\"ph ph-briefcase\"></i>
                    <span>My Bids</span>
                </a>
                <a href=\"#\" class=\"dash-nav-item\">
                    <i class=\"ph ph-folder\"></i>
                    <span>Documents</span>
                </a>
                <a href=\"{% url 'contractor_profile' %}\" class=\"dash-nav-item\">
                    <i class=\"ph ph-user\"></i>
                    <span>Profile</span>
                </a>
                <a href=\"#\" class=\"dash-nav-item sidebar-notif-trigger\">
                    <i class=\"ph ph-bell\"></i>
                    <span>Notifications</span>
                    <span style=\"background: #2E7D32; color: white; border-radius: 50%; width: 18px; height: 18px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; margin-left: auto;\">3</span>
                </a>
                <a href=\"{% url 'settings' %}\" class=\"dash-nav-item\">
                    <i class=\"ph ph-gear\"></i>
                    <span>Settings</span>
                </a>
            </nav>
            
            <a href=\"{% url 'signin' %}\" class=\"dash-nav-item logout\">
                <i class=\"ph ph-sign-out\"></i>
                <span>Logout</span>
            </a>
        </aside>'''
    
    # Very surgical replacement
    start_idx = content.find(sidebar_start)
    end_idx = content.find(sidebar_end) + len(sidebar_end)
    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + new_sidebar + content[end_idx:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_admin_dashboard():
    path = 'templates/procurement/admin_dashboard.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add Notif to Admin Sidebar
    old_line = '<a href=\"{% url \'settings\' %}\" class=\"dash-nav-item admin-nav-item\">'
    new_line = '''<a href=\"#\" class=\"dash-nav-item admin-nav-item sidebar-notif-trigger\">
                    <i class=\"ph ph-bell\"></i>
                    <span>Notifications</span>
                    <span style=\"background: #AACC00; color: #000; border-radius: 50%; width: 18px; height: 18px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; margin-left: auto; font-weight: 800;\">3</span>
                </a>
                <a href=\"{% url \'settings\' %}\" class=\"dash-nav-item admin-nav-item\">'''
    content = content.replace(old_line, new_line)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_dashboard()
fix_admin_dashboard()
print('Fixed sidebars for Dashboard and Admin Dashboard.')
