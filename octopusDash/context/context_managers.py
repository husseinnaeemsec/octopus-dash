from octopusDash.core._registry import octopus_registry
from django.urls import reverse
from octopusDash.templatetags.urltags import get_app_url,get_url
def url_context(request):
    
    registry_list = []
    
    for app,models in octopus_registry.registry.items():
        app = app.lower()
        data = {
                'app':app,
                'url':get_app_url(app),
                'models':[]
            }
        
        
        for model in models:
            model_data =  data['models'].append({'model':model.__name__.lower(),'list':get_url(model,'list'),'create':get_url(model,'create')})
    
    

        registry_list.append(data)
        
    

    return {"urls":registry_list}