from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.index_blog, name='index_blog'),
    path('blog/<int:post_id>/', views.post, name='post')
]
