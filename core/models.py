from django.conf import settings
from django.db import models

from django.urls import reverse

CATEGORY_CHOICES = (
		('HLS', 'Heels'),
		('SNKS', 'Sneakers'),
		('BTS', 'Boots'),
		('O', 'Official'),
		('C&S', 'Crocs & Sandals'),
		('SPRT', 'Sports'),
		('M', 'Male'),
		('F', 'Female'),
	)

class Item(models.Model):
	name			= models.CharField(max_length=123)
	price			= models.FloatField()
	discount_price	= models.FloatField(blank=True, null=True)
	size			= models.CharField(max_length=123)
	slug			= models.SlugField()
	condition 		= models.CharField(max_length=123)
	category 		= models.CharField(choices=CATEGORY_CHOICES, max_length=10)
	quality_score	= models.FloatField()
	timestamp 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("core:product-detail", kwargs={'slug':self.slug})

	def get_add_to_cart_url(self):
		return reverse("core:add-to-cart", kwargs={'slug':self.slug})
	def get_remove_from_cart_url(self):
		return reverse("core:remove-from-cart", kwargs={'slug':self.slug})

class OrderItem(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ordered 		= models.BooleanField(default=False)
	item			= models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity		= models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.item.name}"

	def get_total_item_price(self):
		return self.item.price * self.quantity

	def get_total_discount_item_price(self):
		return self.item.discount_price * self.quantity

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		return self.get_total_item_price

class Order(models.Model):
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	items 			= models.ManyToManyField(OrderItem)
	start_date		= models.DateTimeField(auto_now_add=True)
	ordered_date 	= models.DateTimeField()
	ordered 		= models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def get_sub_total(self):
		sub_total = 0
		for order_item in self.items.all():
			sub_total += order_item.get_final_price()
		return sub_total

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total
