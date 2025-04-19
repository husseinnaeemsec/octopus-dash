from .registry import dashboard
from .models import Profile
from django.utils.text import capfirst
from .conf import settings
from django.apps import apps



def global_context(request):
    
    path_parts = request.path.strip('/').split('/')
    url = ''
    breadcrumb_list = []

    for part in path_parts:
        url += f'/{part}'
        breadcrumb_list.append({
            'name': capfirst(part.replace('-', ' ')),  # Beautify names
            'url': url
        })

    if request.user.is_authenticated and not hasattr(request.user,'profile'):
        profile,created = Profile.objects.get_or_create(user=request.user)
        
    
    return {
        "registry":dashboard.get_registry(),
        'path':breadcrumb_list,
        'octopusdash_settings':settings,
        'installed_apps':apps.get_app_configs(),
    }