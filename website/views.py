from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import BookingForm
from .models import Booking, Service, ServicePackage


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
    service_name = request.GET.get(
        "service",
        ""
    ).strip()

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


@staff_member_required
def admin_dashboard(request):

    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        status="Pending"
    ).count()

    confirmed_bookings = Booking.objects.filter(
        status="Confirmed"
    ).count()

    completed_bookings = Booking.objects.filter(
        status="Completed"
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status="Cancelled"
    ).count()

    total_services = Service.objects.filter(
        active=True
    ).count()

    total_packages = ServicePackage.objects.filter(
        active=True
    ).count()

    recent_bookings = (
        Booking.objects
        .select_related("service_package")
        .order_by("-created_at")[:10]
    )

    context = {
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_services": total_services,
        "total_packages": total_packages,
        "recent_bookings": recent_bookings,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )