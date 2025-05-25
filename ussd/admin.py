from django.contrib import admin
from .models import CustomSession, PaymentTransaction

# Register your models here.
admin.site.register(CustomSession)

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'amount', 'status', 'payment_type', 'nominee_code', 'event_code', 'votes', 'tickets', 'category', 'timestamp']
    list_filter = ('category', 'event_category', 'nominee_code', 'payment_type')