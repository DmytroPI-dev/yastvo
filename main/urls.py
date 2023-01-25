"""This is urls.py in app main
It is created for main app and its parts
"""
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name = 'home'),
    path('menu', views.menu, name = 'menu'),
    path('contacts', views.contacts, name = 'contacts'),
    
   ]
