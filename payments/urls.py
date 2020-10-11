from django.urls import path

from .views import stripePayment,charge

urlpatterns = [
    path('', stripePayment, name="pay"),
    path('charge', charge, name="charge")
]