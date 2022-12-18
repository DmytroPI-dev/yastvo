from django.db import models
from django.db.models import query
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Breakfast, Lunch, Salads, Snack, French_toasts, Category, LatestProducts
from .mixins import CategoryDetailMixin

def test_view(request):
    categories = Category.objects.get_categories_for_left_sidebar()

    return render(request, 'shopping/shopping.html', {'categories': categories})


class ProductDetailView (DetailView):

    CT_MODEL_MODEL_CLASS = {
        'Breakfast': Breakfast,
        'Snack': Snack,
        'Salads': Salads,
        'Lunch' : Lunch,
        'French_toasts' : French_toasts,

    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    
    context_object_name = 'product'
    template_name = 'shopping/product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'shopping/category_detail.html'
    slug_url_kwarg = 'slug'
    