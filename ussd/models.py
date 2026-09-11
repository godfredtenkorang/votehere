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
        ('DUES', 'Dues'),
    )
    session_key = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=100)
    msisdn = models.CharField(max_length=15, null=True, blank=True)
    level = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='VOTE') # New
    
    
    candidate_id = models.CharField(max_length=100, null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    event_id = models.CharField(max_length=10, null=True, blank=True) # New
    ticket_type_id = models.CharField(max_length=100, null=True, blank=True) # New
    tickets = models.PositiveIntegerField(null=True, blank=True) # New
    
    donation_id = models.CharField(max_length=10, blank=True, null=True)
    
    # Student dues fields
    faculty_code = models.CharField(max_length=20, blank=True, null=True)
    department_code = models.CharField(max_length=20, blank=True, null=True)
    department_name = models.CharField(max_length=100, blank=True, null=True)
    department_list = models.JSONField(default=list, blank=True, null=True)  # Store department codes as a list
    level_data = models.JSONField(default=list, blank=True, null=True)  # Store level data as a list of dictionaries
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    student_number = models.CharField(max_length=20, blank=True, null=True)
    dues_level = models.CharField(max_length=10, blank=True, null=True)
    dues_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dues_academic_year = models.CharField(max_length=20, blank=True, null=True)
    
    order_id = models.CharField(max_length=255, blank=True, null=True)
    nalo_order_id = models.CharField(max_length=100, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # Add any other fields you need to track
    
    @property
    def is_expired(self):
        
        return (timezone.now() - self.last_activity).total_seconds() > 75
    
    class Meta:
        indexes = [
            models.Index(fields=['order_id']),

        ]
    
    def __str__(self):
        return f"{self.session_key} - {self.candidate_id} - {self.event_id} - {self.msisdn} - {self.order_id}"
    

class PaymentTransaction(models.Model):
    PAYMENT_TYPES = (
        ('VOTE', 'Vote'),
        ('TICKET', 'Ticket'),
        ('DONATION', 'Donation'),
        ('DUES', 'Dues'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    order_id = models.CharField(max_length=255, primary_key=True)  # Unique order ID for each transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING') 
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, null=True, blank=True) # new
    
    
    invoice_no = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)  # New field
    
    # Additional fields for better tracking
    trans_hash = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    account_name = models.CharField(max_length=255, null=True, blank=True)
    
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
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['trans_hash']),
        ]
    
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
        
        
class Faculty(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class LevelDues(models.Model):
    LEVEL_CHOICES = [
        ('100', 'Level 100'),
        ('200', 'Level 200'),
        ('300', 'Level 300'),
        ('400', 'Level 400'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='level_dues')
    academic_year = models.CharField(max_length=20)  # e.g., "2024/2025"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['level', 'department', 'academic_year']

    def __str__(self):
        return f"{self.department.name} - {self.level} - {self.academic_year}"

class StudentDuesPayment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True)
    invoice_no = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    
    # Student details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_number = models.CharField(max_length=20)
    level = models.CharField(max_length=10)  # e.g., "100"
    
    # Faculty and department
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    level_dues = models.ForeignKey(LevelDues, on_delete=models.SET_NULL, null=True)
    
    # Payment details
    msisdn = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_number} - {self.first_name} {self.last_name}"