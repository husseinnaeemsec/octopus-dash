from django.contrib import admin
from octopusDash.core.model_registry import octopus_registry
from .models import HomePage
from django.contrib.auth.models import User


octopus_registry.register_model(HomePage)
octopus_registry.register_model(User)

