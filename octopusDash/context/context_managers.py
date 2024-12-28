from django.urls import reverse
from octopusDash.core.urls import build_urls
from octopusDash.core.model_registry import octopus_registry
def url_context(request):
    urls = build_urls(octopus_registry.registry)
    # Split the request path into segments
    path_segments = request.path.strip('/').split('/')
    
    # Create a list of breadcrumbs (you can customize this part as needed)
    breadcrumb_data = []
    url = ''
    for segment in path_segments:
        url += f'/{segment}'  # Rebuild the URL step by step
        breadcrumb_data.append({
            'name': segment.replace('-', ' ').title(),  # Capitalize and replace hyphens
            'url': url
        })
    return {"urls":urls,'path':breadcrumb_data}