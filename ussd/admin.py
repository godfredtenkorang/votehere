from django.contrib import admin
from .models import CustomSession, PaymentTransaction

# Register your models here.
admin.site.register(CustomSession)
admin.site.register(PaymentTransaction)