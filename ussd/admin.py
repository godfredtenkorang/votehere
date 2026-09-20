from django.contrib import admin
from .models import CustomSession, PaymentTransaction, Faculty, Department, LevelDues, StudentDuesPayment

# Register your models here.

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['code']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['code', 'name']
    ordering = ['name']

@admin.register(LevelDues)
class LevelDuesAdmin(admin.ModelAdmin):
    list_display = ['department', 'level', 'amount', 'academic_year', 'is_active']
    list_filter = ['department', 'level', 'academic_year', 'is_active']
    search_fields = ['department__name', 'department__code']
    ordering = ['department', 'level']

@admin.register(CustomSession)
class CustomSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'user_id', 'payment_type', 'level', 'last_activity', 'is_expired']
    list_filter = ['payment_type', 'level']
    search_fields = ['session_key', 'user_id', 'msisdn']
    readonly_fields = ['created_at', 'last_activity']
    ordering = ['-last_activity']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'amount', 'status', 'payment_type', 'nominee_code', 'event_code', 'donation_code', 'votes', 'tickets', 'category', 'timestamp']
    list_filter = ('category', 'event_category', 'nominee_code', 'payment_type')