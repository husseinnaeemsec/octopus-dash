from .registry import dashboard

registry = dashboard.get_registry()



def get_model_admin(app_config,model):
    
    
    try:
        return registry[app_config]['models'][model]['admin']
    
    except KeyError:
        return None

def get_app_models(app_config):
    
    try:
        return registry[app_config]['models']
    
    except KeyError:
        return None