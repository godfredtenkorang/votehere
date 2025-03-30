from django.db import models

# Create your models here.
class SendSms(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, default='')
    category = models.CharField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name