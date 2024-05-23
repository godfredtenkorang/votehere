from django.urls import path
from . import views

urlpatterns = [
    path('ussd/', views.ussd_api, name='ussd'),
    path('callback/', views.payment_callback, name='payment_callback'),
]
