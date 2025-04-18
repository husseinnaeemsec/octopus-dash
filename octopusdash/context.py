from .registry import dashboard
def global_context(request):
    
    return {
        "registry":dashboard.get_registry()
    }