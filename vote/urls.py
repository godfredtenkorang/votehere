from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('policy/', views.policy, name='policy'),
    path('termsCondition/', views.termsCondition, name='termsCondition'),
    path('contact/', views.contact, name='contact'),

    path('<slug:category_slug>/', views.category, name='award_by_category'),



    path('search/<slug:category_slug>/',
         views.category_search_view, name='cat-search'),

    # path('search/<slug:category_slug>/',
    #      views.nominees_search_view, name='nom-search'),



]
