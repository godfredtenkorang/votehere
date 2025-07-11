import secrets
from django.db import models
import uuid
from vote.models import Category
from django.utils import timezone
from ticket.models import Event

class CustomSession(models.Model):
    SESSION_TYPES = (
        ('VOTE', 'Vote'),
        ('TICKET', 'Ticket'),
        ('DONATION', 'Donation'),
    )
    msisdn = models.CharField(max_length=15, null=True, blank=True)
    session_key = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=100)
    level = models.CharField(max_length=100, null=True, blank=True)
    candidate_id = models.CharField(max_length=100, null=True, blank=True)
    ticket_type_id = models.CharField(max_length=100, null=True, blank=True) # New
    event_id = models.CharField(max_length=10, null=True, blank=True) # New
    donation_id = models.CharField(max_length=10, blank=True, null=True)
    votes = models.IntegerField(null=True, blank=True)
    tickets = models.PositiveIntegerField(null=True, blank=True) # New
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='VOTE') # New
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # Add any other fields you need to track
    
    @property
    def is_expired(self):
        
        return (timezone.now() - self.last_activity).total_seconds() > 75
    
    def __str__(self):
        return f"{self.session_key} - {self.candidate_id} - {self.event_id} - {self.msisdn} - {self.order_id}"
    

class PaymentTransaction(models.Model):
    PAYMENT_TYPES = (
        ('VOTE', 'Vote'),
        ('TICKET', 'Ticket'),
        ('DONATION', 'Donation'),
    )
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)  # New field
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50) 
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, null=True, blank=True) # new
    
    # Vote-specific fields
    nominee_code = models.CharField(max_length=10, null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='paymenttransactions')
    
    # Ticket-specific fields
    event_code = models.CharField(max_length=10, null=True, blank=True) # new
    tickets = models.PositiveIntegerField(null=True, blank=True) # new
    ticket_type = models.CharField(max_length=20, null=True, blank=True) # new
    event_category = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='paymenttransactions')
    
    # Donation-specific fields
    donation_code = models.CharField(max_length=10, null=True, blank=True) # New
    
    timestamp = models.DateTimeField(null=True, blank=True)  # To store the timestamp of the transaction
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __str__(self):
        return f"Transaction {self.order_id} {self.payment_type} - {self.status} - {self.category} - {self.nominee_code} - {self.timestamp}"


class SMSLog(models.Model):
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20)  # sent, delivered, failed
    transaction = models.ForeignKey(PaymentTransaction, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    
    def __str__(self):
        self.phone_number