from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

class AccessMiddleware:
    """
    Middleware to restrict access to the /dashboard route to admins only.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is '/dashboard'
        # if request.path.startswith('/dashboard'):
        #     # Ensure the user is authenticated and is an admin
        #     if not request.user.is_authenticated:
        #         # Redirect unauthenticated users to the login page
        #         return redirect('/admin/login/?next=/dashboard/')
        #     if not request.user.is_staff:  # Adjust based on your admin criteria
        #         return HttpResponseForbidden("You do not have permission to access this page.")

        # # Process the request normally
        return self.get_response(request)
