from django.urls import path
from . import views


urlpatterns = [
    path('adminPage/', views.admin, name='adminPage'),
]
