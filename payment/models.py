from django.db import models
from django.urls import reverse
from vote.models import SubCategory, Category
import secrets
from .paystack import PayStack

class Nominees(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="nominees")
    slug = models.SlugField(unique=True, null=True)
    total_vote = models.IntegerField(default=0, null=True)
    can_vote = models.BooleanField(default=True)
    can_see_result = models.BooleanField(default=True)
    date_added = models.DateTimeField('date added', null=True)
    end_date = models.DateTimeField('end date', null=True)

    class Meta:
        verbose_name_plural = "nominees"
        ordering = ('-total_vote',)

    def __str__(self):
        return f"{self.category} - {self.sub_category} - {self.name}"


class Payment(models.Model):
    nominee = models.ForeignKey(Nominees, on_delete=models.CASCADE, null=True)
    content = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=14, null=True)
    amount = models.PositiveBigIntegerField()
    total_amount = models.FloatField(null=True)
    vote = models.IntegerField(default=0)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_created',)
        
    def __str__(self) -> str:
        return f"Payment: {self.total_amount}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount * 1
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 1 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    # def get_absolute_url(self):
    #     return reverse("nominee_detail", kwargs={
    #         "ref": self.ref,
    #     })
