from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from blog.models import Post, Whyme
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Category, Product, Sale, Cart, CartItem, User, Order, OrderItem

from .filters import ProductFilter
from django.utils import timezone


now = timezone.now()

def index(request):
    sale = Sale.objects.latest('id')
    timer = sale.date_until.strftime('%Y/%m/%d')
    new = Product.objects.all()[:6]
    whyblock = Whyme.objects.latest('id')
    posts = Post.objects.all()[:3]
    return render(request, 'index.html', {'posts': posts,
                 'whyblock': whyblock, 'new': new, 'sale':sale, 'timer': timer})


class ProductListView(ListView):
	paginate_by = 2
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


def cart_detail(request, total=0, counter=0, total_without_discount=0, cart_items=None, sale=None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		sale = Sale.objects.latest('id')
		for cart_item in cart_items:
			counter += cart_item.quantity
			if sale.is_active:
				total_without_discount += (cart_item.product.price * cart_item.quantity)
				total += (cart_item.product.price * cart_item.quantity)/100 * (100-sale.discount)
			else:
				total += (cart_item.product.price * cart_item.quantity)
		
	except ObjectDoesNotExist:
		pass

	return render(request, 'shop/cart.html', dict(cart_items=cart_items, total=total,counter=counter,
				  total_without_discount=total_without_discount, sale=sale))


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


@login_required
def order_create(request):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	sale = Sale.objects.latest('id')
	cart_items = CartItem.objects.filter(cart=cart, active=True)
	order = Order.objects.create(user=request.user)
	for item in cart_items:
		if sale.is_active:
			price = item.product.price/100 * (100-sale.discount)
			OrderItem.objects.create(order=order, product=item.product, price=price, quantity=item.quantity)
		else:
			OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
	cart.delete()
	return redirect('my_account', username=request.user.username)




def category_products(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = category.products.all()
	paginator = Paginator(products, 2)
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)
	return render(request, 'shop/category.html', {'category': category, 'products': products,
	'page': page, 'paginator': paginator})


@login_required
def my_account(request, username):
	user = get_object_or_404(User, username=username)
	orders =user.orders.all()
	return render(request, 'my_account.html', {'user': user, 'orders': orders})


