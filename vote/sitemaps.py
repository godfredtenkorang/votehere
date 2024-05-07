from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, SubCategory


class StaticSitemap(Sitemap):
    def items(self):
        return ['index', 'about', 'policy', 'termsCondition', 'contact']
    
    def location(self, item):
        return reverse(item)
    
class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()
    
class SubcategorySitemap(Sitemap):
    def items(self):
        return SubCategory.objects.all()[:100]