from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from blog.models import Post, Whyme
from django.views.generic import ListView

from .models import Category, Product, Sale, Cart, CartItem

from .filters import ProductFilter
from django.utils import timezone


now = timezone.now()

def index(request):
    sale = Sale.objects.latest('id')
    t = sale.date_until
    timer = t.strftime('%Y/%m/%d')
    new = Product.objects.all()[:6]
    whyblock = Whyme.objects.latest('id')
    posts = Post.objects.all()[:3]
    return render(request, 'index.html', {'posts': posts,
                 'whyblock': whyblock, 'new': new, 'sale':sale, 'timer': timer})


class ProductListView(ListView):
    model = Product
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET,
                            queryset = self.get_queryset())
        return context


def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product.html', {'product': product})


def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart


def add_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(cart_id=_cart_id(request))
		cart.save()
	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		if cart_item.quantity < cart_item.product.stock:
			cart_item.quantity += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
		cart_item.save()

	return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, total_without_discount=0, cart_items=None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		sale = Sale.objects.latest('id')
		for cart_item in cart_items:
			counter += cart_item.quantity
			if sale.date_until > now:
				total_without_discount += (cart_item.product.price * cart_item.quantity)
				total += (cart_item.product.price * cart_item.quantity)/100 * (100-sale.discount)
			else:
				total += (cart_item.product.price * cart_item.quantity)
				
	except ObjectDoesNotExist:
		pass

	return render(request, 'shop/cart.html', dict(cart_items=cart_items, total=total,counter=counter, sale=sale,
				  total_without_discount=total_without_discount))


def cart_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart_detail')


def cart_remove_product(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart_detail')


def category_products(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = category.products.all()
	return render(request, 'shop/category.html', {'category': category, 'products': products})