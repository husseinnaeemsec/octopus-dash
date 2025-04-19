from django.contrib import admin
from octopusdash.registry import dashboard
from .models import Store, StoreProduct, StoreEmployee, StoreReview, StoreInventory

# Register each model with the custom dashboard (or django admin)
dashboard.register(Store)
dashboard.register(StoreProduct)
dashboard.register(StoreEmployee)
dashboard.register(StoreReview)
dashboard.register(StoreInventory)
