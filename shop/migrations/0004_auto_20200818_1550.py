# Generated by Django 3.0 on 2020-08-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200818_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='media/'),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
