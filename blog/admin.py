from django.contrib import admin

from .models import Post, Whyme

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'pub_date')
    search_fields = ('text', 'title')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Whyme)
class WhymeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text')
    search_fields = ('text', 'title')
