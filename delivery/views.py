# Views for delivery.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, View
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import CheckoutForm
from .models import (
    MenuItems,
    Order,
    OrderItem,
    CheckoutAddress,
    Payment,
    
)

import stripe
stripe.api_key = settings.STRIPE_KEY

class ShowMenuItem(ListView):
    model = MenuItems
    template_name = 'main/delivery.html'
        
    def get_context_data(self, **kwargs):
        context = super(ShowMenuItem, self).get_context_data(**kwargs)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except:
            order = 0
        context['food'] = MenuItems.objects.all()
        context['cart']=order
        context['title'] = _('Delivery')
        
        return context
    
    
class ShowMenuDetailed(DetailView):
    model = MenuItems
    template_name = 'main/delivery-detailed.html'

    def get_context_data(self, **kwargs):
        context = super(ShowMenuDetailed, self).get_context_data(**kwargs)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except:
            order = 0
        context['title'] = MenuItems.objects.get(pk=self.kwargs['pk'])
        context['cart']=order
        return context



class CreateDishes(CreateView):
    model = MenuItems
    template_name = 'main/add-dishes.html'
    fields = ['item', 'category', 'label', 'item_description', 'item_composition', 'item_weight', 'item_price', 'item_discount', 'item_calories', 'item_image', 'milk_added']


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
                
                }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an order"))
            return redirect("delivery")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                phone_number = form.cleaned_data.get('phone_number')            
                payment_option = form.cleaned_data.get('payment_option')
                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    first_name = first_name,
                    last_name= last_name,
                    email = email,
                    phone_number = phone_number,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()

                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(self.request, _("Invalid Payment option"))
                    return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an order"))
            return redirect("order-summary")
        except ValueError:
            messages.error(self.request, _("Form is not completed!"))
            return redirect('checkout')

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price() * 100)  #cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, _("Success make an order"))
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, _("To many request error"))
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, _("Invalid Parameter"))
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, _("Authentication with stripe failed"))
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, _("Network Error"))
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, _("Something went wrong"))
            return redirect('/')
        
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, _("Not identified error"))
            return redirect('/')

        
  

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(MenuItems, pk=pk )
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("delivery")
        else:
            order.items.add(order_item)
            return redirect("delivery")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("delivery")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(MenuItems, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            return redirect("order-summary")
        else:
            messages.info(request, _("This Item is not in your cart"))
            return redirect("product", pk=pk)
    else:
        #add message cart empty
        messages.info(request, _("You cart is empty"))
        return redirect("product", pk = pk)


@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(MenuItems, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            return redirect("order-summary")
        else:
            return redirect("order-summary")
    else:
        #add message cart is empty
        messages.info(request, _("You cart is empty!"))
        return redirect("order-summary")



@login_required
def delete(request):
    Order.objects.get(user=request.user, ordered=False).delete()
    return HttpResponseRedirect(reverse('delivery'))

