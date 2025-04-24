from django.db.models import Model
import inspect 
from django.apps import apps
from django.http import JsonResponse
from .conf import settings
from .forms import form_factory

class DuplicationError(Exception):
    pass

class ModelAdminMetaClass(type):
    
    __action_arguments = ('self', 'request', 'queryset')
    actions_dict = {}
    
    def __new__(cls, name, bases, clsdict):
        
        if name not in {'BaseModelAdmin'}:
            actions = clsdict.get("actions", [])
            if actions:
                for action in actions:
                    if action not in clsdict:
                        raise ValueError(f"ModelAdmin {name} has defined {action} action but it's not implemented.")
                    
                    method = clsdict[action]
                    sig = inspect.signature(method)
                    param_names = tuple(sig.parameters)
                    if param_names != cls.__action_arguments:
                        raise ValueError(f"Action {action} must have the following arguments {cls.__action_arguments}. Found: {param_names}")
                    
                    

                    
                    if not hasattr(method, 'short_desc'):
                        method.short_desc = inspect.getdoc(method).capitalize()  # Default to the action name

                    if not clsdict.get("actions_dict",None):
                        clsdict['actions_dict'] = {}
                        
                    
                    if not getattr(cls,"actions_dict",{}).get(action):
                        actions_dict = getattr(cls,"actions_dict",{})
                        actions_dict[action] = {
                            "name":action.replace("_", " ").capitalize(),
                            "desc":method.short_desc,
                        }
                        
                        clsdict['actions_dict'] = actions_dict
                        
                        
                    
        return super().__new__(cls, name, bases, clsdict)
    



class BaseModelAdmin(metaclass=ModelAdminMetaClass):
    
    def __init__(self,model:Model):
        self.model = model


class ModelAdmin(BaseModelAdmin):
    actions = ['delete_objects']
    list_display = []
    search_fields = []
    filter_fields = []
    fields = '__all__'
    icon = None
    
    def __init__(self,model:Model):
        
        self.model_search_fields = []
        self.model_filter_fields = []
        
        default_search_fields = ("CharField","TextField","JSONField","SlugField")
        default_filter_fields = ("BooleanField","DateField","DateTimeField","TimeField")

        super().__init__(model)
        
        self.form_class = form_factory(model,self.fields)
        self.meta = model._meta
        self.model_name = self.meta.model_name

        
        # Get default search fields (based on type if it's searchable or not )
        if not self.search_fields:
            for field in self.model._meta.get_fields():
                if field.get_internal_type() in default_search_fields:
                    self.model_search_fields.append(field.name)
        else:
            self.model_search_fields = self.search_fields
        if not self.filter_fields:
            for field in self.model._meta.get_fields():
                if field.get_internal_type() in default_filter_fields and field.name in self.list_display:
                    self.model_filter_fields.append({
                        'name':field.name.replace("_"," ").title(),
                        'field':field.name,
                        'type':field.get_internal_type(),
                        'is_bool':field.get_internal_type() == 'BooleanField',
                        'is_date':field.get_internal_type() == 'DateField',
                        'is_datetime':field.get_internal_type() == 'DateTimeField',
                        'is_time':field.get_internal_type() == 'TimeField'
                    })
        
        else:
            self.model_filter_fields = self.filter_fields
    
    def delete_objects(self,request,queryset):
        """ Deleting all selected users  """
        
        return JsonResponse("Deleted",safe=False)


class AppConfiguration:
    
    icon = None
    display_name = None
    

class AppRegistry:
    
    __registry = {}
    
    def __init__(self):
        pass
    
    
    def register(self,model:Model,admin=None):

        try:
            assert issubclass(model,Model),TypeError(f" model {model.__class__}  should be a subclass of django.db.models.Model  ")
        
        except (TypeError) :
            raise TypeError(f"you should not register an instance the model argument should be a subclass of django.db.models.Model ")
        
        app_config = model._meta.app_config
        
        if app_config not in self.get_registry():
            self.__registry[app_config] = {
                "models":{
                    model:{
                        "admin": admin(model) if admin is not None else ModelAdmin(model),
                        "name":model._meta.model_name,
                        "plural":model._meta.verbose_name_plural,
                    }
                },
                'app_name':app_config.label,
            }
        else:
            if not self.get_registry().get(app_config)['models'].get(model):
                self.__registry[app_config]['models'][model] = {
                    'admin':admin(model) if admin is not None else ModelAdmin(model),
                    "name":model._meta.model_name,
                    "plural":model._meta.verbose_name_plural,
                }
            else:
                raise DuplicationError(f"model ({model._meta.model_name})  is already regisrtered  ")
    
    @classmethod
    def set_app_config(cls,app_label,app_config,register_app=False):
        try:
            django_app_config = apps.get_app_config(app_label)
            app = cls.__registry[django_app_config]
            app['config'] = app_config
        except LookupError:
            raise LookupError(f"App with the label {app_label} not found")
        
        except KeyError:
            if register_app:
                cls.__registry[app_config] = {
                    'config':app_config,
                    'models':{},
                }
                
            
            else:
                raise LookupError(f'App with the label {app_label} is not registered remove the app or set register_app to True ')
    
    @classmethod
    def get_app(cls,app:str):
        
        
        if not app:
            return None
        
        app = app.rpartition(".")[-1]
        try:
            app = apps.get_app_config(app)
            
            if not cls.__registry.get(app):
                return None

            return cls.__registry.get(app)
        
        except (LookupError,KeyError):
            return None
    @classmethod
    def get_registry(cls):
        
        return cls.__registry


dashboard = AppRegistry()

