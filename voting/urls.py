from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.voter_login, name='vote-login'),
    path('logout/', views.voter_logout, name='vote-logout'),
    path('vote/<int:election_id>/', views.vote, name='voting'),
    path('results/<int:election_id>/', views.results, name='vote-results'),

]