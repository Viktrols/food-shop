from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search_results'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:product_id>/', views.product, name='product'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove,
         name='cart_remove'),
    path('shop/<slug:slug>/', views.category_products,
         name='category_products'),
    path('myaccount/<str:username>/', views.my_account, name='my_account'),
    path('create/', views.order_create, name='create'),
    path('orderisreate/', views.OrderisCreateView.as_view(),
         name='order_is_create'),
]
