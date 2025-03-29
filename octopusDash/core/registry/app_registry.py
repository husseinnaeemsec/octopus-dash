from django.apps import AppConfig
from django.db.models import Model
from ..views import dynamic_model_views
from ...core.utils import DictToObject
from django.urls import reverse_lazy
from django.apps import apps

class DublicationError(Exception):
    pass

class ModelAdmin:
    permssion_classes= []    
    page_title = None
    paginate_by = 10
    search_fields = []
    filter_fields = []
    display_fields = []
    readonly_fields = []
    urlpatterns = []
    model_form_fields = "__all__"
    model_form_exclude = []
    
    def __init__(self,model:Model,app,**kwargs):
        
        self.label = model._meta.label.split(".")[-1].lower()
        self.app_label = app.label
        self.model = model
        self.verbose_name = model._meta.verbose_name
        self.verbose_name_plural = model._meta.verbose_name_plural
        self.urlpatterns = []
        self.search_fields = kwargs.get('search_fields', self.search_fields)
        self.filter_fields = kwargs.get('filter_fields', self.filter_fields)
        self.display_fields = kwargs.get('display_fields', self.display_fields)
        self.readonly_fields = kwargs.get('readonly_fields', self.readonly_fields)
        self.model_form_fields = kwargs.get('model_form_fields',self.model_form_fields)
        self.model_form_exclude = kwargs.get('model_form_exclude',self.model_form_exclude)
        self.page_title = kwargs.get('page_title',self.page_title if self.page_title else self.label.title())
        self.__view_urls = {}
        self.generate_views()
    
    def get_view(self,view,pk=None):
        
        if pk:
            return reverse_lazy(f"octopus:{view.view_name}",args=[pk])
        
        return reverse_lazy(f"octopus:{view.view_name}")
    
    def get_view_urls(self):
        view_urls = {}
        
        for view in self.views:
            if not view_urls.get(view.view_name) and not view.required_pk:
                view_urls[view.view_name] = {
                    'text':view.view_name.title().replace("-"," "),
                    'url':self.get_view(view)
                }
                


        return view_urls
        
    def generate_views(self):
        
        self.views = [
            dynamic_model_views.DynamicModelView(self),
            dynamic_model_views.DynamicListView(self),
            dynamic_model_views.DynamicCreateView(self),
            dynamic_model_views.DynamicUpdateView(self),
            dynamic_model_views.DynamicDeleteView(self),
            dynamic_model_views.DynamicDetailView(self),
        ]
        
        for view in self.views:
            self.urlpatterns.append(view.path())
            

    

class DashboardApp:
    
    '''
    ## DashboardApp
    
    Dashboard app is responsible for registering Django applications to OctopusDash dashboard
    
    '''
    
    __apps = {}
    __apps_count = 0
    __models_count = 0
    
    page_title = None
    permssion_classes = []
    enable_res_middleware = False
    urlpatterns = []
    
    @classmethod
    def _add_app_to_registry(cls,app):
        
        assert isinstance(app,cls),"app must be an instance of DashboardApp"
        
        if not cls.__apps.get(app.label,None) :
            
            cls.__apps[app.label] = app
            cls.__apps_count += 1
        
        else:
            raise DublicationError("App %s already exists" % app.label.title())
    
    @classmethod
    def increment_models_count(cls):
        cls.__models_count += 1      
    
    @classmethod
    def get_cls_models_count(cls):
        return cls.__models_count
    
    def __init__(self, app_config: AppConfig,**kwargs):
        self.models = {}
        self.app_config = app_config
        self.label = app_config.name.lower()
        self.page_title = self.label.title()
        self.app = apps.get_app_config(app_config.name)
        self.url = f"{self.label}/"
        self.view_name = self.label
        self.__create_app_views()
        self.id = self.get_apps_count()+1
        self.__get_app_models()
        
        if kwargs.get("enable_res_middleware", False):
            self.enable_res_middleware = True
        
        DashboardApp._add_app_to_registry(self)
    
    def __db_info(self):
        db_info = {
            "tables_count":0,
            "models_count":0,
            "registred_models_count":0,
            "models_table_info":{
                
            }
        }
        
        try:
            app_config = apps.get_app_config(self.app_config.name)
            for model_name,model in app_config.models.items():
                model_name = model_name.split('.')[-1].lower()
                db_info['tables_count'] += 1
                db_info['models_count'] += 1
                if self.models.get(model_name,None) is not None:
                    
                    db_info['registred_models_count'] += 1
                    
                db_info['models_table_info'][model_name] = {
                    'name':model._meta.label,
                    'verbose_name':model._meta.verbose_name,
                    'verbose_name_plural':model._meta.verbose_name_plural,
                    'fields':[field.name for field in model._meta.fields],
                    'db_table':model._meta.db_table
                }
        
        except KeyError:
            pass
        
        
        self.db_info = db_info
        
    
    def __get_app_models(self):
        models = []
        try:
            app_config = apps.get_app_config(self.app_config.name)
            
            for model in app_config.get_models():
                models.append(model)
                self.app_models = models
        except:
            self.app_models = []
    
    
    def get_models_table(self):
        data = []
        
        try:
            app_config = apps.get_app_config(self.app.name)
            
            for model in app_config.get_models():
                model_name = model.__name__.lower()
                fields = []
                
                for field in model._meta.get_fields():
                    fields.append({
                            'name':str(field.name),
                            'type':field.__class__.__name__,
                            
                        })

                model_data = DictToObject({
                    'name':str(model.__name__),
                    'registred':self.models.get(model_name,None) is not None, 
                    'fields': fields
                })
        
                data.append(model_data)
        except:
            pass
        
        
        return data
    
    def __create_app_views(self):
        view = dynamic_model_views.DynamicAppView(self)
        config_view = dynamic_model_views.DynamicAppConfigView(self)
        self.view_url = [reverse_lazy(self.view_name)]
        self.urlpatterns.append(view.path())
        self.urlpatterns.append(config_view.path())
    
    def register(self,model:Model,modelAdmin:ModelAdmin=None):
        app_label, model_name = model._meta.label_lower.split(".")        
        if not self.models.get(model_name):
            self.models[model_name] = {
                'model_object':model,
                'model_config': modelAdmin(model,self) if modelAdmin is not None else ModelAdmin(model,self)
            }

            self.__db_info()
            DashboardApp.increment_models_count()
            
            
        else:
            raise DublicationError("Model %s already registered in app %s" % (model_name.title(), self.label.title()))
    
    
    @classmethod
    def get_model_config(cls,app_name,model_name):
        app_name = app_name.lower()
        model_name = model_name.lower()
        
        if app_name in cls.__apps:
            if model_name in cls.__apps[app_name].models:
                return cls.get_registry().get(app_name).models.get(model_name).get("model_config")
            else:
                raise DublicationError("Model %s not found in app %s" % (model_name.title(), app_name.title()))

    @classmethod
    def get_apps_count(cls):
        return cls.__apps_count
    @classmethod
    def get_registry(cls):
        return cls.__apps

    @property
    def models_count(self):
        return len(self.models.keys())

    @classmethod
    def get_app(cls,name):
        return cls.__apps.get(name.lower(),None)
    
    @classmethod
    def get_middleware_apps(cls):
        _apps = []
        
        for app in cls.get_registry().values():
            if app.enable_res_middleware:
                _apps.append(app)
        
        return _apps
        
        

    def __repr__(self):
        return "DashboardApp(%s)" % self.label.title()
    
    


app_registry = DashboardApp.get_registry()
models_count = DashboardApp.get_cls_models_count()
