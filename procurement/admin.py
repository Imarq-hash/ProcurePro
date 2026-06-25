from django.contrib import admin
from .models import User, ContractorProfile, AdminProfile, Tender, Bid, Notification, TenderRequest

admin.site.register(User)
admin.site.register(ContractorProfile)
admin.site.register(AdminProfile)
admin.site.register(Tender)
admin.site.register(Bid)
admin.site.register(Notification)
admin.site.register(TenderRequest)

