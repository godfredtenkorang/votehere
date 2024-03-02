from django.db import models
from vote.models import Category
from django.utils import timezone


class Register(models.Model):
    award = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='register_img')
    category = models.CharField(max_length=250)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    content = models.TextField(null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "register"
        
    def __str__(self):
        return self.name
