from django.db import models

# Create your models here.

class Main_Category(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    image= models.ImageField(upload_to="main_category")
    
    class Meta:
        verbose_name_plural = "main categories"

    def __str__(self):
        return self.name
    
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    image = models.ImageField(upload_to="main_category")
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class Nominees(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    image = models.ImageField(upload_to="main_category")

    class Meta:
        verbose_name_plural = "nominees"

    def __str__(self):
        return self.name
