# Generated by Django 3.2.3 on 2021-05-17 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
    ]