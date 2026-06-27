from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from procurement.models import AdminProfile, Tender, User


TENDERS = [
    {
        "title": "Construction of 50-Bed District Hospital",
        "procuring_entity": "Ministry of Health, Ghana",
        "category": Tender.Category.CONSTRUCTION,
        "location": "Nsawam, Eastern Region",
        "budget_min": Decimal("15000000.00"),
        "budget_max": Decimal("20000000.00"),
        "deadline": "2026-08-15 17:00",
        "scope": (
            "Full structural construction, plumbing, electrical wiring, and landscaping "
            "for a modern 50-bed healthcare facility. Includes the construction of an "
            "administrative block, OPD, surgical theater, and a small staff quarters."
        ),
    },
    {
        "title": "Supply and Installation of Enterprise Server Infrastructure",
        "procuring_entity": "National Identification Authority (NIA)",
        "category": Tender.Category.OTHER,
        "location": "Accra, Greater Accra",
        "budget_min": Decimal("2500000.00"),
        "budget_max": Decimal("3200000.00"),
        "deadline": "2026-07-30 17:00",
        "scope": (
            "Procurement, delivery, and installation of 15 high-performance enterprise "
            "blade servers, UPS backup systems, and associated networking switches. "
            "The winning contractor must provide a 2-year warranty and quarterly "
            "maintenance."
        ),
    },
    {
        "title": "Rehabilitation and Tarring of Feeder Roads (25km)",
        "procuring_entity": "Department of Feeder Roads",
        "category": Tender.Category.INFRASTRUCTURE,
        "location": "Sunyani, Bono Region",
        "budget_min": Decimal("8000000.00"),
        "budget_max": Decimal("12000000.00"),
        "deadline": "2026-08-05 17:00",
        "scope": (
            "Grading, base laying, and bitumen surfacing of 25 kilometers of rural "
            "feeder roads to facilitate the transportation of agricultural produce. "
            "Includes the construction of 4 concrete culverts for drainage."
        ),
    },
    {
        "title": "Procurement of 30 Heavy-Duty Agricultural Tractors",
        "procuring_entity": "Ministry of Food and Agriculture",
        "category": Tender.Category.OTHER,
        "location": "Tamale, Northern Region",
        "budget_min": Decimal("4500000.00"),
        "budget_max": Decimal("5500000.00"),
        "deadline": "2026-07-20 17:00",
        "scope": (
            "Supply and delivery of 30 brand-new 75HP 4WD agricultural tractors with "
            "matching implements, including ploughs and harrows. Supplier must offer "
            "operator training and an initial supply of fast-moving spare parts."
        ),
    },
    {
        "title": "Annual Security and Janitorial Services Contract",
        "procuring_entity": "Ghana Revenue Authority (GRA)",
        "category": Tender.Category.OTHER,
        "location": "National Headquarters, Accra",
        "budget_min": Decimal("1200000.00"),
        "budget_max": Decimal("1200000.00"),
        "deadline": "2026-07-25 17:00",
        "scope": (
            "Provision of 24/7 armed and unarmed security personnel, comprehensive CCTV "
            "monitoring, and daily janitorial/cleaning services for a 10-story corporate "
            "headquarters complex. Contract duration is 24 months, renewable based on "
            "performance."
        ),
    },
    {
        "title": "Off-Grid Solar Power Electrification for Rural Schools",
        "procuring_entity": "Ministry of Education",
        "category": Tender.Category.ELECTRICAL,
        "location": "Various districts in the Upper West Region",
        "budget_min": Decimal("3000000.00"),
        "budget_max": Decimal("3800000.00"),
        "deadline": "2026-08-10 17:00",
        "scope": (
            "Design, supply, and installation of 10kW off-grid solar PV systems complete "
            "with lithium-ion battery storage banks for 15 selected rural basic schools. "
            "The project includes wiring the classrooms and installing energy-efficient "
            "LED lighting."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the database with realistic open tender test postings."

    def handle(self, *args, **options):
        admin_profile = self.get_or_create_admin_profile()
        created = 0
        updated = 0

        for tender in TENDERS:
            deadline = timezone.make_aware(
                datetime.strptime(tender["deadline"], "%Y-%m-%d %H:%M")
            )
            description = (
                f"Procuring Entity: {tender['procuring_entity']}\n\n"
                f"Scope of Work: {tender['scope']}"
            )
            _, was_created = Tender.objects.update_or_create(
                title=tender["title"],
                defaults={
                    "admin": admin_profile,
                    "description": description,
                    "location": tender["location"],
                    "budget_min": tender["budget_min"],
                    "budget_max": tender["budget_max"],
                    "category": tender["category"],
                    "deadline": deadline,
                    "status": Tender.Status.OPEN,
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(TENDERS)} tenders ({created} created, {updated} updated)."
            )
        )

    def get_or_create_admin_profile(self):
        admin_user = User.objects.filter(role=User.Role.ADMIN).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                email="admin@procurepro.com",
                password="adminpassword",
            )

        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = User.Role.ADMIN
        admin_user.save()

        admin_profile, _ = AdminProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                "name": "ProcurePro Admin",
                "department": "Central Procurement",
            },
        )
        return admin_profile
