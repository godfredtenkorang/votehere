from django.urls import path
from . import views
from .views import AystackWebhookView

urlpatterns = [
    path('ussd/', views.ussd_api, name='ussd'),
    path('aystack/webhook/', AystackWebhookView.as_view(), name='aystack-webhook'),
    
]
