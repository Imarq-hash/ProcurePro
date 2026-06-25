"""
Admin Security Module
Ensures the official admin account cannot be accidentally modified or deleted.
Prevents unauthorized changes to critical admin credentials.
"""

from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
import logging
from .models import User

security_logger = logging.getLogger('procurepro.security')

# Official admin credentials (cannot be changed)
OFFICIAL_ADMIN_EMAIL = 'admin@procurepro.com'
OFFICIAL_ADMIN_PASSWORD = 'admin1234'


class AdminSecurityValidator:
    """Validates and protects the official admin account."""
    
    @staticmethod
    def validate_admin_user():
        """
        Verify the official admin user exists and has correct settings.
        Should be called during application startup.
        """
        try:
            admin = User.objects.get(email=OFFICIAL_ADMIN_EMAIL)
            
            # Verify settings
            checks = {
                'is_staff': admin.is_staff,
                'is_superuser': admin.is_superuser,
                'role': admin.role == 'ADMIN',
            }
            
            all_valid = all(checks.values())
            if not all_valid:
                error_msg = f"Admin user settings corrupted: {checks}"
                security_logger.error(error_msg)
                raise ValidationError(error_msg)
                
            security_logger.info(f"Admin security check passed at {timezone.now()}")
            return True
            
        except User.DoesNotExist:
            error_msg = f"Official admin user not found: {OFFICIAL_ADMIN_EMAIL}"
            security_logger.critical(error_msg)
            raise ValidationError(error_msg)
    
    @staticmethod
    def prevent_admin_deletion(sender, instance, **kwargs):
        """
        Signal handler to prevent deletion of the official admin account.
        Connect this to pre_delete signal for User model.
        """
        if instance.email == OFFICIAL_ADMIN_EMAIL:
            error_msg = f"Cannot delete official admin account: {OFFICIAL_ADMIN_EMAIL}"
            security_logger.warning(error_msg)
            raise PermissionDenied(error_msg)
    
    @staticmethod
    def prevent_admin_modification(sender, instance, **kwargs):
        """
        Signal handler to prevent unauthorized modification of admin account.
        Allows password updates only (triggered by explicit admin reset).
        Connect this to pre_save signal for User model.
        """
        if instance.email == OFFICIAL_ADMIN_EMAIL:
            try:
                existing = User.objects.get(email=OFFICIAL_ADMIN_EMAIL)
                
                # Allow password changes, but protect other critical fields
                protected_fields = ['email', 'role', 'is_staff', 'is_superuser']
                
                for field in protected_fields:
                    if getattr(existing, field) != getattr(instance, field):
                        error_msg = f"Cannot modify protected admin field: {field}"
                        security_logger.warning(f"{error_msg} - Attempted change from {getattr(existing, field)} to {getattr(instance, field)}")
                        raise PermissionDenied(error_msg)
                        
            except User.DoesNotExist:
                # Account doesn't exist yet, allow creation
                pass


def verify_admin_credentials(email, password):
    """
    Explicitly verify admin credentials match the official values.
    Returns True if credentials are valid.
    
    Args:
        email: Email to verify
        password: Password to verify
        
    Returns:
        bool: True if credentials match official admin credentials
    """
    from django.contrib.auth import authenticate
    
    # Check email matches
    if email.strip().lower() != OFFICIAL_ADMIN_EMAIL.lower():
        security_logger.warning(f"Invalid admin email attempted: {email}")
        return False
    
    # Authenticate with Django
    user = authenticate(email=email, password=password)
    
    if user is None:
        security_logger.warning(f"Failed admin password verification for: {email}")
        return False
    
    # Verify is_admin check passes
    if not user.is_admin():
        security_logger.warning(f"Admin privileges check failed for: {email}")
        return False
    
    security_logger.info(f"Admin credentials verified successfully at {timezone.now()}")
    return True


def reset_admin_password(new_password):
    """
    Securely reset the official admin password.
    
    Args:
        new_password: New password to set
        
    Raises:
        ValidationError: If admin user not found
        PermissionDenied: If operation fails security checks
    """
    try:
        admin = User.objects.get(email=OFFICIAL_ADMIN_EMAIL)
        admin.set_password(new_password)
        admin.save()
        security_logger.warning(f"Admin password reset at {timezone.now()}")
        return True
    except User.DoesNotExist:
        error_msg = f"Cannot reset password: Admin user not found"
        security_logger.critical(error_msg)
        raise ValidationError(error_msg)
