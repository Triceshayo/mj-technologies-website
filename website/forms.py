from django import forms
from .models import Booking, ServicePackage


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "customer_name",
            "phone",
            "email",
            "company_name",
            "service",
            "service_package",
            "booking_date",
            "booking_time",
            "description",
        ]

        widgets = {
            "customer_name": forms.TextInput(attrs={
                "placeholder": "Your full name",
                "class": "form-control",
            }),

            "phone": forms.TextInput(attrs={
                "placeholder": "+255 XXX XXX XXX",
                "class": "form-control",
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "your@email.com",
                "class": "form-control",
            }),

            "company_name": forms.TextInput(attrs={
                "placeholder": "Company or business name (optional)",
                "class": "form-control",
            }),

            "service": forms.Select(attrs={
                "class": "form-control",
            }),

            "service_package": forms.Select(attrs={
                "class": "form-control",
            }),

            "booking_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),

            "booking_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control",
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "Tell us about the service you need...",
                "rows": 5,
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        packages = (
            ServicePackage.objects
            .filter(active=True)
            .select_related("service")
        )

        self.fields["service_package"].choices = [
            (
                package.id,
                f"{package.name} — TSh {package.price:,.0f}"
            )
            for package in packages
        ]

        self.fields["service_package"].label = "Service Package"

        self.fields["service_package"].required = False