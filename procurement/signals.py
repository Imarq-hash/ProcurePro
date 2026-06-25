from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import Tender, Bid, Notification, User, ContractorProfile
from .admin_security import AdminSecurityValidator

@receiver(post_save, sender=Tender)
def tender_posted_notification(sender, instance, created, **kwargs):
    """
    Notify all contractors when a new tender is posted (status set to OPEN).
    """
    if instance.status == Tender.Status.OPEN:
        # Check if it was just created as OPEN or updated to OPEN
        # For simplicity, we'll notify if it's OPEN. 
        # In a real app, we might want to track if a notification was already sent.
        
        # Get all contractors
        contractors = User.objects.filter(role=User.Role.CONTRACTOR)
        
        for contractor in contractors:
            # Avoid duplicate notifications for the same tender if it's just an update
            # (Simplified: just create for now, or check for existing)
            Notification.objects.get_or_create(
                user=contractor,
                message=f"New Tender Posted: {instance.title}. Category: {instance.get_category_display()}.",
                # We could add a link or entity reference if we expand the model
            )

@receiver(post_save, sender=Bid)
def bid_status_notification(sender, instance, created, **kwargs):
    """
    Notify contractor when bid status changes (Awarded/Rejected).
    Notify admin when a new bid is submitted.
    """
    if created:
        # Notify Admin about new bid
        admins = User.objects.filter(role=User.Role.ADMIN)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"New Bid submitted for {instance.tender.title} by {instance.contractor.company_name}."
            )
    else:
        # Status update notifications for contractor
        if instance.status == Bid.Status.ACCEPTED:
            Notification.objects.create(
                user=instance.contractor.user,
                message=f"Congratulations! Your bid for '{instance.tender.title}' has been ACCEPTED. Tender awarded."
            )
        elif instance.status == Bid.Status.REJECTED:
            Notification.objects.create(
                user=instance.contractor.user,
                message=f"Update: Your bid for '{instance.tender.title}' was not selected."
            )
        elif instance.status == Bid.Status.UNDER_REVIEW:
            Notification.objects.create(
                user=instance.contractor.user,
                message=f"Your bid for '{instance.tender.title}' is now under review."
            )


# Admin Security Signal Handlers
@receiver(pre_delete, sender=User)
def prevent_admin_deletion(sender, instance, **kwargs):
    """Prevent deletion of the official admin account."""
    AdminSecurityValidator.prevent_admin_deletion(sender, instance, **kwargs)


@receiver(pre_save, sender=User)
def prevent_admin_modification(sender, instance, **kwargs):
    """Prevent unauthorized modification of critical admin fields."""
    AdminSecurityValidator.prevent_admin_modification(sender, instance, **kwargs)
