from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView,TemplateView


class DynamicViews:
    
    
    @classmethod
    def create_app_view(self,app,**kwargs):
        
        class AppView(TemplateView):
            
            template_name = 'apps/app.html'
            
            def get_context_data(self,**kwargs):
                
                context = super().get_context_data(**kwargs)
                context['app_name'] = app

                
                return context
        
        return AppView
        
    
    def create_view(registry_object):
        
        class ModelCreateView(CreateView):
            
            template_name = 'apps/CRUD/create.html'
            form_class = registry_object.form_class
            success_url = registry_object.success_url            
            
            def get_context_data(self, **kwargs):
                
                context = super().get_context_data(**kwargs)
                
                
                return context
        
        
        return ModelCreateView
    
    def list_view(registry_object, **kwargs):
        
        class ModelListView(ListView):
            
            model = registry_object.model
            template_name = 'apps/CRUD/list.html'
            context_object_name = 'objects'
        
        
        return ModelListView
    
    def update_view(registry_object, **kwargs):
        
        class ModelUpdateView(UpdateView):
            
            model = registry_object.model
            template_name = 'apps/CRUD/update.html'
            form_class = registry_object.form_class
            success_url = registry_object.success_url
            
            
            def get_context_data(self, **kwargs):
                
                context = super().get_context_data(**kwargs)
                
                
                return context
        
        
        return ModelUpdateView
    
    def detail_view(registry_object, **kwargs):
        
        class ModelDetailView(DetailView):
            
            model = registry_object.model
            template_name = 'apps/detail.html'
            context_object_name = 'object'


        
        return ModelDetailView
    
    def delete_view(registry_object, **kwargs):
        
        class ModelDeleteView(DeleteView):
            
            model = registry_object.model
            template_name = 'apps/CRUD/delete.html'
            success_url = registry_object.success_url


        
        return ModelDeleteView
    
    