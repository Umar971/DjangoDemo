from django.contrib import admin
from .models import Product, Category, Comment, Order, OrderItem


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(OrderItem)
admin.site.register(Order)