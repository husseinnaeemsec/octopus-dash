from django import template
from django.urls import reverse_lazy
from octopusDash.core.model_registry import RegistryObject,octopus_registry

register = template.Library()

@register.filter(name='attr')
def attr(obj, field_name):
    return getattr(obj, field_name, None)




@register.simple_tag(name='get_model_view')
def get_model_view(app_name,model_name,viwename,**kwargs):
    
    
    return RegistryObject.get_model_view(app_name,model_name,viwename,**kwargs)
    

@register.simple_tag(name='get_app_view')
def get_app_view(app_name,viwename,**kwargs):
    
    return RegistryObject.get_app_view(app_name,viwename,**kwargs)
    