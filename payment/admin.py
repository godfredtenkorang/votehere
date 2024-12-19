from django.contrib import admin
from .models import Payment, Nominees, PageExpiration

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
    fieldsets = [(None, {'fields': ['category', 'sub_category', 'name', 'image', 'slug', 'total_vote', 'can_vote', 'can_see_result', 'code']}), ('Date Information', {
        'fields': ['date_added', 'end_date'], 'classes': ['collapse']}), ]
    inlines = [PaymentInLine]
    prepopulated_fields = {"slug": ("name",)}
  
  
admin.site.register(Nominees, VoteNomineeAdmin)



admin.site.register(PageExpiration)