from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import Item, OrderItem, Order


class HomeView(ListView):
	model 					= Item
	template_name			= "home_page.html"

class CheckoutView(ListView):
	model 					= Item
	template_name			= "checkout.html"

class AboutView(ListView):
	model 					= Item
	template_name			= "about_page.html"

class ContactView(ListView):
	model 					= Item
	template_name			= "contact/view.html"

def home(request):
	context = {
		"items" : Item.objects.all()
	}
	return render(request, "home_page.html", context)

class OrderSummaryView(View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object': order
			}
			return render(self.request, 'order_summary.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an active order")
			return redirect("/")

class ProductListView(ListView):
	model 					= Item
	template_name			= "list.html"

class ProductDetailView(DetailView):
	model 					= Item
	template_name			= "detail.html"


def add_to_cart(request, slug):
	item 					= get_object_or_404(Item, slug=slug)
	order_item, created 	= OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
	order_qs 				= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# Check if order item is in order
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item was successfully updated")
		else:
			messages.info(request, "This item was successfully added to your cart")
			order.items.add(order_item)
			return redirect('core:order_summary')
	else:
		ordered_date		= timezone.now()
		order 				= Order.objects.create(user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "This item was successfully updated")
	return redirect("core:order_summary")

def remove_from_cart(request, slug):
	item 					= get_object_or_404(Item, slug=slug)
	order_qs 				= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# Check if order item is in order
		if order.items.filter(item__slug=item.slug).exists():
			order_item 		= OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
			order.items.remove(order_item)
			messages.info(request, "This item was successfully removed from cart")
			return redirect('core:order_summary')
		else:
			messages.info(request, "This item was not in your cart")
			return redirect('core:product-detail', slug=slug)
	else:
		messages.info(request, "You do not have an active order")
		return redirect('core:product-detail', slug=slug)


def remove_single_item_from_cart(request, slug):
	item 					= get_object_or_404(Item, slug=slug)
	order_qs 				= Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# Check if order item is in order
		if order.items.filter(item__slug=item.slug).exists():
			order_item 		= OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			messages.info(request, "This item's quantity was updated")
			return redirect('core:order_summary')
		else:
			messages.info(request, "This item was not in your cart")
			return redirect('core:product-detail', slug=slug)
	else:
		messages.info(request, "You do not have an active order")
		return redirect('core:product-detail', slug=slug)