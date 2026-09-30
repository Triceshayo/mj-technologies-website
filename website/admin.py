from django.contrib import admin
from .models import Booking, Service, ServicePackage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
        "order",
        "created_at",
    )

    list_filter = (
        "active",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "order",
        "name",
    )


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service",
        "price",
        "active",
        "order",
        "created_at",
    )

    list_filter = (
        "service",
        "active",
    )

    search_fields = (
        "name",
        "service__name",
        "description",
    )

    ordering = (
        "service",
        "order",
        "price",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_number",
        "customer_name",
        "phone",
        "service",
        "service_package",
        "booking_date",
        "booking_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "service",
        "booking_date",
    )

    search_fields = (
        "booking_number",
        "customer_name",
        "phone",
        "email",
        "company_name",
        "service_package__name",
    )

    readonly_fields = (
        "booking_number",
        "created_at",
    )

    ordering = (
        "-created_at",
    )