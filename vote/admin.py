from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Category)
# admin.site.register(SubCategory)


class NomineesInLine(admin.TabularInline):
    model = SubCategory
    extra = 3
    prepopulated_fields = {"slug": ("content",)}
    
  
  
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['award', 'title', 'image', 'slug',]}), ('Date Information', {
        'fields': ['date_added', 'end_date'], 'classes': ['collapse']}), ]
    inlines = [NomineesInLine]
    prepopulated_fields = {"slug": ("award",)}
  
  
admin.site.register(Category, CategoryAdmin)