from django.db import models
import secrets
from .paystack import PayStack
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils import timezone

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
# Add these new fields for QR code functionality
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    qr_verified = models.BooleanField(default=False)
    qr_verification_date = models.DateTimeField(null=True, blank=True)
    qr_verification_token = models.CharField(max_length=100, null=True, blank=True)
    

    
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
                
        # Generate QR code if not already generated
        if not self.qr_verification_token:
            self.qr_verification_token = secrets.token_urlsafe(20)
            
        super().save(*args, **kwargs)
        
        if not self.qr_code:
            self.generate_qr_code()
            
    def generate_qr_code(self):
        if self.qr_verification_token:
            # Create QR code data - use a verification URL
            verification_url = f"https://voteafric.com/%2Fverify-ticket/{self.qr_verification_token}/"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(verification_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            # Save to model field
            filename = f'ticket_qr_{self.ref}.png'
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
            
            # Save the model again to store the QR code
            super().save(update_fields=['qr_code'])
        
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
    
    def verify_qr_code(self):
        """Verify the QR code and mark as scanned"""
        if self.qr_verified:
            return "already_scanned"
        
        self.qr_verified = True
        self.qr_verification_date = timezone.now()
        self.save()
        return "verified"


