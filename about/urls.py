from django.urls import path

from . import views


app_name = 'about'

urlpatterns = [
    path('', views.AboutProjectView.as_view(), name='about_project'),
    ]