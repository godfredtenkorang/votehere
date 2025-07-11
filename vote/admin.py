from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Category)
# admin.site.register(SubCategory)


class SubCategoryInline(admin.TabularInline):  # or admin.StackedInline
    model = SubCategory
    extra = 0  # Number of empty forms to display

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('award', 'title', 'date_added', 'end_date')
    inlines = [SubCategoryInline]
    prepopulated_fields = {'slug': ('award',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', 'date', 'can_check_result')
    list_filter = ('category', 'can_check_result')
    list_editable = ('can_check_result',)
    actions = ['can_check_result']
    prepopulated_fields = {'slug': ('content',)}


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_added', 'blog_recommended')
    list_filter = ('date_added', 'blog_recommended')
    search_fields = ('title', 'content', 'content1', 'content2', 'content3', 'content4', 'content5')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog, BlogAdmin)