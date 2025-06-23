from .contrib.admin import registry
from django.http import HttpRequest

apps = registry.get_apps()

def global_context(request:HttpRequest):
    if not request.user.is_authenticated:
        
        return {}
    
    return {
        'od_apps':apps
    }