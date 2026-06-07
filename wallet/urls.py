from . import views
from django.urls import path

urlpatterns = [
    path('top_up_guide/', views.top_up_guide, name='top_up_guide'),
    path('top_up/', views.top_up, name='top_up'),
    path('main_wallet/', views.main_wallet, name='main_wallet'),
    path('wallet_login/', views.wallet_login, name='wallet_login'),
]