from django.urls import path
from vote.api import views


urlpatterns = [
    path('', views.category_view)
]