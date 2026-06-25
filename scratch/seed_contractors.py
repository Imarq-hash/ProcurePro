import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procurepro_project.settings')
django.setup()

from procurement.models import User, ContractorProfile

def seed():
    # Create some mock contractors if none exist
    if ContractorProfile.objects.count() == 0:
        print("Seeding contractors...")
        
        users_data = [
            ("apex@example.com", "Apex Structural Ltd", "Accra, Ghana", "Construction & Infrastructure", 12, "DE-9921-X"),
            ("stivo@example.com", "Stivo & Co Ltd", "Kumasi, Ghana", "Electrical", 5, "EL-3341-Y"),
            ("quansah@example.com", "K Quansah Ltd", "Accra, Ghana", "Plumbing", 8, "PL-1122-Z"),
        ]
        
        for email, company, address, spec, exp, lic in users_data:
            user = User.objects.create_user(email=email, password='password123', role=User.Role.CONTRACTOR)
            ContractorProfile.objects.create(
                user=user,
                company_name=company,
                address=address,
                specialization=spec,
                experience_years=exp,
                license_number=lic,
                status=ContractorProfile.Status.APPROVED,
                phone="+233 20 123 4567"
            )
        print("Done seeding contractors.")
    else:
        print(f"Already have {ContractorProfile.objects.count()} contractors.")

if __name__ == '__main__':
    seed()
