from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Category)
# admin.site.register(SubCategory)


class NomineesInLine(admin.TabularInline):
    model = SubCategory
    extra = 3
    
  
  
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['award', 'title', 'image', 'slug',]}), ('Date Information', {
        'fields': ['date'], 'classes': ['collapse']}), ]
    inlines = [NomineesInLine]
  
  
admin.site.register(Category, CategoryAdmin)