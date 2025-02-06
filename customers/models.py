from enum import unique

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Customer(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    phone = PhoneNumberField(region='UZ', unique=True)
    address = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    VAT_number = models.CharField(max_length=100, unique=True,null=True,blank=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.name} => {self.phone}"

    @property
    def image_url(self):
        return self.image.url