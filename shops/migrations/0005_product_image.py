# Generated by Django 5.1.5 on 2025-02-03 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_alter_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shops/media/products/'),
        ),
    ]
