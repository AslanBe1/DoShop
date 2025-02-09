from django.db import models
from django.contrib.auth.models import AbstractUser
from User.managers import UserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField('Email Address',
                          unique=True
                          )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

#
#
# class Register(models.Model):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.email