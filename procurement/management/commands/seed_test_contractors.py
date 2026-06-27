from django.core.management.base import BaseCommand

from procurement.models import ContractorProfile, User


CONTRACTORS = [
    {
        "company_name": "Apex Structural Ltd.",
        "email": "admin@apexstructural.com.gh",
        "password": "SecurePass123!",
        "contact_person": "Kwame Mensah",
        "phone": "+233 24 123 4567",
        "registration_number": "CS1209384",
        "location": "East Legon, Accra, Ghana",
        "specialization": "Civil Engineering & Road Construction",
        "experience_years": 15,
    },
    {
        "company_name": "Horizon Tech Solutions",
        "email": "info@horizontech.io",
        "password": "SecurePass123!",
        "contact_person": "Sarah Ofori",
        "phone": "+233 20 987 6543",
        "registration_number": "CS9948271",
        "location": "Airport Residential Area, Accra, Ghana",
        "specialization": "IT Infrastructure & Software Supply",
        "experience_years": 8,
    },
    {
        "company_name": "BuildRight Logistics",
        "email": "procurement@buildrightlogistics.com",
        "password": "SecurePass123!",
        "contact_person": "David Ansah",
        "phone": "+233 55 444 3322",
        "registration_number": "CS4455667",
        "location": "Tema Industrial Area, Tema, Ghana",
        "specialization": "Heavy Equipment & Material Supply",
        "experience_years": 10,
    },
    {
        "company_name": "EcoGreen Facilities",
        "email": "hello@ecogreenfacilities.com",
        "password": "SecurePass123!",
        "contact_person": "Abena Appiah",
        "phone": "+233 27 111 2233",
        "registration_number": "CS7788990",
        "location": "Kumasi, Ashanti Region, Ghana",
        "specialization": "Facilities Management & Janitorial Services",
        "experience_years": 7,
    },
    {
        "company_name": "Zenith Electricals",
        "email": "bids@zenithelectricals.net",
        "password": "SecurePass123!",
        "contact_person": "Emmanuel Tetteh",
        "phone": "+233 50 555 8899",
        "registration_number": "CS2233445",
        "location": "Spintex Road, Accra, Ghana",
        "specialization": "Electrical Engineering & Solar Power",
        "experience_years": 12,
    },
    {
        "company_name": "Vanguard Health",
        "email": "supply@vanguardhealth.com.gh",
        "password": "SecurePass123!",
        "contact_person": "Dr. Grace Addo",
        "phone": "+233 24 777 9900",
        "registration_number": "CS1122334",
        "location": "Ridge, Accra, Ghana",
        "specialization": "Medical Equipment & Pharmaceuticals",
        "experience_years": 9,
    },
]


class Command(BaseCommand):
    help = "Seed the database with realistic approved contractor test accounts."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for contractor in CONTRACTORS:
            names = contractor["contact_person"].split(" ", 1)
            user, user_created = User.objects.get_or_create(
                email=contractor["email"].lower(),
                defaults={
                    "role": User.Role.CONTRACTOR,
                    "first_name": names[0],
                    "last_name": names[1] if len(names) > 1 else "",
                },
            )
            user.role = User.Role.CONTRACTOR
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ""
            user.set_password(contractor["password"])
            user.save()

            ContractorProfile.objects.update_or_create(
                user=user,
                defaults={
                    "company_name": contractor["company_name"],
                    "license_number": contractor["registration_number"],
                    "phone": contractor["phone"],
                    "address": contractor["location"],
                    "specialization": contractor["specialization"],
                    "experience_years": contractor["experience_years"],
                    "status": ContractorProfile.Status.APPROVED,
                },
            )

            if user_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(CONTRACTORS)} contractors ({created} created, {updated} updated)."
            )
        )
