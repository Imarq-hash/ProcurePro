from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from decimal import Decimal, InvalidOperation
from datetime import datetime
import os
import logging
from django_ratelimit.decorators import ratelimit
from .models import Notification, User, ContractorProfile, Tender, TenderRequest, Bid
from .admin_security import verify_admin_credentials

logger = logging.getLogger('procurepro')
security_logger = logging.getLogger('procurepro.security')

def validate_document_file(file):
    """Validate uploaded file for security and size constraints."""
    from django.conf import settings
    
    # Check file size
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if file.size > max_size:
        raise ValidationError(f'File size exceeds maximum allowed size of {max_size // 1024 // 1024}MB.')
    
    # Check file extension
    allowed_extensions = getattr(settings, 'ALLOWED_UPLOAD_EXTENSIONS', ('pdf', 'doc', 'docx', 'xls', 'xlsx'))
    file_ext = os.path.splitext(file.name)[1].lstrip('.').lower()
    if file_ext not in allowed_extensions:
        raise ValidationError(f'File type ".{file_ext}" is not allowed. Allowed types: {", ".join(allowed_extensions)}')
    
    # Check file content type
    allowed_content_types = {
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }
    if file.content_type not in allowed_content_types:
        raise ValidationError(f'Invalid file content type: {file.content_type}')
    
    return True


def redirect_non_contractor_user(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    return redirect('home')


def home_view(request):
    featured_tenders = Tender.objects.filter(status=Tender.Status.OPEN).order_by('-created_at')[:3]
    top_contractors = ContractorProfile.objects.annotate(num_bids=Count('bids')).order_by('-num_bids')[:3]
    completed_projects = Tender.objects.filter(status=Tender.Status.CLOSED).order_by('-updated_at')[:3]
    
    context = {
        'featured_tenders': featured_tenders,
        'top_contractors': top_contractors,
        'completed_projects': completed_projects,
    }
    return render(request, 'procurement/index.html', context)

@ratelimit(key='ip', rate='5/h', method='POST')
def signin_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    safe_next = next_url if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()) else None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')
        
        # Extra security verification for admin logins
        if login_type == 'admin':
            if not verify_admin_credentials(email, password):
                security_logger.warning(f'Failed admin login attempt for email: {email} from IP: {request.META.get("REMOTE_ADDR")}')
                messages.error(request, 'Invalid email or password.')
                return render(request, 'procurement/admin_login.html')
            security_logger.info(f'Admin login verified: {email} from IP: {request.META.get("REMOTE_ADDR")}')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if login_type == 'admin' and not user.is_admin():
                messages.error(request, 'Access Denied: You do not have administrative privileges.')
                return render(request, 'procurement/admin_login.html')

            login(request, user)
            logger.info(f'User logged in: {user.email} (role={user.role})')
            if user.is_admin():
                return redirect('admin_dashboard')
            return redirect(safe_next or 'dashboard')
        else:
            security_logger.warning(f'Failed login attempt for email: {email} from IP: {request.META.get("REMOTE_ADDR")}')
            if login_type == 'admin':
                messages.error(request, 'Invalid email or password.')
                return render(request, 'procurement/admin_login.html')
            messages.error(request, 'Invalid email or password. If you do not have an account, please sign up.')
            
    return render(request, 'procurement/signin.html', {'next': safe_next})

