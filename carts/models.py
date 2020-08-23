from django.db import models
from shop.models import Product


class CartsItem(models.Model):
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


class Carts(models.Model):
	products = models.ManyToManyField(CartsItem)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id) + "thcart"

	def get_total(self):
		total = 0
		for order_item in self.products.all():
			total += order_item.get_final_price()
		return total