from django.contrib import admin
from .models import CustomSession, PaymentTransaction, Faculty, Department, LevelDues, StudentDuesPayment

# Register your models here.
admin.site.register(CustomSession)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(LevelDues)
admin.site.register(StudentDuesPayment)

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'amount', 'status', 'payment_type', 'nominee_code', 'event_code', 'donation_code', 'votes', 'tickets', 'category', 'timestamp']
    list_filter = ('category', 'event_category', 'nominee_code', 'payment_type')