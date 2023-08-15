"""This is urls.py in app main
It is created for main app and its parts
"""
from django.urls import path
from . import views
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
    ShowMenuItem,
    ShowMenuDetailed,
    CreateDishes
    
)

urlpatterns = [
    path('', ShowMenuItem.as_view(), name = 'delivery'),
    path('<slug:_id>', ShowMenuDetailed.as_view(), name = 'delivery-detailed' ),  
    path('add', CreateDishes.as_view(), name = 'add'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('add-to-cart/<slug:_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:pk>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<slug:pk>/', reduce_quantity_item, name='reduce-quantity-item'),
    path('delete', views.delete, name='delete'),
]



