from django.urls import path

from . import views
from .views import ProductListView

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('shop/<int:product_id>/', views.product, name='product'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),
    path('shop/<slug:slug>/', views.category_products, name='category_products'),
]
