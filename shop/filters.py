import django_filters 

from .models import Product

class ProductFilter(django_filters.FilterSet):
    
    CHOICES= (
        ('descending', 'Сначала новинки'),
        ('price', 'Цена по возрастанию'),
        ('price_2', 'Цена по убыванию')
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES,
                                           method = 'filter_by_ordering')
    class Meta:
        model = Product
        fields = {
            'description': ['icontains'],
        }
    


    def filter_by_ordering(self, queryset, name, value):
        if value == 'price_2':
            expression = '-price'
        elif value == 'descending':
            expression = '-created'
        elif value == 'price':
            expression = 'price'
        return queryset.order_by(expression)
