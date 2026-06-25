from django.urls import reverse
from django.test import TestCase
from .models import User, ContractorProfile


class AuthTests(TestCase):
    def test_contractor_signup_creates_user_and_redirects(self):
        signup_url = reverse('signup')
        response = self.client.post(signup_url, {
            'email': 'contractor@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
            'company_name': 'Test Contractor',
            'license_number': 'LIC12345',
            'phone': '0244123456',
            'address': '1 Test Street',
            'specialization': 'Infrastructure',
            'experience': '5',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        user = User.objects.filter(email='contractor@example.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertEqual(user.role, User.Role.CONTRACTOR)
        self.assertTrue(hasattr(user, 'contractor_profile'))
        self.assertEqual(user.contractor_profile.company_name, 'Test Contractor')

    def test_signin_as_admin_with_non_admin_user_fails(self):
        user = User.objects.create_user(
            email='user@example.com',
            password='StrongPass123!'
        )
        signin_url = reverse('signin')
        response = self.client.post(signin_url, {
            'email': user.email,
            'password': 'StrongPass123!',
            'login_type': 'admin',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'procurement/admin_login.html')
        self.assertContains(response, 'Access Denied: You do not have administrative privileges.')

    def test_admin_signin_redirects_to_admin_dashboard(self):
        admin = User.objects.create_user(
            email='admin@example.com',
            password='AdminPass123!@',
            role=User.Role.ADMIN,
            is_staff=True,
        )
        signin_url = reverse('signin')
        response = self.client.post(signin_url, {
            'email': admin.email,
            'password': 'AdminPass123!@',
            'login_type': 'admin',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('admin_dashboard'))

    def test_contractor_signin_redirects_to_dashboard(self):
        contractor = User.objects.create_user(
            email='contractor2@example.com',
            password='ContractorPass1!'
        )
        signin_url = reverse('signin')
        response = self.client.post(signin_url, {
            'email': contractor.email,
            'password': 'ContractorPass1!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_non_contractor_cannot_access_contractor_pages(self):
        user = User.objects.create_user(
            email='user2@example.com',
            password='UserPass123!'
            # default role is CONTRACTOR by model default; change to admin to simulate non-contractor user
        )
        user.role = User.Role.ADMIN
        user.is_staff = True
        user.save()

        self.client.login(email=user.email, password='UserPass123!')

        restricted_urls = [
            reverse('dashboard'),
            reverse('my_bids'),
            reverse('tenders'),
            reverse('settings')
        ]

        for url in restricted_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200, f'{url} should not be accessible by non-contractor')
            self.assertIn(response.status_code, (302, 301), f'{url} should redirect for non-contractor access')

    def test_non_contractor_cannot_access_contractor_profile_view(self):
        contractor = User.objects.create_user(
            email='contractor-test@example.com',
            password='ContractorPass123!'
        )
        ContractorProfile.objects.create(
            user=contractor,
            company_name='Test Contractor',
            license_number='LIC999',
            status=ContractorProfile.Status.APPROVED
        )

        non_contractor = User.objects.create_user(
            email='user3@example.com',
            password='UserPass456!'
        )
        non_contractor.role = User.Role.ADMIN
        non_contractor.is_staff = True
        non_contractor.save()

        self.client.login(email=non_contractor.email, password='UserPass456!')
        response = self.client.get(reverse('contractor_profile', args=[contractor.pk]))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, (302, 301))
