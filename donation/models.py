from django.db import models
import secrets
from .paystack import PayStack


class DonationCause(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='donation_img/', default='', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    end_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class DonationPayment(models.Model):
    donation = models.ForeignKey(DonationCause, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    email = models.EmailField(null=True, blank=True)
    amount = models.PositiveBigIntegerField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self):
        return self.donation.name
        
       
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = DonationPayment.objects.filter(ref=ref)
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
