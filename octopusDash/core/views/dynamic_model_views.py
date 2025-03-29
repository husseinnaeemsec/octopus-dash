from django.views.generic import (ListView,CreateView,DeleteView,DetailView,UpdateView,TemplateView)
from ..permissions import PermissionMixin,IsAdmin
from ..forms.dynamic_forms import generate_model_form
from ..forms.app_forms import AppConfigModelForm,AppConfig
from django.shortcuts import render
from django.urls import path as django_path,reverse_lazy
from . import DynamicView
from ...models import ResourcesAccessLog
from ...core.utils import convert_size_to_mb
from django.utils.module_loading import import_string

class DynamicListView(DynamicView):
    
    def __init__(self,model_admin,*args, **kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/list/"
        self.view_name = f"list-{self.model_name}"
        self.template_name = "pages/list.html"
        
        

    def view(self):
        
        model_name = self.model_name
        
        class ModelListView(PermissionMixin,ListView):
            model = self.model
            template_name = self.template_name
            paginate_by = self.model_admin.paginate_by
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            model_admin = self.model_admin
            context_object_name = 'objects'

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                object_headers = []
                if len(self.model_admin.display_fields) > 0:
                    for field_name in self.model_admin.display_fields:
                        try:
                            self.model._meta.get_field(field_name)
                            object_headers.append(field_name)
                        except Exception as e:
                            continue
                else:
                    for field in self.model._meta.fields:
                        object_headers.append(field.name)

                context["object_headers"] = object_headers
                context['model_name'] = model_name
                
                return context
        
        return ModelListView
    
    
    def path(self):
        
        view_path = django_path(self.url,self.view().as_view(),name=self.view_name)
                
        return view_path

class DynamicCreateView(DynamicView):
    
    def __init__(self,model_admin,**kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/create/"
        self.view_name = f"create-{self.model_name}"
        self.template_name = "pages/create.html"
        self.form_class = generate_model_form(
            model_admin.model,
            fields=model_admin.model_form_fields,
            exclude=model_admin.model_form_exclude,
            readonly_fields=model_admin.readonly_fields,
            )


    def view(self):
        class ModelCreateView(PermissionMixin,CreateView):
            model = self.model
            form_class = self.form_class
            template_name = self.template_name
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            success_url = reverse_lazy(f"octopus:{self.view_name}")
            

        return ModelCreateView
    
    
    def path(self):
        
        view_path = django_path(self.url,self.view().as_view(),name=self.view_name)
                
        return view_path

class DynamicUpdateView(DynamicView):
    
    def __init__(self,model_admin,**kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/update/<int:pk>/"
        self.view_name = f"update-{self.model_name}"
        self.required_pk = True
        self.template_name = "pages/update.html"
        self.form_class = generate_model_form(
            model_admin.model,
            fields=model_admin.model_form_fields,
            exclude=model_admin.model_form_exclude
            )
    
    def view(self):
        class ModelUpdateView(PermissionMixin,UpdateView):
            model = self.model
            form_class = self.form_class
            template_name = self.template_name
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            success_url = '/'
            
            
            
            
        return ModelUpdateView
    
    
    def path(self):
        return django_path(self.url,self.view().as_view(),name=self.view_name)

class DynamicDeleteView(DynamicView):
    
    def __init__(self,model_admin,**kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/delete/<int:pk>/"
        self.view_name = f"delete-{self.model_name}"
        self.required_pk = True
        self.template_name = "pages/delete.html"
    
    def view(self):
        class ModelDeleteView(PermissionMixin,DeleteView):
            model = self.model
            template_name = self.template_name
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            
        return ModelDeleteView
    
    
    def path(self):
        return django_path(self.url,self.view().as_view(),name=self.view_name)

class DynamicDetailView(DynamicView):
    
    def __init__(self,model_admin,**kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/<int:pk>/"
        self.view_name = f"detail-{self.model_name}"
        self.required_pk = True
        self.template_name = "pages/detail.html"

    def view(self):
        class ModelDetailView(PermissionMixin,DetailView):
            model = self.model
            template_name = self.template_name
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            
        return ModelDetailView

    def path(self):
        return django_path(self.url,self.view().as_view(),name=self.view_name)

class DynamicModelView(DynamicView):

    
    def __init__(self,model_admin,**kwargs):
        
        super().__init__(model_admin,**kwargs)
        self.url = f"{self.app_name}/{self.model_name}/"
        self.view_name = self.model_name + '-view'
        self.template_name = 'pages/model.html'
    
    def view(self):
        class ModelView(PermissionMixin,TemplateView):
            template_name = self.template_name
            permission_classes = self.model_admin.permssion_classes or [IsAdmin]
            
        return ModelView
    
    def path(self):
        return django_path(self.url,self.view().as_view(),name=self.view_name)

class DynamicAppView:

    def __init__(self,app,view_name=None,url=None,**kwargs):
        self.app = app
        if not view_name or not url:
            self.url = f"{app.label}/"
            self.view_name = app.label
        
        else:
            self.url = url
            self.view_name = view_name
        
        self.template_name = 'pages/app.html'
    

    def view(self):
        app = self.app
        class AppView(PermissionMixin,TemplateView):
            template_name = self.template_name
            permission_classes = [IsAdmin]
            
            def get_context_data(self, **kwargs):
                context  = super().get_context_data(**kwargs)
                context['app_name'] = app.label
                models_list = [model_name for model_name in app.models.keys()]
                context['models'] = models_list
                context['models_count'] = len(models_list)
                context['app_info'] = import_string("octopusDash.core.registry.DashboardApp").get_app(app.label)
                
                return context
            
        return AppView
    
    def path(self):
        return django_path(self.url,self.view().as_view(),name=self.view_name)

class DynamicAppConfigView:
    
    def __init__(self,app,url=None,**kwargs):
        self.app = app
    
    def view(self):
        app = self.app
        description = "This is default app description for the app %s" %app.label.capitalize()
        class AppConfigView(TemplateView):
            
            template_name = 'pages/app_config.html'
            
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                return context
            
            def get(self,request):
                
                return render(request,self.template_name,self.get_context_data())
            
            def post(self,request):
                
                form = AppConfigModelForm(request.POST,instance=self.app_config_object)
                
                if form.is_valid():
                    config = form.save(commit=False)
                    config.app_id = app.label
                    config.save()
                    
                    return render(request,self.template_name,self.get_context_data())
                
                
                return render(request,self.template_name,self.get_context_data())
            
        
        return AppConfigView
    
    def path(self):
        return django_path(f"{self.app.label}/config/",self.view().as_view(),name=f"config-{self.app.label}")