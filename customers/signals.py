from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=Customer)
def customer_created(sender, instance, created, **kwargs):
    if created:
        print(f"{instance} successfully created!")
    else:
        print(f"{instance} successfully updated!")


@receiver(post_delete, sender=Customer)
def customer_deleted(sender, instance, **kwargs):
    print(f"{instance} successfully deleted!")