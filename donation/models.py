from django.db import models


class DonationCause(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
