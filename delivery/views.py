# Views for delivery.
from .models import MenuItems
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

class ShowMenuItem(ListView):
    model = MenuItems
    template_name = 'main/delivery.html'
    context_object_name = 'items'


    def get_context_data(self, **kwargs):
        ctx = super(ShowMenuItem, self).get_context_data(**kwargs)

        ctx['title'] = 'Доставка Кафе Яство'
        return ctx

class ShowMenuDetailed(DetailView):
    model = MenuItems
    template_name = 'main/delivery-detailed.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShowMenuDetailed, self).get_context_data(**kwargs)

        ctx['title'] = MenuItems.objects.get(pk=self.kwargs['pk'])
        return ctx

class CreateDishes(CreateView):
    model = MenuItems
    template_name = 'main/add-dishes.html'
    fields = ['title', 'item_description', 'item_composition', 'item_weight', 'item_price', 'item_image']

    