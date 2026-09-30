from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse

from .forms import BookingForm
from .models import Service, ServicePackage


def home(request):
    services = Service.objects.filter(
        active=True
    ).prefetch_related("packages")

    return render(
        request,
        "home.html",
        {
            "services": services,
        }
    )


def pricing(request):
    services = Service.objects.filter(
        active=True
    ).prefetch_related("packages")

    return render(
        request,
        "pricing.html",
        {
            "services": services,
        }
    )


def service_packages(request):
    service_name = request.GET.get("service", "").strip()

    packages = ServicePackage.objects.filter(
        active=True,
        service__name=service_name
    ).order_by(
        "order",
        "price"
    )

    data = [
        {
            "id": package.id,
            "name": package.name,
            "price": str(package.price),
        }
        for package in packages
    ]

    return JsonResponse(
        {
            "packages": data
        }
    )


def book_service(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save()

            send_mail(
                f"Booking Confirmation - {booking.booking_number}",

                f"""
Hello {booking.customer_name},

Thank you for booking a service with MJ TECHNOLOGIES AND BUSINESS GROUP LTD.

Your booking has been received successfully.

Booking Number: {booking.booking_number}
Service: {booking.service}
Package: {booking.service_package if booking.service_package else "Not specified"}
Date: {booking.booking_date}
Time: {booking.booking_time}
Status: {booking.status}

We will contact you to confirm your booking.

MJ TECHNOLOGIES AND BUSINESS GROUP LTD
HOME OF EXCELLENCE

Phone: +255 789 104 216
WhatsApp: +255 789 104 216
Email: mjtechnologies51@gmail.com

Thank you for choosing MJ Technologies.
""",

                "mjtechnologies51@gmail.com",

                [booking.email],
            )

            return redirect(
                "booking_success",
                booking_number=booking.booking_number
            )

    else:

        package_id = request.GET.get("package")

        if package_id:

            try:

                package = ServicePackage.objects.get(
                    id=package_id,
                    active=True
                )

                form = BookingForm(
                    initial={
                        "service": package.service.name,
                        "service_package": package.id,
                    }
                )

            except ServicePackage.DoesNotExist:

                form = BookingForm()

        else:

            form = BookingForm()

    return render(
        request,
        "booking.html",
        {
            "form": form,
        }
    )


def booking_success(request, booking_number):

    return render(
        request,
        "booking_success.html",
        {
            "booking_number": booking_number
        }
    )