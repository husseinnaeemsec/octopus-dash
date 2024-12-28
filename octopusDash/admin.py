from django.contrib import admin
from octopusDash.models import Post,Poll
from octopusDash.core.model_registry import octopus_registry


post_kwargs = {
    'fields':['id','title','content','author'],
    'display_fields':['id','title','content'],
    'view':{
        'paginate_by':1
    },
    'pemrssions':{
        
    },
    # include custom widget to a specific view 
    'include_custom_widget':{
        'view':'list',
        'widget':'my_app/widgets/list_widget.html',
        'order':'top' # or 'bottom' or container_id example: "#top_widget"
    },
    # You can include your own custom pages but make sure to include permssions and handle security issues
    'include_custom_pages':[
        {
        'page':'Settings',
        'url_pattern': '/url_pattern/', # use reverse for stable output 
        'view':'ListView', # include your view
        'name':'view-name',

        },
        
    ]
}


octopus_registry.register_model(Post,**post_kwargs)
octopus_registry.register_model(Poll)

admin.site.register(Post)
