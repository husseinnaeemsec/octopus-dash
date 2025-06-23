from ...contrib.admin import registry
from ...exceptions import AppNotFound, ModelNotFound
from ...forms import DynamicFilterForm

class AppContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(kwargs.get("app"))
        if not self.app:
            raise AppNotFound(f'App with label "{kwargs.get("app")}" not found')
        return super().dispatch(request, *args, **kwargs)


class AppModelContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(kwargs.get("app"))
        if not self.app:
            raise AppNotFound(f'App with label "{kwargs.get("app")}" not found')
        self.model_name = kwargs.get("model")
        self.model = self.app.get_model(self.model_name)
        if not self.model:
            raise ModelNotFound(f'Model "{self.model_name}" not found')
        self.model_admin = self.app.get_model_admin(self.model_name)
        self.filters_form = DynamicFilterForm(self.model_admin, request.GET)
        return super().dispatch(request, *args, **kwargs)
    