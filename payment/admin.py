from django.contrib import admin
from .models import Payment, Nominees, PageExpiration, RequestForPayment

# admin.site.register(Payment)
# admin.site.register(Nominees)

# @admin.register(Nominees)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ['category', 'sub_category', 'name', 'image', 'slug', 'total_vote']
    


# @admin.register(Payment)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ['nominee', 'name', 'email', 'phone',
#                     'amount', 'total_amount', 'vote', 'ref', 'verified', 'date_created']
    
# class NomineesInline(admin.TabularInline):
#     model = Payment

# @admin.register(Nominees)
# class PaymentAdmin(admin.ModelAdmin):
#     inlines = [
#         NomineesInline,
#     ]
class PaymentInLine(admin.TabularInline):
    model = Payment
    extra = 3
    exclude = ('amount',)
  
  
class VoteNomineeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['category', 'sub_category', 'name', 'image', 'slug', 'total_vote', 'can_vote', 'can_see_result', 'price_per_vote', 'code', 'access_code', 'phone_number']}), ('Date Information', {
        'fields': ['date_added', 'end_date'], }), ]
    inlines = [PaymentInLine]
    list_display = ['category', 'sub_category', 'name', 'total_vote', 'code', 'access_code', 'phone_number']
    list_filter = ('category', 'sub_category')
    search_fields = ('name', 'code')
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(Nominees, VoteNomineeAdmin)



admin.site.register(PageExpiration)


@admin.register(RequestForPayment)
class RequestForPaymentAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'phone', 'email', 'amount', 'date_requested']
    list_filter = ('category',)
    search_fields = ('phone', 'category')