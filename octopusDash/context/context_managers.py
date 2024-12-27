from django.urls import reverse
from octopusDash.core.urls import build_urls
from octopusDash.core.model_registry import octopus_registry
def url_context(request):
    urls = build_urls(octopus_registry.registry)
    
    print(urls)

    return {"urls":urls}