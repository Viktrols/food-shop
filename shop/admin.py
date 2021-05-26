from django.contrib import admin

from .models import Category, Product, Sale, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('description', 'name',)
    empty_value_display = '-пусто-'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'code', 'price', 'stock',)
    search_fields = ('name', 'code')
    empty_value_display = '-пусто-'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk',)


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product')
