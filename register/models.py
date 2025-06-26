from django.db import models
from vote.models import Category
from django.utils import timezone

CHOICES = (
    ("HARDWORKING YOUTH OF THE YEAR", "HARDWORKING YOUTH OF THE YEAR"),
    ("FASHION ICON OF THE YEAR", "FASHION ICON OF THE YEAR"),
    ("CONTENT CREATOR OF THE YEAR", "CONTENT CREATOR OF THE YEAR"),
    ("ENTREPRENEUR OF THE YEAR", "ENTREPRENEUR OF THE YEAR"),
    ("SOCIAL MEDIA INFLUENCER OF THE YEAR", "SOCIAL MEDIA INFLUENCER OF THE YEAR"),
    ("IDLE LADY OF THE YEAR", "IDLE LADY OF THE YEAR"),
    ("GENTLEMAN OF THE YEAR", "GENTLEMAN OF THE YEAR"),
    ("DANCER OF THE YEAR", "DANCER OF THE YEAR"),
    ("ACTOR OF THE YEAR", "ACTOR OF THE YEAR"),
    ("MOVIE STAR OF THE YEAR", "MOVIE STAR OF THE YEAR"),
    ("MUSIC ARTIST OF THE YEAR", "MUSIC ARTIST OF THE YEAR"),
)


class Register(models.Model):
    award = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='profile.png', upload_to='register_img')
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    content = models.TextField(null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "register"
        
    def __str__(self):
        return self.name

class EventOrganizer(models.Model):
    EVENT_TYPES = [
        ('REALITY', 'Reality Show'),
        ('AWARDS', 'Awards'),
        ('ELECTIONS', 'Elections'),
        ('QUIZ', 'Quiz'),
        ('OTHER', 'Other'),
    ]
    
    event_name = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    event_description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    promo_code = models.CharField(max_length=50, blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.event_name} by {self.organization_name}"