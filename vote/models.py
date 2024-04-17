from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    award = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="category")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(timezone.now, null=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ('-date',)

    def __str__(self):
        return self.award
    # def get_absolute_url(self):
    #     return reverse('award:award_by_category', args=[self.slug])

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(timezone.now)
    
    class Meta:
        verbose_name_plural = "sub categories"
        ordering = ('-date',)

    def __str__(self):
        return self.content
    
