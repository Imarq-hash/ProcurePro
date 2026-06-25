import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procurepro_project.settings')
django.setup()

from procurement.models import User, ContractorProfile, Tender, AdminProfile

def seed():
    print("Clearing old mock data...")
    ContractorProfile.objects.all().delete()
    Tender.objects.all().delete()
    # Delete non-admin users to clean up emails
    User.objects.filter(role=User.Role.CONTRACTOR).delete()

    print("Seeding 6 contractors...")
    contractors_data = [
        ("apex@example.com", "Apex Structural Ltd", "14 Independence Avenue, Accra", "CONSTRUCTION", 12, "DE-9921-X", "+233 20 123 4567"),
        ("stivo@example.com", "Stivo & Co Ltd", "Kumasi, Ashanti Region", "ELECTRICAL", 5, "EL-3341-Y", "+233 24 555 1234"),
        ("quansah@example.com", "K Quansah Ltd", "Tema, Greater Accra", "PLUMBING", 8, "PL-1122-Z", "+233 27 888 9999"),
        ("valor@example.com", "Women of Valor Ltd", "Wa, Upper West", "INFRASTRUCTURE", 10, "IN-7766-W", "+233 50 111 2222"),
        ("fayol@example.com", "Fayol Construction", "Madina, Accra", "CONSTRUCTION", 4, "CO-5544-V", "+233 26 777 8888"),
        ("ave@example.com", "Ave Konstrakz", "Cape Coast, Central Region", "OTHER", 7, "OT-2233-U", "+233 20 999 0000"),
    ]
    
    for email, company, address, spec, exp, lic, phone in contractors_data:
        user = User.objects.create_user(email=email, password='password123', role=User.Role.CONTRACTOR)
        ContractorProfile.objects.create(
            user=user,
            company_name=company,
            address=address,
            specialization=spec,
            experience_years=exp,
            license_number=lic,
            status=ContractorProfile.Status.APPROVED,
            phone=phone
        )

    print("Ensuring Admin exists for tenders...")
    admin_user = User.objects.filter(role=User.Role.ADMIN).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(email="admin@procurepro.com", password="adminpassword")
        
    admin_profile, _ = AdminProfile.objects.get_or_create(
        user=admin_user,
        defaults={'name': 'ProcurePro Admin', 'department': 'Central Procurement'}
    )

    print("Seeding 6 tenders...")
    tenders_data = [
        ("Public School Renovation & Expansion", "Renovation of existing facilities and construction of new wings for a public elementary school, including modern classrooms and playground.", "Accra", 4200000, 5000000, "CONSTRUCTION", 30),
        ("National Highway Resurfacing", "Comprehensive resurfacing of 50km of the main national highway, including drainage improvements and road markings.", "Tema", 15000000, 20000000, "INFRASTRUCTURE", 60),
        ("Regional Hospital Electrical Upgrade", "Complete overhaul of the electrical grid for the regional hospital to support new MRI and intensive care units.", "Kumasi", 800000, 1200000, "ELECTRICAL", 45),
        ("Municipal Water Supply Extension", "Extension of the municipal water supply lines to newly developed residential areas, including pumping stations.", "Madina", 2500000, 3000000, "PLUMBING", 90),
        ("University Library Construction", "Construction of a new 3-story modern library complex for the university campus.", "Cape Coast", 8500000, 10000000, "CONSTRUCTION", 120),
        ("Solar Farm Installation", "Installation of a 5MW solar farm to supplement the national grid in the northern sector.", "Wa", 5000000, 7500000, "ELECTRICAL", 180),
    ]

    for title, desc, loc, b_min, b_max, cat, days in tenders_data:
        Tender.objects.create(
            admin=admin_profile,
            title=title,
            description=desc,
            location=loc,
            budget_min=b_min,
            budget_max=b_max,
            category=cat,
            status=Tender.Status.OPEN,
            deadline=timezone.now() + timedelta(days=days)
        )

    print("Successfully seeded 6 contractors and 6 tenders!")

if __name__ == '__main__':
    seed()
