from django.urls import reverse_lazy

from django import template

register = template.Library()


@register.filter(name='get_url')
def get_url(model,view:str='list',pk=None):
    
    model_name = model.__name__.lower()
    app_name = model._meta.app_label.lower()
    
    if view == 'list':
        
        return reverse_lazy(f"{app_name}-{model_name}-list")
    
    elif view == 'create':
        
        return reverse_lazy(f"{app_name}-{model_name}-create")
    
    elif view == 'edit':
        
        return reverse_lazy(f"{app_name}-{model_name}-edit", kwargs={'pk': pk})
    
    elif view == 'delete':
        
        return reverse_lazy(f"{app_name}-{model_name}-delete", kwargs={'pk': pk})
    
    elif view == "detail":
        return reverse_lazy(f"{app_name}-{model_name}-detail", kwargs={'pk': pk})
    
    else:
        raise ValueError("Invalid view. Supported views: list, create, edit, delete, detail")
    
@register.filter(name='get_app_url')
def get_app_url(app_name):
    
    return reverse_lazy(app_name)

