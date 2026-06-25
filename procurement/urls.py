from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Notifications
    path('notifications/mark-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_read'),
    

    # Public & Auth
    path('', views.home_view, name='home'),
    path('request-tender/', views.request_tender_view, name='request_tender'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('help-center/', TemplateView.as_view(template_name='procurement/help_center.html'), name='help_center'),
    path('contractors/<int:pk>/profile/', views.contractor_profile_view, name='contractor_profile'),
    
    # Contractor Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tenders/', views.tenders_list_view, name='tenders'),
    path('tenders/<int:pk>/details/', views.tender_details_view, name='project_details'),
    path('tenders/<int:pk>/submit/', views.submit_bid_view, name='submit_bid'),
    path('contractors/', views.contractors_list_view, name='contractors'),
    path('my-bids/', views.my_bids_view, name='my_bids'),
    path('settings/', views.settings_view, name='settings'),
    
    # Admin Portal
    path('admin-login/', TemplateView.as_view(template_name='procurement/admin_login.html'), name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-post-tender/', views.admin_post_tender_view, name='admin_post_tender'),
    path('admin-manage-tenders/', views.admin_manage_tenders_view, name='admin_manage_tenders'),
    path('admin-tender-requests/', views.admin_tender_requests_view, name='admin_tender_requests'),
    path('admin-tender-requests/<int:pk>/review/', views.admin_review_request_view, name='admin_review_request'),
    path('admin-tender-requests/<int:pk>/document/download/', views.download_tender_document, name='download_tender_document'),
    path('admin-contractors/', views.admin_contractors_view, name='admin_contractors'),
    path('admin-review-bids/', views.admin_review_bids_view, name='admin_review_bids'),
    path('admin-reports/', views.admin_reports_view, name='admin_reports'),
]
