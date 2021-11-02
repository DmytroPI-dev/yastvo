from django.urls import path
from .views import test_view, ProductDetaliView


urlpatterns = [
    path('', test_view, name = 'shopping'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetaliView.as_view(), name='product_detail')
    ]
