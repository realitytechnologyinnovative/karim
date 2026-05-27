from django.core.management.base import BaseCommand

from apps.projects.models import Project
from apps.services.models import Service


class Command(BaseCommand):
    help = "Seed demo content (services and projects)."

    def handle(self, *args, **options):
        services_data = [
            (
                "Environmental & Social Impact Assessment (ESIA)",
                "esia",
                "Integrated impact assessment aligning with lender safeguards and national regulations.",
                1,
            ),
            (
                "Environmental Impact Assessment (EIA)",
                "eia",
                "Focused technical studies for emissions, noise, water, waste, and ecological receptors.",
                2,
            ),
            (
                "Resettlement Action Plan (RAP)",
                "rap",
                "Census, asset valuation, eligibility frameworks, and implementation monitoring.",
                3,
            ),
            (
                "Environmental & Social Management Plan (ESMP)",
                "esmp",
                "Mitigation measures, monitoring indicators, reporting rhythms, and training.",
                4,
            ),
        ]
        for title, slug, desc, order in services_data:
            Service.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": desc,
                    "sort_order": order,
                    "is_published": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Services seeded."))

        projects_data = [
            (
                "Lagos corridor rapid transit — ESIA",
                "lagos-corridor-transit-esia",
                "Baseline ecology and social surveys for a BRT corridor, including air quality modelling and stakeholder engagement plan.",
                "Lagos, Nigeria",
                2024,
            ),
            (
                "Port berth expansion — EIA & marine monitoring",
                "port-berth-expansion-eia",
                "Hydrodynamic considerations, sediment quality, and construction-phase environmental monitoring.",
                "Rivers State, Nigeria",
                2023,
            ),
            (
                "Solar farm cluster — ESMP",
                "solar-farm-cluster-esmp",
                "Operational ESMP with biodiversity offsets checklist and grievance mechanism design.",
                "Northern Nigeria",
                2025,
            ),
            (
                "Agro-processing hub — RAP",
                "agro-processing-hub-rap",
                "Land take inventory, livelihood restoration, and community development priorities.",
                "Kaduna, Nigeria",
                2022,
            ),
        ]
        for title, slug, desc, loc, year in projects_data:
            Project.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": desc,
                    "location": loc,
                    "year": year,
                    "is_published": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Projects seeded."))
