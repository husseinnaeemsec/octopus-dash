from django.contrib import admin
from octopusDash.models import Post,Poll
from octopusDash.core.model_registry import octopus_registry


post_kwargs = {
    'fields':['id','title','content','author'],
    'pagination':{
        'object_per_page':20,
        'show_first_last':True,
        'prev_next_format':'first_last_numbers',
        'last_page_number':True,
        'template': 'admin/pagination/numeric.html',
        'show_endless':True,
        'show_unnumbered':True,
    }
}

octopus_registry.register_model(Post,**post_kwargs)
octopus_registry.register_model(Poll)

admin.site.register(Post)
