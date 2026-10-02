from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "pricing/",
        views.pricing,
        name="pricing",
    ),

    path(
        "book-service/",
        views.book_service,
        name="book_service",
    ),

    path(
        "service-packages/",
        views.service_packages,
        name="service_packages",
    ),

    path(
        "booking-success/<str:booking_number>/",
        views.booking_success,
        name="booking_success",
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),
]