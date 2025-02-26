from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from User.models import User
from .models import Product
import json
from django.core.mail import EmailMessage

@receiver(post_save, sender=Product)
def product_save(sender, instance, created,**kwargs):
    if created:
        users = User.objects.all()
        email_of_users = [user.email for user in users]
        email =  EmailMessage(
            'Product Saved',
            f'{instance.name.title()} successfully created',
            to = email_of_users
        )
        email.send()

        email_admin = EmailMessage(
            'Create Product',
            f'{email_of_users}  successfully sent',
            to = ['aslanabdimuminov31@gmail.com']
        )
        email_admin.send()

    else:
        email_admin = EmailMessage(
            'Update Product',
            f'{instance}  successfully updated',
            to=['aslanabdimuminov31@gmail.com']
        )
        email_admin.send()

@receiver(post_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    email_admin = EmailMessage(
        'Deleted Product',
        f' {instance} successfully Deleted',
        to=['aslanabdimuminov31@gmail.com']
    )
    email_admin.send()

@receiver(pre_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    data = {
        f'{instance.id}': {
            'id': instance.id,
            'name': instance.name,
            'price': float(instance.price),
            'stock': instance.quantity,
            'image': str(instance.image),
            'description': instance.description,
            'category': instance.category_id,
            'rating': instance.rating,
        }
    }

    with open('product.json', 'a') as f:
            json.dump(data, f,indent=4)

    print(f'{instance} Successfully Deleted!')