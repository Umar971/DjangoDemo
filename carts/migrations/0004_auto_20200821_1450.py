# Generated by Django 3.0 on 2020-08-21 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20200821_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartsitem',
            name='carts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='carts.Carts'),
        ),
    ]
