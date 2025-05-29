# voting/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Election, Category, Candidate, Voter, Vote

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    show_change_link = True
    inlines = [CandidateInline]

class ElectionAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]
    list_display = ('name', 'election', 'order')
    list_filter = ('election',)
    ordering = ('election', 'order')

class VoterInline(admin.StackedInline):
    model = Voter
    can_delete = False
    verbose_name_plural = 'Voters'

class CustomUserAdmin(UserAdmin):
    inlines = (VoterInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Candidate)
admin.site.register(Vote)
