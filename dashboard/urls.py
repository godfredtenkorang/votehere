from django.urls import path
from . import views

from .views import GeneratePdf, GetSubCategoriesView


urlpatterns = [
    # Activities
    path('admin/', views.admin, name='adminPage'),
    path('access-award/', views.access_award_by_code, name='access_award_by_code'),
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
    path('access-award-transactions/', views.access_transaction_by_code, name='access_transaction_by_code'),
    path('ussd_transactions/<int:category_id>/', views.ussd_transactions, name='ussd_transactions'),
    path('online_transactions/<int:category_id>/', views.online_transactions, name='online_transactions'),
    path('TransactionCat/<slug:category_slug>/', views.TransactionCat, name='TransactionCat'),

    # PDF
    path('generate/<pdf>/', views.generate, name='generate'),
    path('pdf/<form>/', GeneratePdf.as_view(), name='pdf'),
    
    
    path('add_nominee/', views.add_nominee, name='add_nominee'),
    path('get_subcategories/', GetSubCategoriesView.as_view(), name='get_subcategories'),
    path('sms/', views.send_sms, name='send_sms'),
    path('send-category-sms/', views.send_sms_to_nominees, name='send_category_sms'),
    path('award_revenue_insight/<int:subcategory_id>/', views.award_revenue_insight, name='award_revenue_insight'),
    
    path('get_all_categories/', views.get_all_categories, name='get_all_categories'),
    path('get_all_nominees/<slug:category_slug>/', views.get_nominee_by_category, name='get_nominee_by_category'),
    path('update_nominee/<slug:nominee_slug>/', views.update_nominee_by_category, name='update_nominee'),
    
    path('payment-transactions/', views.payment_transactions, name='payment_transactions'),
    path('payment-transactions/<int:invoice_id>/', views.payment_transactions_detail, name='update_transaction'),
    


     path('accessTicket/', views.accessTicket, name='accessTicket'),
     path('ticketActivity/<slug:event_slug>/', views.ticketActivity, name='ticketActivity'),
     path('onlineTransaction/', views.onlineTransaction, name='onlineTransaction'),
     path('ussdTransaction/', views.ussdTransaction, name='ussdTransaction'),
   
]
