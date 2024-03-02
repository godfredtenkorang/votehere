from django.urls import path
from . import views


urlpatterns = [
    path('nominate/<slug:nominate_slug>/', views.nominate, name='nominate'),
]
