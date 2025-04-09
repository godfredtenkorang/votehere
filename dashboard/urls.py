from django.urls import path
from . import views

from .views import GeneratePdf


urlpatterns = [
    # Activities
    path('admin/', views.admin, name='adminPage'),
    path('activity-category/<slug:category_slug>/', views.activity_category, name='activity_category'),
    path('activity-nominee/<slug:nominee_slug>/', views.activity_nominee, name='activity_nominee'),
    
    # Registration
    path('registration/', views.registration, name='registration'),
    path('registration-category/', views.registration_category, name='registration_category'),
    path('registration-nominee/<slug:register_slug>/', views.registration_nominee, name='registration_nominee'),
    
    # Transaction
    path('transaction/<slug:nominee_slug>/', views.transaction, name='transaction'),

    path('transaction-category/<slug:transaction_slug>/', views.transaction_category, name='transaction_category'),

    path('team/', views.team, name='team'),

    path('transaction-category/<slug:transaction_slug>/', views.transaction_category, name='transaction_category'),
    path('adminHome/', views.adminHome, name='adminHome'),
    path('TransactionMain/', views.TransactionMain, name='TransactionMain'),
    path('ussd_transactions/<int:category_id>/', views.ussd_transactions, name='ussd_transactions'),
    path('TransactionCat/<slug:category_slug>/', views.TransactionCat, name='TransactionCat'),

    # PDF
    path('generate/<pdf>/', views.generate, name='generate'),
    path('pdf/<form>/', GeneratePdf.as_view(), name='pdf'),
    
    
    path('add_nominee/', views.add_nominee, name='add_nominee'),
    path('sms/', views.send_sms, name='send_sms'),
]
