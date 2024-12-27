from django.contrib import admin
from octopusDash.models import Post,Poll
from octopusDash.core.model_registry import octopus_registry


post_kwargs = {
    'fields':['id','title','content','author']
}

octopus_registry.register_model(Post,**post_kwargs)
octopus_registry.register_model(Poll)


