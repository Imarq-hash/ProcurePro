from django.core.cache import cache
from .models import Notification, Tender, TenderRequest
from django.utils import timezone
from datetime import timedelta

def notifications(request):
    if request.user.is_authenticated:
        cache_key = f'unread_notifications_count_{request.user.id}'
        unread_count = cache.get(cache_key)
        if unread_count is None:
            unread_count = request.user.notifications.filter(is_read=False).count()
            cache.set(cache_key, unread_count, 60)
        all_notifications = request.user.notifications.all().order_by('-created_at')[:10]
        
        pending_requests_count = 0
        if request.user.is_admin():
            pending_requests_count = TenderRequest.objects.filter(status='PENDING').count()
            
        return {
            'unread_notifications_count': unread_count,
            'recent_notifications': all_notifications,
            'pending_requests_count': pending_requests_count
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
        'pending_requests_count': 0
    }

