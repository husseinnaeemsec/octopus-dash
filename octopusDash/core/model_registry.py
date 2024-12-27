from django.apps import apps
from django.db.models import Model
from django.urls import reverse
from octopusDash.core.forms import generate_form
from django.apps import AppConfig
from octopusDash.core.views import DynamicViews
from octopusDash.core import DictToObject
from django.urls import path
class RegistryObject:
    
    
    
    def __init__(self,model:Model,**kwargs):
        self.model = model
        self.kwargs = kwargs
        self.model_name = self.model.__name__.lower()
        self.app_label = self.model._meta.app_label.lower()
        self.form_class = generate_form(model,**kwargs)
        self.model_view_url = f"{self.app_label}/{self.model.__name__.lower()}/"
        self.app_view = f"{self.app_label}/"
        self.model_base_view_name = f"{self.app_label}-{self.model.__name__.lower()}"
        self.search_fields = self.kwargs.get('search_fields', [])
        self.model_permssions = self.kwargs.get("permssions",[])
        self.model_icon = self.kwargs.get('icon',None)
        self.success_url = self.kwargs.get('success_url','/dashboard')
        self.object_headers = self.kwargs.get("display_fields",[field.name for field in self.model._meta.get_fields()])
        self.url_patterns = DictToObject({
            'create':self.model_view_url+'create/',
            'list':self.model_view_url+'list/',
            'update':self.model_view_url+'update/<int:pk>/',
            'detail':self.model_view_url+'detail/<int:pk>/',
            'delete':self.model_view_url+'delete/<int:pk>/',
            'search':self.model_view_url+'search/'
        })
        self.routes_view_name = DictToObject({
            'create':f"{self.app_label}-{self.model.__name__.lower()}-create",
            'list':f"{self.app_label}-{self.model.__name__.lower()}-list",
            'update':f"{self.app_label}-{self.model.__name__.lower()}-update",
            'detail':f"{self.app_label}-{self.model.__name__.lower()}-detail",
            'delete':f"{self.app_label}-{self.model.__name__.lower()}-delete",
            'search':f"{self.app_label}-{self.model.__name__.lower()}-search"
        })

    @classmethod
    def get_model_view(self,app_name,model_name,viewname,**kwargs):
        
        pk = kwargs.get("pk")
        
        url = reverse(f"{app_name}-{model_name}-{viewname}",kwargs={'pk':pk})
        
        
        return url
    
    @classmethod
    def get_app_view(self,app_name,viewname,**kwargs):
        
        return reverse(f"{app_name}-{viewname}",**kwargs)

    
    def get_model_routes(self):
        

        
        class ModelRoutes:
            
            create = path(self.url_patterns.create,DynamicViews.create_view(self).as_view(),name=self.routes_view_name.create)
            list = path(self.url_patterns.list, DynamicViews.list_view(self).as_view(),name=self.routes_view_name.list)
            update = path(self.url_patterns.update, DynamicViews.update_view(self).as_view(),name=self.routes_view_name.update)
            detail = path(self.url_patterns.detail, DynamicViews.detail_view(self).as_view(),name=self.routes_view_name.detail)
            delete = path(self.url_patterns.delete, DynamicViews.delete_view(self).as_view(),name=self.routes_view_name.delete)
            search = path(self.url_patterns.search, DynamicViews.list_view(self).as_view(),name=self.routes_view_name.search)
        
        return ModelRoutes()

    def get_urlpatterns(self):
        
        routes = self.get_model_routes()
        
        patterns = [routes.create, routes.list,routes.update, routes.delete,routes.detail,routes.search]
        
        return patterns
    


class AppRegistryObject:
    
    def __init__(self,app_config:AppConfig,**app_kwargs):
        self.app_name = app_config.name.split('.')[-1].lower()
        self.view_path = f"apps/{self.app_name}"
        self.url_patterns = DictToObject({
            'settings':f"{self.view_path}/settings/",
            'app':f"{self.view_path}/",
            "access":f"{self.view_path}/access/",
        })
        
        self.routes_view_name = DictToObject({
            'settings':f"{self.app_name}-settings",
            'app':f"{self.app_name}",
            'access':f"{self.app_name}-access",
        })
        
    
    def get_app_routes(self):

                
        class AppRoutes:

            settings = path(self.url_patterns.settings,DynamicViews.create_app_view(self.app_name,'apps/settings.html').as_view(),name=self.routes_view_name.settings)
            app = path(self.url_patterns.app, DynamicViews.create_app_view(self.app_name).as_view(),name=self.routes_view_name.app)
            access = path(self.url_patterns.access, DynamicViews.create_app_view(self.app_name,'apps/access.html').as_view(),name=self.routes_view_name.access)
            

        return AppRoutes()
    
    def get_urlpatterns(self):
        
        routes = self.get_app_routes()
        
        patterns = [routes.app,routes.settings,routes.access]
        
        return patterns

class Registry:
    def __init__(self):
        # Initialize an empty dictionary to store models grouped by app name
        self.registry = {}
        
    
    def register_model(self,model,**kwargs):
        
        app_label = model._meta.app_label.split('.')[-1].lower()
        if not self.registry.get(app_label):
            self.registry[app_label] = {
                'app': app_label,
                'app_registry_object':AppRegistryObject(model._meta.app_config) ,
                'models':[RegistryObject(model,**kwargs)]
            }
            
            
        
        else:
            object = RegistryObject(model,**kwargs)
            if object not in self.registry[app_label]['models']:
                self.registry[app_label]['models'].append(object)
            
            else:
                raise ValueError(f"Model {model.__name__} already registered in app {app_label}")


octopus_registry = Registry()