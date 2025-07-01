import random
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    award = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="category")
    slug = models.SlugField(unique=True)
    date_added = models.DateTimeField('date added', null=True)
    end_date = models.DateTimeField('end date', null=True)
    access_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    nomination_end_date = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.access_code:
            # Generate a random 6-digit code if none exists
            self.access_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ('-date_added',)

    def __str__(self):
        return self.award
    
    def get_absolute_url(self):
        return f"/category/{self.slug}"
    
    def get_cat_image(self):
        if self.image:
            return "https://voteafric.com/" + self.image.url
        return ''

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(timezone.now)
    can_check_result = models.BooleanField(default=False)  # Add this field
    
    class Meta:
        verbose_name_plural = "sub categories"
        ordering = ('-date',)

    def __str__(self):
        return self.content
    
    
    def get_absolute_url(self):
        return reverse('award_by_category', args=[self.id])
    
    def get_subcat_image(self):
        if self.image:
            return "https://voteafric.com/" + self.image.url
        return ''


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=250)
    image = models.ImageField(upload_to='blog-img')
    slug = models.SlugField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "blogs"
        ordering = ('-date_added',)

    def __str__(self):
        return self.title