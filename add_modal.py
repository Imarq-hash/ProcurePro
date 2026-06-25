import glob
import os

modal_html = '''
    <!-- Notification Detail Modal -->
    <div id="notifDetailModal" class="modal-notif" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; align-items: center; justify-content: center;">
        <div class="modal-notif-content" style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; position: relative;">
            <span id="notifModalClose" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer;">&times;</span>
            <h2 id="notifModalTitle" style="color: #000; margin-bottom: 15px;"></h2>
            <p id="notifModalMsg" style="color: #666; line-height: 1.6;"></p>
            <div style="margin-top: 25px; text-align: right;">
                <button onclick="document.getElementById('notifDetailModal').style.display='none'" class="btn btn-primary" style="padding: 8px 24px;">Close</button>
            </div>
        </div>
    </div>
'''

template_dir = 'templates/procurement'
html_files = glob.glob(os.path.join(template_dir, '*.html'))

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="notification-wrapper">' in content and 'notifDetailModal' not in content:
        if '</body>' in content:
            content = content.replace('</body>', modal_html + '\\n</body>')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

print('Added notification modal to dashboards.')
