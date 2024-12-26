from django.apps import apps

urlpatterns =[] 

if apps.ready:
    
    from octopusDash.core.url_registry import url_registry,generate_urls_from_registry

    urlpatterns = generate_urls_from_registry(url_registry)



 