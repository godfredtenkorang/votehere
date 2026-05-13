from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Category, CategoryUpdate

@receiver(pre_save, sender=Category)
def create_category_update_on_status_change(sender, instance, **kwargs):
    if instance.pk:  # Check if the category already exists (is being updated)
        old = Category.objects.get(pk=instance.pk)
        # Check if end_date changed
        if old.end_date != instance.end_date and instance.end_date:
            CategoryUpdate.objects.create(
                category=instance, 
                message=f"Voting deadline for {instance.award} has been updated to {instance.end_date}. Please vote before the new deadline.", 
                update_type='info'
            )
