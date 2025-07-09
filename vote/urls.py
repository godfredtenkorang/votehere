from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    # path('blog-detail/<slug:blog_slug>/', views.blog_detail, name='blog-detail'),
    path('blog-detail/', views.blog_detail, name='blog-detail'),
    path('policy/', views.policy, name='policy'),
    path('terms_and_condition/', views.termsCondition, name='termsCondition'),
    path('contact/', views.contact, name='contact'),

    path('award/', views.award_page, name='award_page'),
    path('joinUs/', views.joinUs, name='joinUs'),
 

    path('<slug:category_slug>/', views.category, name='award_by_category'),



    path('search/<slug:category_slug>/',
         views.category_search_view, name='cat-search'),

    # path('search/<slug:category_slug>/',
    #      views.nominees_search_view, name='nom-search'),
    

  
] 

