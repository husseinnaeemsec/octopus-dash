from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, ProductReview, Supplier
from octopusdash.registry import dashboard
# Register each model with the custom dashboard (or django admin)
dashboard.register(Product)
dashboard.register(ProductCategory)
dashboard.register(ProductImage)
dashboard.register(ProductReview)
dashboard.register(Supplier)
