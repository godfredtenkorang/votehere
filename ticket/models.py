from django.db import models
import secrets
from .paystack import PayStack

# Create your models here.




class Event(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    # total_tickets = models.PositiveIntegerField()
    # available_tickets = models.PositiveIntegerField()
    ticket_image = models.ImageField(upload_to='ticket_img/', default='')
    access_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    date_added = models.DateTimeField()
    end_date = models.DateTimeField()
    available = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)
    
    @property
    def total_tickets(self):
        return sum(ticket_type.total_tickets for ticket_type in self.ticket_types.all())
    
    @property
    def available_tickets(self):
        return sum(ticket_type.available_tickets for ticket_type in self.ticket_types.all())
    
    
    def __str__(self):
        return self.name
    
class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)  # e.g., "Single", "VIP", "Couple"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.event.name}"


class TicketPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.SET_NULL, null=True)
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


