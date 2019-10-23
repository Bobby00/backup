from django.urls import path
from .views import ProductListView, ProductDetailView, HomeView, AboutView, CheckoutView, ContactView, add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderSummaryView

app_name = 'core'

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('checkout/', CheckoutView.as_view(), name='checkout'),
	path('about_us/', AboutView.as_view(), name='about'),
	path('contact_us/', ContactView.as_view(), name='contact'),
	path('products/', ProductListView.as_view(), name='product-list'),
	path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),
	path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
	path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
	path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
	path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
]