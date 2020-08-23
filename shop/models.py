import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField

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

    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", kwargs={
            'pk': self.pk
        })



class OrderItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_added)


class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

