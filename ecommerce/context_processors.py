from shop.models import Category, Cart, CartItem
from shop.views import _cart_id


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def counter(request):
	item_count = 0
	if 'admin' in request.path:
		return {}
	else:
		try:
			cart = Cart.objects.filter(cart_id=_cart_id(request))
			cart_items = CartItem.objects.all().filter(cart=cart[:1])
			for cart_item in cart_items:
				item_count += cart_item.quantity
		except Cart.DoesNotExist:
			item_count = 0
	return dict(item_count=item_count)