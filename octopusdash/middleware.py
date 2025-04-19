from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings


try:
    dashboard_path = settings.DASHBOARD_PATH

except:
    dashboard_path = None

class CheckAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        response = self.get_response(request)
        
        if dashboard_path and request.path.startswith(dashboard_path) and not request.user.is_authenticated and not request.path == reverse_lazy("octopusdash-login") :
            
            return redirect(reverse_lazy("octopusdash-login"))
        
        return response