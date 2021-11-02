"""This is urls.py in app main
It is created for main app and its parts
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowMenuItem.as_view(), name = 'delivery'),
    path('<int:pk>', views.ShowMenuDetailed.as_view(), name = 'delivery-detailed' ),  #задаем динемический путь: int - integer, slug = span
    path('add', views.CreateDishes.as_view(), name = 'add'),
]
