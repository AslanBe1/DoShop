from decimal import Decimal

from django.db import models

# Create your models here.

class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    discount = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE)

    @property
    def discount_price(self):
        if self.discount > 0:
            self.price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return Decimal(self.price).quantize(Decimal('0.001'))

    def __str__(self):
        return self.name