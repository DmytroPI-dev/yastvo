# Register your models here.
from django.contrib import admin

from .models import (
    MenuItems,
    Order,
    OrderItem,
    Payment,
    CheckoutAddress,

)

admin.site.register(MenuItems)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutAddress)
admin.site.register(Payment)