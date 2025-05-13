from django.db import models
import uuid
from vote.models import Category

class CustomSession(models.Model):
    SESSION_TYPES = (
        ('VOTE', 'Vote'),
        ('TICKET', 'Ticket'),
    )
    msisdn = models.CharField(max_length=15, null=True, blank=True)
    session_key = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=100)
    level = models.CharField(max_length=100, null=True, blank=True)
    candidate_id = models.CharField(max_length=100, null=True, blank=True)
    event_id = models.CharField(max_length=10, null=True, blank=True) # New
    votes = models.IntegerField(null=True, blank=True)
    tickets = models.PositiveIntegerField(null=True, blank=True) # New
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='VOTE')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # Add any other fields you need to track
    
    def __str__(self):
        return f"{self.session_key} - {self.candidate_id} - {self.msisdn} - {self.order_id}"
    

class PaymentTransaction(models.Model):
    PAYMENT_TYPES = (
        ('VOTE', 'Vote'),
        ('TICKET', 'Ticket'),
    )
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50) 
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, null=True, blank=True) # new
    nominee_code = models.CharField(max_length=10, null=True, blank=True)
    event_code = models.CharField(max_length=10, null=True, blank=True) # new
    votes = models.IntegerField(null=True, blank=True)
    tickets = models.PositiveIntegerField(null=True, blank=True) # new
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='paymenttransactions')
    timestamp = models.DateTimeField(null=True, blank=True)  # To store the timestamp of the transaction
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.order_id} {self.payment_type} - {self.status} - {self.category} - {self.nominee_code}"