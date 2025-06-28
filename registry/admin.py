

from django.apps import apps
from django.db.models import Model
from django.db import models
from ..contrib.managers import DashboardModelManager
from ..utils.fields import get_field_input_type
from .metaclasses import ModelAdminMetaClass
from ._exceptions import *
from .decorators import action

# --------------------------
# Main ModelAdmin class
# --------------------------

class ModelAdmin(metaclass=ModelAdminMetaClass):
    """
    Base admin class for Django models.
    
    Attributes correspond to configuration options and are validated on class creation.
    """

    model: Model | None
    list_display: list = []
    list_editable: list = []
    search_fields: list = []
    filter_fields: list = []
    permission_classes: list = []
    readonly_fields: list = []
    hidden_fields: list = []
    serializer_class = None
    lookup_field: str = 'id'
    plural_name: str = None
    form_fields = '__all__'

    model_icon: str = ''' <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
        </svg>
        '''
    actions: list = ['delete']

    def __init__(self, model: Model = None, *args, **kwargs):
        """
        Initialize the ModelAdmin instance.

        Args:
            model (Model): The Django model class to be managed.
        """
        
        if not self.model and not model:
            raise MissingModelException(self.__class__.__name__)
        
        
        if model and not self.model:
            self.model = model
        
        
        self._filter_fields = {}
        self.manager = DashboardModelManager(self.model)
        self.model_name = self.model._meta.model_name
        self.model_name_display = self.model_name.title()
        self.model_plural_name = self.model._meta.verbose_name_plural
        self.model_plural_name_display = self.model_plural_name.title()
        self.model_icon = kwargs.get("icon")
        self.model_opts = self.model._meta

        # Prepare filter fields metadata for UI rendering
        if self.filter_fields:
            for field in self.model._meta.get_fields():
                if field.name in self.filter_fields:
                    field_data = {
                        'display_name': field.name.replace("_", " ").title(),
                        'lookup_query': field.name
                    }

                    if isinstance(field, models.BooleanField):
                        field_data['type'] = 'bool'

                    elif isinstance(field, (models.DateField, models.DateTimeField, models.TimeField)):

                        if isinstance(field, models.DateTimeField):
                            field_data['type'] = 'datetime'
                        elif isinstance(field, models.DateField):
                            field_data['type'] = 'date'
                        elif isinstance(field, models.TimeField):
                            field_data['type'] = 'time'

                        # For date/time range filtering
                        field_data['lookup_query'] = [
                            f"{field.name}_start",
                            f"{field.name}_end",
                        ]

                    self._filter_fields[field.name] = field_data

    def get_inline_edit_fields(self) -> dict:
        """
        Return a dict of fields that are editable inline.

        Returns:
            dict: Keys are field names; values are dicts with field metadata.
        """
        fields = {}
        if self.list_editable:
            for field in self.model._meta.get_fields():
                if field.name in self.list_editable:
                    fields[field.name] = {
                        'field': field,
                        'type': get_field_input_type(field),
                    }
        return fields

    def get_filter_fields(self):
        """
        Returns the filter fields metadata prepared at initialization.

        Returns:
            dict|None: Dict of filter fields or None if none configured.
        """
        if not self.filter_fields or not self._filter_fields:
            return None
        return self._filter_fields

    def get_actions(self):
        """
        Returns a list of available actions with keys and descriptions.

        Returns:
            list: Each item is a dict with 'key' and 'desc' of the action.
        """
        actions = []
        for action in self.actions:
            actions.append({
                'key': action,
                'desc': getattr(self, action)._desc
            })
        return actions

    @action(desc="Delete all instances")
    def delete(self, queryset):
        """
        Default action to delete all selected instances.

        Args:
            queryset (QuerySet): The queryset of objects to delete.
        """
        for obj in queryset:
            obj.delete()

    def get_queryset(self):
        """Return the default queryset for the managed model."""
        return self.model.objects.all()


# --------------------------
# AppAdmin: Register and manage models in an app
# --------------------------

# Used to get the global registry class to avoid cirluar import 
def get_registry():
    from .app_registry import Registry

    return Registry

class AppAdmin:
    """
    Class to manage models registered under a Django app for admin interface.
    """
    app_icon: str = ''' <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                        </svg>
                    '''

    def __init__(self, app_label: str, include_all_model=False) -> None:
        """
        Initialize AppAdmin by loading the app config and registering the app in the global registry.

        Args:
            app_label (str): The Django app label to manage.
            include_all_model (bool): If True, include all models (currently unused).
        """
        self._models = {}

        try:
            self.app = apps.get_app_config(app_label)
            self.app_label = app_label
            get_registry().register_app(self)
        except LookupError:
            raise AppNotFound(f"App with the label {app_label} not found ")

    def register_to_admin_panel(self, model: Model = None, model_admin: ModelAdmin | None = None):
        """
        Register a model or a ModelAdmin to this app's admin panel.

        Args:
            model (Model, optional): Django model class.
            model_admin (ModelAdmin, optional): A pre-configured ModelAdmin instance.

        Raises:
            ModelRegistrationConflict: If both `model` and `model_admin` are provided.
        """
        if model and model_admin:
            raise ModelRegistrationConflict()


        if model_admin and not model:
            model_admin = model_admin()
            model = model_admin.model 
        
        else:
            model_admin = ModelAdmin(model)

        model_name = model._meta.model_name.lower()
        if not self._models.get(model_name):
            self._models[model_name] = {
                'model': model,
                'model_admin': model_admin
            }

    def get_models(self):
        """Return all registered models."""
        return self._models

    def get_model(self, model: str) -> Model | None:
        """Return the model class for a given model name, or None if not registered."""
        model_obj = self._models.get(model, None)
        if model_obj is not None:
            return model_obj['model']
        return None

    def get_model_admin(self, model: str) -> ModelAdmin | None:
        """Return the ModelAdmin instance for a given model name, or None if not registered."""
        model_obj = self._models.get(model, None)
        if model_obj is not None:
            return model_obj['model_admin']
        return None
