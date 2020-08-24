from django.contrib import admin
from .models import Product, Category, Comment, Order, OrderItem, Payment, Coupon


admin.site.register(Coupon)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)