@ratelimit(key='ip', rate='5/h', method='POST')
def signup_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    safe_next = next_url if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()) else None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        company_name = request.POST.get('company_name')
        license_number = request.POST.get('license_number')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        
        if not password or password != confirm_password:
            messages.error(request, 'Passwords do not match or are empty.')
            return render(request, 'procurement/signup.html', {'next': safe_next})
            
        try:
            validate_password(password)
        except ValidationError as password_errors:
            for error in password_errors:
                messages.error(request, error)
            return render(request, 'procurement/signup.html', {'next': safe_next})
            
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists. Please sign in instead.')
            return render(request, 'procurement/signup.html', {'next': safe_next})
            
        user = User.objects.create_user(email=email, password=password, role=User.Role.CONTRACTOR)
        ContractorProfile.objects.create(
            user=user,
            company_name=company_name or email.split('@')[0],
            license_number=license_number if license_number else None,
            phone=phone,
            address=address,
            specialization=specialization,
            experience_years=int(experience) if experience and experience.isdigit() else None,
            status='PENDING'
        )
        logger.info(f'New user registered: {user.email}')
        login(request, user)
        return redirect(safe_next or 'dashboard')
    return render(request, 'procurement/signup.html', {'next': safe_next})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@ratelimit(key='user', rate='5/h', method='POST')
