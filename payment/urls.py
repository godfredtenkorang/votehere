from django.urls import path
from . import views


urlpatterns = [
    path('', views.make_payment, name='make-payment'),
    path('result/<slug:result_slug>/', views.result, name='result'),
    path('nominee/<slug:nominee_slug>/', views.nominees, name='nominee_detail'),

    path('make_payment/<str:ref>/',views.verify_payment, name='verify-payment'),
    path('vote/<slug:nominee_slug>/', views.vote, name='vote-page'),
    
    path('vote_success/<slug:nominee_slug>/', views.vote_success, name='vote-success'),
    path('vote_failed/<slug:nominee_slug>/', views.vote_failed, name='vote-failed'),
    path('search-transaction/', views.search_transaction, name='search_transaction'),
    
    path('not_exist/', views.access_denied, name='access-denied'),
    path('result_denied/', views.result_denied, name='result-denied'),
]