# Generated by Django 3.0 on 2020-08-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20200821_0821'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartsitem',
            name='product',
        ),
        migrations.AddField(
            model_name='cartsitem',
            name='products',
            field=models.ManyToManyField(to='shop.Product'),
        ),
    ]
