# Generated by Django 3.0 on 2020-08-24 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20200824_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Coupon'),
        ),
    ]