from django.urls import path
from . import views


urlpatterns = [
    path('donation_causes/', views.donation_page, name='donation_page'),
    path('donation/<slug:donation_slug>/', views.donation_detail, name='donation_detail'),
    path('donation/make_payment/', views.make_payment, name='donation_make_payment'),
    path('donation/make_payment/<str:ref>/',views.verify_payment, name='donation-verify-payment'),
    # Add more paths as needed for donation-related views
]