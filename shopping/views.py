from django.db.models import query
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import DetailView
from shopping import models
from .models import Breakfast, Lunch, Salads, Snack, French_toasts

def test_view(request):
    return render(request, 'shopping/shopping.html', {})


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
