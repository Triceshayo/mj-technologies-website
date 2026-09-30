from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class ServicePackage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    features = models.TextField(
        blank=True,
        help_text="Andika kila feature kwenye mstari mpya."
    )

    active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order", "price"]
        verbose_name = "Service Package"
        verbose_name_plural = "Service Packages"

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class Booking(models.Model):

    SERVICE_CHOICES = [
        (
            "Website & Software Development",
            "Website & Software Development"
        ),
        (
            "Online Applications & Digital Services",
            "Online Applications & Digital Services"
        ),
        (
            "Company Registration & Business Compliance",
            "Company Registration & Business Compliance"
        ),
        (
            "Graphic Design, Branding & Printing",
            "Graphic Design, Branding & Printing"
        ),
        (
            "Digital Marketing & Social Media",
            "Digital Marketing & Social Media"
        ),
        (
            "Business Consultancy & Development",
            "Business Consultancy & Development"
        ),
        (
            "Technology & Digital Solutions",
            "Technology & Digital Solutions"
        ),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    booking_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    company_name = models.CharField(
        max_length=150,
        blank=True
    )

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES
    )

    service_package = models.ForeignKey(
        ServicePackage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings"
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.booking_number:
            last_booking = Booking.objects.order_by("-id").first()

            if last_booking:
                last_number = last_booking.id + 1
            else:
                last_number = 1

            self.booking_number = f"MJT-{last_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_number} - {self.customer_name}"

# Create your models here.
