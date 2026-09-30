from django.core.management.base import BaseCommand

from website.models import Service, ServicePackage


class Command(BaseCommand):
    help = "Create MJ Technologies services and packages"

    def handle(self, *args, **options):

        service_name = "Website & Software Development"

        service_description = (
            "Professional website and software development "
            "solutions for businesses, organizations and individuals."
        )

        # Get all existing services with this name
        services = Service.objects.filter(name=service_name).order_by("id")

        # If none exists, create one
        if not services.exists():
            service = Service.objects.create(
                name=service_name,
                description=service_description,
                active=True,
                order=1,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created service: {service.name}"
                )
            )

        else:
            # Keep the first service
            service = services.first()

            # Remove duplicate services
            duplicates = services.exclude(id=service.id)

            duplicate_count = duplicates.count()

            if duplicate_count > 0:
                duplicates.delete()

                self.stdout.write(
                    self.style.WARNING(
                        f"Removed {duplicate_count} duplicate service(s)."
                    )
                )

            # Update the main service
            service.description = service_description
            service.active = True
            service.order = 1
            service.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Using service: {service.name}"
                )
            )

        # Packages
        packages = [
            {
                "name": "Basic Website",
                "price": 300000,
                "description": (
                    "A professional website for individuals "
                    "and small businesses."
                ),
                "features": (
                    "Professional responsive design\n"
                    "Up to 5 pages\n"
                    "Mobile friendly\n"
                    "Contact form\n"
                    "WhatsApp integration"
                ),
                "order": 1,
            },
            {
                "name": "Business Website",
                "price": 200000,
                "description": (
                    "A modern business website designed "
                    "to establish a strong online presence."
                ),
                "features": (
                    "Professional responsive design\n"
                    "Up to 10 pages\n"
                    "Mobile friendly\n"
                    "Contact form\n"
                    "WhatsApp integration\n"
                    "Social media integration"
                ),
                "order": 2,
            },
            {
                "name": "Premium Website",
                "price": 400000,
                "description": (
                    "Advanced website solution for businesses "
                    "that need more functionality."
                ),
                "features": (
                    "Premium responsive design\n"
                    "Up to 15 pages\n"
                    "Mobile friendly\n"
                    "Advanced contact forms\n"
                    "WhatsApp integration\n"
                    "Social media integration\n"
                    "Advanced functionality"
                ),
                "order": 3,
            },
        ]

        for package_data in packages:

            existing_packages = ServicePackage.objects.filter(
                service=service,
                name=package_data["name"]
            ).order_by("id")

            if existing_packages.exists():

                package = existing_packages.first()

                duplicate_packages = existing_packages.exclude(
                    id=package.id
                )

                duplicate_count = duplicate_packages.count()

                if duplicate_count > 0:
                    duplicate_packages.delete()

                package.description = package_data["description"]
                package.price = package_data["price"]
                package.features = package_data["features"]
                package.active = True
                package.order = package_data["order"]
                package.save()

                self.stdout.write(
                    self.style.WARNING(
                        f"Updated package: {package.name} "
                        f"- TSh {package.price:,.0f}"
                    )
                )

            else:

                package = ServicePackage.objects.create(
                    service=service,
                    name=package_data["name"],
                    description=package_data["description"],
                    price=package_data["price"],
                    features=package_data["features"],
                    active=True,
                    order=package_data["order"],
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created package: {package.name} "
                        f"- TSh {package.price:,.0f}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "MJ Technologies services and packages "
                "are ready successfully!"
            )
        )