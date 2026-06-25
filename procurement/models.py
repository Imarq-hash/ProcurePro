from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        CONTRACTOR = 'CONTRACTOR', _('Contractor')

    # Replace username with email as the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CONTRACTOR)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_admin(self):
        # Consider both role and Django staff/superuser flags to reduce accidental privilege grants.
        return self.role == self.Role.ADMIN and (self.is_staff or self.is_superuser)

    def is_contractor(self):
        return self.role == self.Role.CONTRACTOR


class ContractorProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        SUSPENDED = 'SUSPENDED', _('Suspended')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contractor_profile')
    company_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    @property
    def image_url(self):
        contractor_images = [
            '/static/assets/contractor1.jpg',
            '/static/assets/contractor2.jpg',
            '/static/assets/contractor3.jpg',
            '/static/assets/contractor6.png',
            '/static/assets/conntractor4.png',
            '/static/assets/contractr5.png',
        ]
        index = self.pk % len(contractor_images) if self.pk else 0
        return contractor_images[index]

    def __str__(self):
        return self.company_name

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Tender(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CLOSED = 'CLOSED', _('Closed')
        DRAFT = 'DRAFT', _('Draft')

    class Category(models.TextChoices):
        CONSTRUCTION = 'CONSTRUCTION', _('Construction')
        INFRASTRUCTURE = 'INFRASTRUCTURE', _('Infrastructure')
        ELECTRICAL = 'ELECTRICAL', _('Electrical/Energy')
        PLUMBING = 'PLUMBING', _('Plumbing')
        OTHER = 'OTHER', _('Other')

    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, related_name='tenders_posted')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    budget_min = models.DecimalField(max_length=15, decimal_places=2, max_digits=15, null=True, blank=True)
    budget_max = models.DecimalField(max_length=15, decimal_places=2, max_digits=15, null=True, blank=True)
    category = models.CharField(max_length=50, choices=Category.choices)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def image_url(self):
        category_images = {
            'CONSTRUCTION': [
                '/static/assets/school_block.png',
                '/static/assets/road_repair.png',
                '/static/assets/building.jpg'
            ],
            'INFRASTRUCTURE': [
                '/static/assets/road_repair.png',
                '/static/assets/road.jpg',
                '/static/assets/hardhat_hero.png'
            ],
            'ELECTRICAL': [
                '/static/assets/hospital_electrical.png',
                '/static/assets/road.jpg',
                '/static/assets/building.jpg'
            ],
            'PLUMBING': [
                '/static/assets/contractor1.jpg',
                '/static/assets/contractor3.jpg',
                '/static/assets/contractor6.png'
            ],
            'OTHER': [
                '/static/assets/contractor2.jpg',
                '/static/assets/contractr5.png',
                '/static/assets/building.jpg'
            ],
        }
        images = category_images.get(self.category, category_images['OTHER'])
        index = self.pk % len(images) if self.pk else 0
        return images[index]

    def __str__(self):
        return self.title

class Bid(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', _('Submitted')
        UNDER_REVIEW = 'UNDER_REVIEW', _('Under Review')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        REJECTED = 'REJECTED', _('Rejected')

    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='bids')
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    duration = models.CharField(max_length=100) # e.g., '6 Months'
    proposal_text = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.contractor.company_name} for {self.tender.title}"

class Document(models.Model):
    class EntityType(models.TextChoices):
        TENDER = 'TENDER', _('Tender')
        BID = 'BID', _('Bid')
        CONTRACTOR = 'CONTRACTOR', _('Contractor Profile')

    entity_type = models.CharField(max_length=20, choices=EntityType.choices)
    entity_id = models.PositiveIntegerField() # A simple generic link, or could use contenttypes framework
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.link:
            trimmed_link = self.link.strip()
            if trimmed_link.lower().startswith('javascript:') or trimmed_link.lower().startswith('data:'):
                raise ValidationError('Invalid notification link.')
            if not trimmed_link.startswith('/') or trimmed_link.startswith('//'):
                raise ValidationError('Notification links must be internal and start with a single /.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"To {self.user.email}: {self.message[:20]}"

class TenderRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        DECLINED = 'DECLINED', _('Declined')

    name = models.CharField(max_length=255)
    email = models.EmailField()
    tender_title = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='tender_requests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Request for {self.tender_title} by {self.name}"

