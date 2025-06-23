from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



class CheckAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dashboard_path = None

        try:
            dashboard_path = settings.OCTOPUSDASH.get("dashboard_path")

        except (AttributeError,KeyError):
            dashboard_path = None

        
        if not dashboard_path:
            raise ImproperlyConfigured("To enable authentication checks in OctopusDash, you must define the dashboard_path in your OCTOPUSDASH configuration.  ")
        
        response = self.get_response(request)
        

        
        if not dashboard_path.startswith("/"):
            dashboard_path = "/"+dashboard_path
        
        if dashboard_path and request.path.startswith(dashboard_path) and not request.user.is_authenticated and not request.path == reverse_lazy("od-login") :
            
            return redirect(reverse_lazy("od-login"))
        
        return response