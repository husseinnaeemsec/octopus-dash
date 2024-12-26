from django.contrib import admin
from octopusDash.models import Post,Poll
from octopusDash.core._registry import octopus_registry


octopus_registry.register_model(Post)
octopus_registry.register_model(Poll)


