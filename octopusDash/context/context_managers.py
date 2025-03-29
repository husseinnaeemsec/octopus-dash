from ..core import DashboardApp,app_registry
from ..models import DashboardSetting

def url_context(request):
    # Split the request path into segments
    path_segments = request.path.strip('/').split('/')
    settings,created= DashboardSetting.objects.get_or_create(site_id=1)
    
    # Create a list of breadcrumbs (you can customize this part as needed)
    breadcrumb_data = []
    url = ''
    for segment in path_segments:
        url += f'/{segment}'  # Rebuild the URL step by step
        breadcrumb_data.append({
            'name': segment.replace('-', ' ').title(),  # Capitalize and replace hyphens
            'url': url
        })
    return {'path':breadcrumb_data,'app_registry': app_registry.items(),'settings':settings}