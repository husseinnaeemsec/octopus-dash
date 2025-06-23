from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from ..exceptions import AppNotFound,ModelNotFound
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
import logging


logger = logging.getLogger(__name__)

from django.core.exceptions import ImproperlyConfigured



class ViewErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        dashboard_path = None
        try:
            dashboard_path = settings.OCTOPUSDASH.get("dashboard_path")
        except (AttributeError, KeyError, Exception):
            pass
        
        if dashboard_path is not None and not dashboard_path.startswith("/"):
            dashboard_path = "/" + dashboard_path
        
        self.dashboard_path = dashboard_path

    def __call__(self, request):
        try:
            if self.dashboard_path is None:
                raise ImproperlyConfigured(
                    "To enable authentication checks in OctopusDash, you must define the dashboard_path in your OCTOPUSDASH configuration."
                )

            response = self.get_response(request)
            return response

        except Exception as ex:
            if request.path.startswith(self.dashboard_path):
                return self.process_exception(request, ex)
            raise

    def process_exception(self, request, exception):
        if isinstance(exception, AppNotFound):
            return render(request, 'od/errors/app_not_found.html', status=404)
        elif isinstance(exception, ModelNotFound):
            return render(request, 'od/errors/model_not_found.html', status=404)
        elif isinstance(exception, Http404):
            return render(request, 'od/errors/page_not_found.html', status=404)
        else:
            raise