def request_tender_view(request):
    """Handle tender requests with authentication and validation."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        tender_title = request.POST.get('tender_title', '').strip()
        description = request.POST.get('description', '').strip()
        document = request.FILES.get('document')

        # SECURITY: Verify email ownership - only allow user's own email
        if email != request.user.email:
            security_logger.warning(f'Email mismatch: user {request.user.email} attempted to submit tender for {email}')
            messages.error(request, 'You can only submit tender requests using your registered email address.')
            return render(request, 'procurement/request_tender.html')

        # Validate required fields
        if not name or len(name) < 2 or len(name) > 255:
            messages.error(request, 'Name must be between 2 and 255 characters.')
            return render(request, 'procurement/request_tender.html')
        
        if not tender_title or len(tender_title) < 5 or len(tender_title) > 255:
            messages.error(request, 'Tender title must be between 5 and 255 characters.')
            return render(request, 'procurement/request_tender.html')
        
        if not description or len(description) < 20 or len(description) > 5000:
            messages.error(request, 'Description must be between 20 and 5000 characters.')
            return render(request, 'procurement/request_tender.html')

        # Validate document if provided
        if document:
            try:
                validate_document_file(document)
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'procurement/request_tender.html')

        # Store in DB
        tender_request = TenderRequest.objects.create(
            name=name,
            email=email,
            tender_title=tender_title,
            description=description,
            document=document
        )
        
        logger.info(f'Tender request created: ID={tender_request.id}, title="{tender_title}", user={request.user.email}')

        # Notify Admins with review link
        admins = User.objects.filter(role=User.Role.ADMIN)
        review_url = reverse('admin_review_request', args=[tender_request.id])
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"New Tender Request: '{tender_title}' from {name} ({email}).",
                link=review_url
            )
        
        messages.success(request, 'Your tender request has been submitted successfully. We will review it shortly.')
        return redirect('dashboard')

    return render(request, 'procurement/request_tender.html')


@login_required
def dashboard_view(request):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)
        
    try:
        contractor = request.user.contractor_profile
        my_bids = contractor.bids.all().order_by('-submitted_at')[:5]
        my_bids_count = contractor.bids.count()
    except ContractorProfile.DoesNotExist:
        my_bids = []
        my_bids_count = 0

    open_tenders = Tender.objects.filter(status=Tender.Status.OPEN).order_by('-created_at')[:5]
    
    # Stats
    open_tenders_count = Tender.objects.filter(status=Tender.Status.OPEN).count()
    closed_tenders_count = Tender.objects.filter(status=Tender.Status.CLOSED).count()
    notifications_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'my_bids': my_bids,
        'open_tenders': open_tenders,
        'stats': {
            'my_bids': my_bids_count,
            'open_tenders': open_tenders_count,
            'closed_tenders': closed_tenders_count,
            'notifications': notifications_count,
        }
    }
    return render(request, 'procurement/dashboard.html', context)

@login_required
def my_bids_view(request):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)
        
    try:
        contractor = request.user.contractor_profile
        all_bids = contractor.bids.all().order_by('-submitted_at')
        total_bids = all_bids.count()
        pending_bids = all_bids.filter(status='SUBMITTED').count() + all_bids.filter(status='UNDER_REVIEW').count()
        accepted_bids = all_bids.filter(status='ACCEPTED').count()
    except ContractorProfile.DoesNotExist:
        all_bids = []
        total_bids = 0
        pending_bids = 0
        accepted_bids = 0
        
    context = {
        'bids': all_bids,
        'stats': {
            'total': total_bids,
            'pending': pending_bids,
            'accepted': accepted_bids
        }
    }
    return render(request, 'procurement/my_bids.html', context)

@login_required
def admin_dashboard_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
        
    context = {
        'stats': {
            'total_contractors': ContractorProfile.objects.count(),
            'active_tenders': Tender.objects.filter(status=Tender.Status.OPEN).count(),
            'submitted_bids': Bid.objects.count(),
            'closed_tenders': Tender.objects.filter(status=Tender.Status.CLOSED).count(),
        },
        'recent_bids': Bid.objects.all().order_by('-submitted_at')[:5],
        'tender_requests': TenderRequest.objects.filter(is_processed=False).order_by('-created_at')[:3]
    }
    return render(request, 'procurement/admin_dashboard.html', context)




@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    cache_key = f'unread_notifications_count_{request.user.id}'
    cache.set(cache_key, request.user.notifications.filter(is_read=False).count(), 60)
    return JsonResponse({'status': 'success'})

@login_required
def mark_all_notifications_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    cache_key = f'unread_notifications_count_{request.user.id}'
    cache.set(cache_key, 0, 60)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def admin_tender_requests_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    
    requests_list = TenderRequest.objects.all().order_by('-created_at')
    
    context = {
        'requests': requests_list,
        'active_tab': 'tender_requests'
    }
    return render(request, 'procurement/admin_tender_requests.html', context)

@login_required
def admin_review_request_view(request, pk):
    if not request.user.is_admin():
        return redirect('dashboard')
        
    tender_request = get_object_or_404(TenderRequest, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category')
            location = request.POST.get('location')
            budget_min = request.POST.get('budget_min')
            budget_max = request.POST.get('budget_max')
            deadline = request.POST.get('deadline')
            
            b_min = float(budget_min) if budget_min else None
            b_max = float(budget_max) if budget_max else None
            
            # SECURITY: Only allow actual admin users to access this function
            try:
                admin_profile = request.user.admin_profile
            except AttributeError:
                # Log security incident and deny access
                import logging
                logger = logging.getLogger('procurepro.security')
                logger.warning(f'Privilege escalation attempt: user {request.user.email} tried to review tender request without admin profile')
                messages.error(request, 'Access Denied: You do not have administrative privileges.')
                return redirect('dashboard')
                
            tender = Tender.objects.create(
                admin=admin_profile,
                title=title,
                description=description,
                category=category,
                location=location,
                budget_min=b_min,
                budget_max=b_max,
                deadline=deadline,
                status=Tender.Status.OPEN
            )
            
            if tender_request.document:
                from .models import Document
                Document.objects.create(
                    entity_type=Document.EntityType.TENDER,
                    entity_id=tender.id,
                    file=tender_request.document,
                    file_name=tender_request.document.name.split('/')[-1]
                )
            
            tender_request.status = TenderRequest.Status.APPROVED
            tender_request.is_processed = True
            tender_request.save()
            
            user = User.objects.filter(email=tender_request.email).first()
            if user:
                Notification.objects.create(
                    user=user,
                    message=f"Your tender request '{tender.title}' has been APPROVED and published!"
                )
                
            messages.success(request, f"Tender '{tender.title}' has been successfully published!")
            return redirect('admin_tender_requests')
            
        elif action == 'decline':
            tender_request.status = TenderRequest.Status.DECLINED
            tender_request.is_processed = True
            tender_request.save()
            
            user = User.objects.filter(email=tender_request.email).first()
            if user:
                Notification.objects.create(
                    user=user,
                    message=f"Your tender request '{tender_request.tender_title}' has been declined."
                )
                
            messages.success(request, f"Tender request '{tender_request.tender_title}' was declined.")
            return redirect('admin_tender_requests')
            
    context = {
        'tender_request': tender_request,
        'categories': Tender.Category.choices,
        'active_tab': 'tender_requests'
    }
    return render(request, 'procurement/admin_review_request.html', context)

@login_required
def tenders_list_view(request):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)

    tenders = Tender.objects.filter(status=Tender.Status.OPEN).order_by('-created_at')
    
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    budget_range = request.GET.get('budget', '')
    
    if query:
        tenders = tenders.filter(title__icontains=query) | tenders.filter(description__icontains=query)
    if category:
        tenders = tenders.filter(category=category.upper())
    if location:
        tenders = tenders.filter(location__icontains=location)
    if budget_range:
        if budget_range == '0-500k':
            tenders = tenders.filter(budget_max__lte=500000)
        elif budget_range == '500k-1m':
            tenders = tenders.filter(budget_min__gte=500000, budget_max__lte=1000000)
        elif budget_range == '1m+':
            tenders = tenders.filter(budget_max__gt=1000000)
            
    context = {
        'tenders': tenders,
        'categories': Tender.Category.choices
    }
    return render(request, 'procurement/tenders.html', context)

def contractors_list_view(request):
    # SECURITY: Only show approved contractors to public
    contractors = ContractorProfile.objects.filter(
        status=ContractorProfile.Status.APPROVED
    ).order_by('company_name')
    
    # Handle search
    query = request.GET.get('q', '')
    if query:
        contractors = contractors.filter(company_name__icontains=query) | contractors.filter(specialization__icontains=query)
    
    # Handle location filter
    location = request.GET.get('location', '')
    if location:
        contractors = contractors.filter(address__icontains=location)
    
    # Handle specialization filter
    specialization = request.GET.get('specialization', '')
    if specialization:
        contractors = contractors.filter(specialization__icontains=specialization)
    
    # Handle experience filter
    experience = request.GET.get('experience', '')
    if experience:
        if experience == '0-5':
            contractors = contractors.filter(experience_years__lte=5)
        elif experience == '5-10':
            contractors = contractors.filter(experience_years__gte=5, experience_years__lte=10)
        elif experience == '10+':
            contractors = contractors.filter(experience_years__gte=10)
    
    context = {
        'contractors': contractors
    }
    return render(request, 'procurement/contractors.html', context)

@login_required
def contractor_profile_view(request, pk):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)

    contractor = get_object_or_404(ContractorProfile, pk=pk)
    context = {
        'contractor': contractor
    }
    return render(request, 'procurement/contractor_profile.html', context)

@login_required
def tender_details_view(request, pk):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)

    tender = get_object_or_404(Tender, pk=pk)
    context = {
        'tender': tender
    }
    return render(request, 'procurement/project_details.html', context)

@login_required
def submit_bid_view(request, pk):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)
        
    tender = get_object_or_404(Tender, pk=pk)
    
    try:
        contractor = request.user.contractor_profile
    except ContractorProfile.DoesNotExist:
        messages.error(request, 'You must complete your contractor profile before submitting bids.')
        return redirect('settings')
    
    # SECURITY: Enforce contractor profile status - only APPROVED contractors can bid
    if contractor.status != ContractorProfile.Status.APPROVED:
        security_logger.warning(f'Unapproved contractor {request.user.email} (status={contractor.status}) attempted to submit bid')
        messages.error(request, f'Your contractor profile must be APPROVED to submit bids. Current status: {contractor.status}. Please contact support.')
        return redirect('settings')
        
    if request.method == 'POST':
        # Validate and parse amount
        try:
            amount = Decimal(request.POST.get('amount', '0').strip())
            if amount <= 0:
                raise ValueError('Bid amount must be greater than zero')
            if amount > Decimal('999999999.99'):
                raise ValueError('Bid amount exceeds maximum allowed value')
        except (TypeError, ValueError, InvalidOperation) as e:
            messages.error(request, 'Bid amount must be a valid positive number.')
            return render(request, 'procurement/submit_bid.html', {'tender': tender})
        
        # Validate duration
        duration = request.POST.get('duration', '').strip()
        if not duration or len(duration) < 3 or len(duration) > 100:
            messages.error(request, 'Duration must be between 3 and 100 characters (e.g., "6 Months").')
            return render(request, 'procurement/submit_bid.html', {'tender': tender})
        
        # Validate proposal text
        proposal_text = request.POST.get('proposal_text', '').strip()
        if not proposal_text or len(proposal_text) < 100 or len(proposal_text) > 5000:
            messages.error(request, 'Proposal must be between 100 and 5000 characters.')
            return render(request, 'procurement/submit_bid.html', {'tender': tender})
        
        # Validate deadline hasn't passed
        if tender.deadline and timezone.now() > tender.deadline:
            messages.error(request, 'This tender\'s deadline has passed. No new bids can be submitted.')
            return render(request, 'procurement/submit_bid.html', {'tender': tender})
        
        # Create bid
        bid = Bid.objects.create(
            tender=tender,
            contractor=contractor,
            amount=amount,
            duration=duration,
            proposal_text=proposal_text,
            status=Bid.Status.SUBMITTED
        )
        
        logger.info(f'Bid submitted: ID={bid.id}, tender={tender.title}, contractor={contractor.company_name}, amount={amount}')
        messages.success(request, f'Your bid for "{tender.title}" was submitted successfully!')
        return redirect('my_bids')
        
    context = {
        'tender': tender
    }
    return render(request, 'procurement/submit_bid.html', context)

@login_required
def admin_post_tender_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', '').upper()
        location = request.POST.get('location', '').strip()
        budget_min = request.POST.get('budget_min', '').strip()
        budget_max = request.POST.get('budget_max', '').strip()
        deadline = request.POST.get('deadline', '').strip()
        
        # Validate title
        if not title or len(title) < 5 or len(title) > 255:
            messages.error(request, 'Tender title must be between 5 and 255 characters.')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # Validate description
        if not description or len(description) < 20 or len(description) > 5000:
            messages.error(request, 'Description must be between 20 and 5000 characters.')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # Validate category
        valid_categories = dict(Tender.Category.choices)
        if category not in valid_categories:
            messages.error(request, 'Invalid category selected.')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # Validate location
        if not location or len(location) < 2 or len(location) > 255:
            messages.error(request, 'Location must be between 2 and 255 characters.')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # Validate budgets
        try:
            b_min = Decimal(budget_min) if budget_min else None
            b_max = Decimal(budget_max) if budget_max else None
            
            if b_min is not None and b_min < 0:
                raise ValueError('Minimum budget cannot be negative')
            if b_max is not None and b_max < 0:
                raise ValueError('Maximum budget cannot be negative')
            if b_min is not None and b_max is not None and b_min > b_max:
                raise ValueError('Minimum budget cannot exceed maximum budget')
        except (ValueError, InvalidOperation) as e:
            messages.error(request, f'Invalid budget amounts: {str(e)}')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # Validate deadline
        try:
            deadline_dt = datetime.fromisoformat(deadline)
            if timezone.make_aware(deadline_dt) <= timezone.now():
                raise ValueError('Deadline must be in the future')
        except (ValueError, TypeError) as e:
            messages.error(request, 'Invalid deadline. Deadline must be a future date and time.')
            return render(request, 'procurement/admin_post_tender.html', {'categories': Tender.Category.choices})
        
        # SECURITY: Only allow actual admin users to access this function
        try:
            admin_profile = request.user.admin_profile
        except AttributeError:
            # Log security incident and deny access
            security_logger.warning(f'Privilege escalation attempt: user {request.user.email} tried to post tender without admin profile')
            messages.error(request, 'Access Denied: You do not have administrative privileges.')
            return redirect('dashboard')
            
        tender = Tender.objects.create(
            admin=admin_profile,
            title=title,
            description=description,
            category=category,
            location=location,
            budget_min=b_min,
            budget_max=b_max,
            deadline=deadline_dt,
            status=Tender.Status.OPEN
        )
        
        logger.info(f'Tender created by admin {request.user.email}: ID={tender.id}, title="{title}"')
        messages.success(request, f'Tender "{title}" was published successfully!')
        return redirect('admin_manage_tenders')
        
    context = {
        'categories': Tender.Category.choices
    }
    return render(request, 'procurement/admin_post_tender.html', context)

@login_required
def admin_manage_tenders_view(request):
    from django.core.paginator import Paginator
    
    if not request.user.is_admin():
        return redirect('dashboard')
    
    # Get all tenders and paginate
    tenders_list = Tender.objects.all().order_by('-created_at')
    paginator = Paginator(tenders_list, 25)  # Show 25 tenders per page
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    context = {
        'tenders': page,
        'page_obj': page
    }
    return render(request, 'procurement/admin_manage_tenders.html', context)

@login_required
def admin_contractors_view(request):
    from django.core.paginator import Paginator
    
    if not request.user.is_admin():
        return redirect('dashboard')
    
    # Get all contractors and paginate
    contractors_list = ContractorProfile.objects.all().order_by('-user__date_joined')
    paginator = Paginator(contractors_list, 25)  # Show 25 contractors per page
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    return render(request, 'procurement/admin_contractors.html', {'contractors': page, 'page_obj': page})

@login_required
def admin_review_bids_view(request):
    from django.core.paginator import Paginator
    
    if not request.user.is_admin():
        return redirect('dashboard')
    
    # Get pending bids and paginate
    bids_list = Bid.objects.filter(status__in=[Bid.Status.SUBMITTED, Bid.Status.UNDER_REVIEW]).order_by('submitted_at')
    paginator = Paginator(bids_list, 25)  # Show 25 bids per page
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    return render(request, 'procurement/admin_review_bids.html', {'pending_bids': page, 'page_obj': page})

@login_required
def admin_reports_view(request):
    if not request.user.is_admin():
        return redirect('dashboard')
    
    # Calculate some basic metrics
    total_tenders = Tender.objects.count()
    total_bids = Bid.objects.count()
    active_contractors = ContractorProfile.objects.filter(status='APPROVED').count()
    
    context = {
        'total_tenders': total_tenders,
        'total_bids': total_bids,
        'active_contractors': active_contractors,
    }
    return render(request, 'procurement/admin_reports.html', context)

@login_required
def settings_view(request):
    if not request.user.is_contractor():
        return redirect_non_contractor_user(request)

    try:
        profile = request.user.contractor_profile
    except ContractorProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if profile and company_name:
            profile.company_name = company_name
            profile.save()
            messages.success(request, "Settings updated successfully!")
            return redirect('settings')
            
    return render(request, 'procurement/settings.html', {'profile': profile})


@login_required
def download_tender_document(request, tender_request_id):
    """Protected document download - only admins can download."""
    tender_request = get_object_or_404(TenderRequest, pk=tender_request_id)
    
    # SECURITY: Only admin can download documents
    if not request.user.is_admin():
        security_logger.warning(f'Unauthorized document download attempt: user {request.user.email} for tender_request {tender_request_id}')
        messages.error(request, 'You do not have permission to download this document.')
        return redirect('home')
    
    if not tender_request.document:
        messages.error(request, 'Document not found.')
        return redirect('admin_tender_requests')
    
    try:
        # Serve file without exposing file path
        response = FileResponse(tender_request.document.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{tender_request.document.name.split("/")[-1]}"'
        logger.info(f'Document downloaded by admin {request.user.email}: tender_request {tender_request_id}')
        return response
    except Exception as e:
        logger.error(f'Error downloading document: {str(e)}')
        messages.error(request, 'Error downloading document.')
        return redirect('admin_tender_requests')
