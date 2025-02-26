import json
from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=Customer)
def customer_created(sender, instance, created, **kwargs):
    if created:
        email = EmailMessage(
            'Customer Created',
            f'{instance} Customer Successfully Created',
            to=['aslanabdimuminov31@gmail.com'],
        )
        email.send()

    else:
        email = EmailMessage(
            'Customer Updated',
            f'{instance} Customer Successfully Updated',
            to=['aslanabdimuminov31@gmail.com',]
        )
        email.send()


@receiver(post_delete, sender=Customer)
def customer_deleted(sender, instance, **kwargs):
    email = EmailMessage(
        'Customer Deleted',
        f'{instance} Customer Successfully Deleted',
        to = ['aslanabdimuminov31@gmail.com'],
    )
    email.send()

@receiver(pre_delete, sender=Customer)
def customer_pre_delete(sender, instance, **kwargs):
    data = {
        f'{instance.id}': {
            'id' : str(instance.id),
            'name' : instance.name,
            'image' : str(instance.image),
            'address' : instance.address,
            'phone' : instance.phone,
            'email' : str(instance.email),
            'VAT' : instance.VAT_number,
            'password': str(instance.password),

        },
    }

    with open('customers.json', 'w') as f:
        json.dump(data, f)

    email = EmailMessage(
        'Customer Deleted',
        f'{instance} Customer Successfully Deleted',
        to = 'aslanabdimuminov31@gmail.com',
    )
    email.send()


