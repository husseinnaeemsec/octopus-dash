from ...contrib.admin import registry
from ...exceptions import AppNotFound, ModelNotFound
from ...forms import DynamicFilterForm,model_form_factory

class AppContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(kwargs.get("app"))
        if not self.app:
            raise AppNotFound(f'App with label "{kwargs.get("app")}" not found')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self):
        
        context = super().get_context_data() or {}
        
        context.update({
            'app':self.app,
        })
        
        return context

class ModelContextMixin:
    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(kwargs.get("app"))
        if not self.app:
            raise AppNotFound(f'App with label "{kwargs.get("app")}" not found')

        model_name = kwargs.get("model")
        self.model = self.app.get_model(model_name)
        if not self.model:
            raise ModelNotFound(f'Model "{model_name}" not found')

        self.model_admin = self.app.get_model_admin(model_name)
        self.model_form_class = model_form_factory(self.model_admin, self.model_admin.form_fields)

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs) or {}
        
        context.update({
            'app':self.app,
            'model_admin':self.model_admin,
        })
        
        return context

    
    def get_form_class(self,*args,**kwargs):
        return self.model_form_class
    
