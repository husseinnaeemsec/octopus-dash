
from octopusdash.registry import dashboard,ModelAdmin
from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, Payment, OrderStatus

# Register each model with the custom dashboard (or django admin)

class OrderAdmin(ModelAdmin):
    list_display = ['user','order_number','customer_name','total_amount','order_date','status']

class PaymentAdmin(ModelAdmin):
    
    list_display = ['order','payment_method','amount','payment_date']

dashboard.register(Order,OrderAdmin)
dashboard.register(OrderItem)
dashboard.register(ShippingAddress)
dashboard.register(Payment,PaymentAdmin)
dashboard.register(OrderStatus)

admin.site.register(Order)