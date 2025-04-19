from django.db import models
import secrets
from .paystack import PayStack
from ussd.models import PaymentTransaction

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    ticket_image = models.ImageField(upload_to='ticket_img/', default='')
    date_added = models.DateTimeField()
    end_date = models.DateTimeField()
    available = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class TicketPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveBigIntegerField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    

    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return self.event.name
        
       
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = TicketPayment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount * 100
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


class SMSLog(models.Model):
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20)  # sent, delivered, failed
    transaction = models.ForeignKey(PaymentTransaction, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    
    def __str__(self):
        self.phone_number