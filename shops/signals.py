from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def product_save(sender, instance, created,**kwargs):
    if created:
        print(f'{instance} successfully created!')
    else:
        print(f'{instance} updated successfully!')


@receiver(post_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    print(f'{instance} successfully deleted!')