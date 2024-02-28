from django.db import models

# Create your models here.

class Payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=14, null=True)
    amount = models.PositiveBigIntegerField()
    votes = models.IntegerField(default=0)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)