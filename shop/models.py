import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
    	return reverse('shop:index')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/profile_pictures')
    facebook_url = models.CharField(max_length=255, null=True, blank=True, )
    twitter_url = models.CharField(max_length=255, null=True, blank=True, )
    instagram_url = models.CharField(max_length=255, null=True, blank=True, )
    linked_in_url = models.CharField(max_length=255, null=True, blank=True, )
    website_url = models.CharField(max_length=255, null=True, blank=True, )

    def __str__(self):
    	return str(self.user)    


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    discount_price = models.FloatField(blank=True, null=True)
    product_image = models.ImageField(upload_to='media/')
    created_at = models.DateField(auto_now_add=True)
    stock =  models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)


    def ran_gen_serial_num(chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(10)) 
    

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('shop:index')
