document.addEventListener('DOMContentLoaded', function() {

    // --- NOTIFICATION SYSTEM (CRITICAL FIX) ---
    const notifBtn = document.getElementById('notificationBtn');
    const notifDropdown = document.getElementById('notificationDropdown');
    
    if (notifBtn && notifDropdown) {
        // Notification elements are present and ready.
        
        notifBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            notifDropdown.classList.toggle('active');
            // Toggled notification dropdown visibility.
        });

        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
                notifDropdown.classList.remove('active');
            }
        });
    } else {
        // Notification DOM elements not present on this page.
    }

    // --- REST OF THE SYSTEM ---
    
    // Notification Details Modal
    const notifItems = document.querySelectorAll('.notification-item');
    const notifDetailModal = document.getElementById('notifDetailModal');
    const notifModalTitle = document.getElementById('notifModalTitle');
    const notifModalMsg = document.getElementById('notifModalMsg');
    const notifModalClose = document.getElementById('notifModalClose');

    if (notifItems && notifDetailModal) {
        notifItems.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                const title = this.querySelector('.notification-item-title').textContent;
                const msg = this.querySelector('.notification-item-msg').textContent;
                const notifId = this.dataset.id;
                
                // Mark as read in backend
                if (notifId) {
                    fetch(`/notifications/mark-read/${notifId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }).then(response => {
                        if (response.ok) {
                            this.classList.remove('unread');
                            // Update badge if necessary
                            const badge = document.querySelector('.notification-badge');
                            if (badge) {
                                let count = parseInt(badge.textContent);
                                if (count > 1) {
                                    badge.textContent = count - 1;
                                } else {
                                    badge.style.display = 'none';
                                }
                            }
                        }
                    });
                }

                if (notifModalTitle) notifModalTitle.textContent = title;
                if (notifModalMsg) notifModalMsg.textContent = msg;

                // Handle notification link button dynamically
                let actionBtn = notifDetailModal.querySelector('.modal-action-btn');
                if (!actionBtn) {
                    const footerDiv = notifDetailModal.querySelector('div[style*="text-align: right"]') || notifDetailModal.querySelector('div[style*="text-align:right"]');
                    if (footerDiv) {
                        actionBtn = document.createElement('a');
                        actionBtn.className = 'btn btn-primary modal-action-btn';
                        actionBtn.style.padding = '10px 24px';
                        actionBtn.style.textDecoration = 'none';
                        actionBtn.style.marginLeft = '10px';
                        actionBtn.style.display = 'inline-block';
                        footerDiv.appendChild(actionBtn);
                    }
                }
                
                const link = this.dataset.link;
                if (link && actionBtn && isSafeNotificationLink(link)) {
                    actionBtn.href = link;
                    actionBtn.target = '_self';
                    actionBtn.textContent = 'Take Action';
                    actionBtn.style.display = 'inline-block';
                    
                    const otherLinks = notifDetailModal.querySelectorAll('a:not(.modal-action-btn)');
                    otherLinks.forEach(lnk => lnk.style.display = 'none');
                } else if (actionBtn) {
                    actionBtn.style.display = 'none';
                    const otherLinks = notifDetailModal.querySelectorAll('a:not(.modal-action-btn)');
                    otherLinks.forEach(lnk => lnk.style.display = 'inline-block');
                }
                
                notifDetailModal.style.display = 'flex';
                if (notifDropdown) notifDropdown.classList.remove('active');
            });
        });
    }

    // Helper to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    if (notifModalClose) {
        notifModalClose.addEventListener('click', () => {
            notifDetailModal.style.display = 'none';
        });
    }

    function isSafeNotificationLink(link) {
        if (!link) return false;
        const trimmed = link.trim();
        if (/^javascript:/i.test(trimmed)) return false;
        return trimmed.startsWith('/') || trimmed.startsWith('#');
    }

    // Sidebar Notification Trigger
    const sidebarNotifTriggers = document.querySelectorAll('.sidebar-notif-trigger');
    sidebarNotifTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            if (notifDropdown) notifDropdown.classList.toggle('active');
        });
    });

    // Password visibility toggle
    const togglePassword = document.querySelectorAll('.toggle-password');
    togglePassword.forEach(icon => {
        icon.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.replace('ph-eye-slash', 'ph-eye');
            } else {
                input.type = 'password';
                this.classList.replace('ph-eye', 'ph-eye-slash');
            }
        });
    });

    // Mark all as read
    const markReadBtn = document.querySelector('.mark-read');
    if (markReadBtn) {
        markReadBtn.addEventListener('click', function() {
            document.querySelectorAll('.notification-item.unread').forEach(item => {
                item.classList.remove('unread');
            });
            const badge = document.querySelector('.notification-badge');
            if (badge) badge.style.display = 'none';
        });
    }
});
