from django.db import models
import uuid

class CustomSession(models.Model):
    session_key = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=100)
    level = models.CharField(max_length=100, null=True, blank=True)
    candidate_id = models.CharField(max_length=100, null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Add any other fields you need to track
    
    def __str__(self):
        return self.session_key
    

class PaymentTransaction(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    msisdn = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transaction {self.order_id} - {self.status}"