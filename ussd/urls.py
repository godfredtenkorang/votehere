from django.urls import path
from . import views

urlpatterns = [
    path('ussd', views.index, name='index'),
]
