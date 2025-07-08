from django.contrib import admin
from .models import DonationCause, DonationPayment

# Register your models here.
class PaymentInLine(admin.TabularInline):
    model = DonationPayment
    extra = 1
    
  
  
class DonationCauseAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'code', 'image', 'slug', 'description', 'target_amount', 'current_amount', 'end_date', 'active']}), ]
    inlines = [PaymentInLine]
    list_filter = ('name', 'code')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(DonationCause, DonationCauseAdmin)