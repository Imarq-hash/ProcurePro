import os

files = ['templates/procurement/dashboard.html', 'templates/procurement/admin_dashboard.html']
for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Improve Modal Design
    old_modal = '<div id=\"notifDetailModal\" class=\"modal-notif\" style=\"display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; align-items: center; justify-content: center;\">'
    new_modal = '<div id=\"notifDetailModal\" class=\"modal-notif\" style=\"display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; backdrop-filter: blur(5px); align-items: center; justify-content: center;\">'
    content = content.replace(old_modal, new_modal)

    # Add Action Button to Modal
    old_btn_row = '<div style=\"margin-top: 25px; text-align: right;\">\n                <button onclick=\"document.getElementById(\"notifDetailModal\").style.display=\"none\"\" class=\"btn btn-primary\" style=\"padding: 8px 24px;\">Close</button>\n            </div>'
    # Use a simpler match
    content = content.replace('padding: 8px 24px;\">Close</button>', 'padding: 8px 24px; margin-right: 10px; background: #eee; color: #333; border: none;\">Dismiss</button><a href=\"/tenders/\" class=\"btn btn-primary\" style=\"padding: 10px 24px; text-decoration: none;\">View Tender</a>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Improved notification modals.')
