from django.urls import path
from . import views


urlpatterns = [
    path('', views.make_payment, name='make-payment')
]