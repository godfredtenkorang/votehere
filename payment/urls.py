from django.urls import path
from . import views


urlpatterns = [
    path('', views.make_payment, name='make-payment'),
    path('result/', views.result, name='result'),
    path('nominee/<slug:nominee_slug>/', views.nominees, name='nominee_detail'),
    path('make_payment/<str:ref>/',views.verify_payment, name='verify-payment')
]