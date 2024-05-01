from django.urls import path
from . import views


urlpatterns = [
    # Activities
    path('adminPage/', views.admin, name='adminPage'),
    path('activity-category/', views.activity_category, name='activity_category'),
    path('activity-nominee/', views.activity_nominee, name='activity_nominee'),
    
    # Registration
    path('registration/', views.registration, name='registration'),
    path('registration-category/', views.registration_category, name='registration_category'),
    path('registration-nominee/', views.registration_nominee, name='registration_nominee'),
    
    # Transaction
    path('transaction/', views.transaction, name='transaction'),
    path('transaction-category/', views.transaction_category, name='transaction_category'),
]
