from django.core.exceptions import PermissionDenied
import importlib
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_default_permission_classes():
    """
    Dynamically import and return the default permission classes
    specified in OCTOPUS_DASH_SETTINGS.
    """
    permission_classes = []
    if hasattr(settings, "OCTOPUS_DASH_SETTINGS"):
        for path in settings.OCTOPUS_DASH_SETTINGS.get("DEFAULT_PERMISSION_CLASSES", []):
            try:
                module_path, class_name = path.rsplit(".", 1)
                module = importlib.import_module(module_path)
                permission_class = getattr(module, class_name)
                permission_classes.append(permission_class)
            except (ImportError, AttributeError, ValueError) as e:
                raise ImproperlyConfigured(
                    f"Could not import permission class '{path}': {e}"
                )
    return permission_classes


class PermissionMixin:
    """
    Mixin to add permission_classes to Django class-based views.
    """
    permission_classes = []
    permission_classes.extend(get_default_permission_classes())

    def check_permissions(self, request):
        """
        Check if the request satisfies the required permissions.
        """
        for permission_class in self.permission_classes:
            if not permission_class().has_permission(request, self):
                raise PermissionDenied("You do not have permission to access this view.")

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to check permissions before processing the request.
        """
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)


class IsAdmin:
    """
    Permission class to allow only admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_staff

class IsAuthenticated:
    """
    Permission class to allow only authenticated users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated