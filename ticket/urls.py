from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.ticketing, name='ticketing'),
    path('ticketForm/', views.ticketForm, name='ticketForm')
]