"""votehere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from vote.sitemaps import *
from django.views.generic.base import TemplateView

# Sitemaps
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticSitemap,
    'categories': CategorySitemap,
    'subcategorypages': SubcategorySitemap
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name="vote/robots.txt", content_type="text/plain")),
    path('voteafric_admin/', admin.site.urls),
    path('', include('vote.urls')),
    path('voting/', include('voting.urls')),
    path('payment/', include('payment.urls')),
    path('register/', include('register.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('maindashboard/', include('maindashboard.urls')),
    path('user/', include('user.urls')),
    path('ussd/', include('ussd.urls')),
    path('/', include('ticket.urls')),
    path('donation/', include('donation.urls')),
    path('api/vote/', include('vote.api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'vote.views.custom_404_view'