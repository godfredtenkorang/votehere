from django.urls import path
from . import views
from .views import GetSubCategoriesView

urlpatterns = [
    path('admin/', views.dashboard, name='main_dashboard'),
    path('add_nominee/', views.add_nominee, name='add_nominee'),
    path('get_subcategories/', GetSubCategoriesView.as_view(), name='get_subcategories'),
    path('sms/', views.send_sms, name='send_sms'),
    path('send-category-sms/', views.send_sms_to_nominees, name='send_category_sms'),
    path('send-access-code/', views.send_access_code_to_nominee, name='send_access_code'),
    
    path('get_all_categories/', views.get_all_categories, name='get_all_categories'),
    path('get_all_nominees/<slug:category_slug>/', views.get_nominee_by_category, name='get_nominee_by_category'),
    path('update_nominee/<slug:nominee_slug>/', views.update_nominee_by_category, name='update_nominee'),
    
    path('bulk_voting_transactions/<slug:category_slug>/', views.get_bulk_voting_transactions_by_category, name='bulk_voting_transactions'),
    
    path('payment-transactions/', views.payment_transactions, name='payment_transactions'),
    path('payment-transactions/<int:invoice_id>/', views.payment_transactions_detail, name='update_transaction'),
    
    path('filter_online_transactions/', views.filter_online_transactions, name='filter_online_transactions'),
    
    path('blog_list/', views.blog_list, name='blog_list'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('update_blog/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),

    path('receipt/', views.receipt, name='receipt'),
]