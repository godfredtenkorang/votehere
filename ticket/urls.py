from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.ticketing, name='ticketing'),
    path('purchase_ticket/<slug:event_slug>/', views.purchase_ticket, name='ticketForm'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
    path('payment-success/', views.ticket_success, name='ticket_success'),
    path('payment-failed/', views.ticket_failed, name='ticket_failed'),
]