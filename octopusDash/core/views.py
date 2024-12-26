from octopusDash.core.model_registry import octopus_registry
from octopusDash.core.url_registry import url_registry
from django.views.generic import TemplateView
from django.urls import path
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import generate_form



def generate_apps_views():
    app_views = []
    
    for app,models in octopus_registry.get_models_by_app().items():
        
        class AppView(TemplateView):
            
            template_name = 'apps/app.hmtl'
            
            def get_context_data(self, **kwargs):
                
                context = super().get_context_data(**kwargs)
                
                context['app'] = app
                context['models'] = models
                
                return context
            
        
        url_registry.register_app_url(app,f"{app.lower()}/",AppView)


def generate_app_view(app):
    
    class AppView(TemplateView):
        
        template_name = 'apps/app.html'

        def get_context_data(self,**kwargs):
            
            context = super().get_context_data(**kwargs)
            context['app_name'] = app
            return context
            
    
    url_registry.register_app_url(app,f"{app.lower()}",AppView)
    
    return AppView


def generate_generic_views():
    for app, models in octopus_registry.get_models_by_app().items():
        for model_class in models:
            app_name = model_class._meta.app_label.lower()
            model_name = model_class.__name__.lower()

            # List View
            class ModelListView(ListView):
                model = model_class
                template_name = f'apps/CRUD/list.html'
                context_object_name = 'objects'
                

            # Register List View
            url_registry.register_model_url(
                model_class,
                f"{app_name}/{model_name}/list/",
                ModelListView,
                name=f"{app_name}-{model_name}-list"
            )

            # Create View
            class ModelCreateView(CreateView):
                model = model_class
                template_name = f'apps/CRUD/create.html'
                success_url = reverse_lazy(f'{app_name}-{model_name}-create')
                form_class  = generate_form(model_class)

            # Register Create View
            url_registry.register_model_url(
                model_class,
                f"{app_name}/{model_name}/create/",
                ModelCreateView,
                name=f"{app_name}-{model_name}-create",
            )

            # Update View
            class ModelUpdateView(UpdateView):
                model = model_class
                fields = '__all__'
                template_name = f'apps/CRUD/form.html'
                success_url = reverse_lazy(f'{app_name}-{model_name}-list')

            # Register Update View
            url_registry.register_model_url(
                model_class,
                f"{app_name}/{model_name}/update/<int:pk>/",
                ModelUpdateView,
                name=f"{app_name}-{model_name}-update"
            )

            # Detail View
            class ModelDetailView(DetailView):
                model = model_class
                template_name = f'apps/detail.html'
                context_object_name = 'object'

            # Register Detail View
            url_registry.register_model_url(
                model_class,
                f"{app_name}/{model_name}/detail/<int:pk>/",
                ModelDetailView,
                name=f"{app_name}-{model_name}-detail"
            )

            # Delete View
            class ModelDeleteView(DeleteView):
                model = model_class
                template_name = f'apps/confirm_delete.html'
                success_url = reverse_lazy(f'{app_name}-{model_name}-list')

            # Register Delete View
            url_registry.register_model_url(
                model_class,
                f"{app_name}/{model_name}/delete/<int:pk>/",
                ModelDeleteView,
                name=f"{app_name}-{model_name}-delete"
            )


# Call this function after registering all models
generate_generic_views()


