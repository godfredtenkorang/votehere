from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('about/', views.about, name='about'),
   path('policy/', views.policy, name='policy'), 
   path('termsCondition/', views.termsCondition, name='termsCondition'), 
   path('contact/', views.contact, name='contact'), 
   path('nominees/', views.nominees, name='nominee'), 
   path('category/', views.category, name='category'), 
   path('nominate/', views.nominate, name='nominate'), 
   path('contact/', views.contact, name='contact'), 

]