# Generated by Django 5.1.5 on 2025-02-02 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
