
from octopusdash.registry import dashboard
from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, Payment, OrderStatus

# Register each model with the custom dashboard (or django admin)
dashboard.register(Order)
dashboard.register(OrderItem)
dashboard.register(ShippingAddress)
dashboard.register(Payment)
dashboard.register(OrderStatus)
