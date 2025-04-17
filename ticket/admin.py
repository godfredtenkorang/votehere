from django.contrib import admin
from .models import Event, TicketPayment

# Register your models here.


class PaymentInLine(admin.TabularInline):
    model = TicketPayment
    extra = 3
    exclude = ('amount',)
  
  
class VoteNomineeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'code', 'price', 'description', 'total_tickets', 'available_tickets', 'ticket_image', 'date_added', 'end_date', 'available', 'slug']}), ]
    inlines = [PaymentInLine]
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(Event, VoteNomineeAdmin)
