import os

path = 'static/js/script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the existing notification toggle with a more robust version
old_code = '''    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notifDropdown.classList.toggle('active');
        });
        document.addEventListener('click', (e) => {
            if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
                notifDropdown.classList.remove('active');
            }
        });
    }'''

new_code = '''    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    if (notifBtn && notifDropdown) {
        notifBtn.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            notifDropdown.classList.toggle('active');
            console.log('Notification toggled');
        };
        document.addEventListener('click', function(e) {
            if (notifDropdown.classList.contains('active')) {
                if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
                    notifDropdown.classList.remove('active');
                }
            }
        });
    }'''

content = content.replace(old_code, new_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated script.js with robust notification logic.')
