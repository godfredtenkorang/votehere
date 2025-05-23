from django.contrib import admin
from .models import Event, TicketPayment, TicketType

# Register your models here.


class PaymentInLine(admin.TabularInline):
    model = TicketPayment
    extra = 3
    exclude = ('amount',)
  
  
class VoteNomineeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'code', 'description', 'access_code', 'ticket_image', 'date_added', 'end_date', 'available', 'slug']}), ]
    inlines = [PaymentInLine]
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(Event, VoteNomineeAdmin)
admin.site.register(TicketType)


