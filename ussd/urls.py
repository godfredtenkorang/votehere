from django.urls import path
from . import views
from .views import AystackWebhookView

urlpatterns = [
    path('ussd/', views.ussd_api, name='ussd'),
    path('webhooks/heroku/', views.heroku_webhook, name='heroku_webhook'),
    
]
