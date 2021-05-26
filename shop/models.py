from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.utils import timezone


now = timezone.now()

User = get_user_model()


class Category(models.Model):

    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def get_url(self):
        return reverse('category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET('Другое'),
                                 related_name='products')
    name = models.CharField(max_length=250)
    code = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    weight = models.PositiveIntegerField(help_text='в граммах/миллилитрах')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.id])

    def __str__(self):
        return self.name


class Sale(models.Model):
    title = models.CharField(max_length=500)
    date_until = models.DateTimeField()
    discount = models.IntegerField(help_text='скидка в процентах', default=0)
    image = models.ImageField(upload_to='blog', blank=True)

    @property
    def is_active(self):
        return now < self.date_until


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ { self.id }'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
