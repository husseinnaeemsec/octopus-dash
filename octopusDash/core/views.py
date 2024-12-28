from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView,TemplateView


class DynamicViews:
    
    
    @classmethod
    def create_app_view(self,app,template=None,**kwargs):
        
        class AppView(TemplateView):
            
            template_name = template or 'apps/app.html'
            
            def get_context_data(self,**kwargs):
                
                context = super().get_context_data(**kwargs)
                context['app_name'] = app

                
                return context
        
        return AppView
        
    
    def create_model_view(registry_object):
        
        class ModelView(TemplateView):
            
            model = registry_object.model
            template_name = 'apps/model.html'

            def get_context_data(self, **kwargs):
                
                context = super().get_context_data(**kwargs)
                context['app_name'] = registry_object.model._meta.app_label.lower()
                context['model_name'] = registry_object.model.__name__.lower()
                
                
                return context
        
        return ModelView
    
    def create_view(registry_object):
        
        class ModelCreateView(CreateView):
            
            template_name = 'apps/CRUD/create.html'
            form_class = registry_object.form_class
            success_url = registry_object.success_url            
            
            def post(self, request, *args, **kwargs):
                return super().post(request, *args, **kwargs)
            
            def get_context_data(self, **kwargs):
                
                context = super().get_context_data(**kwargs)
                
                
                return context
        
        
        return ModelCreateView
    
    def list_view(registry_object, **kwargs):
        class ModelListView(ListView):
            model = registry_object.model
            template_name = 'apps/CRUD/list.html'
            context_object_name = 'objects'
            paginate_by = kwargs.get('paginate_by', 10) if kwargs.get('paginate_by',10) <= 50 else 10 

            def get_context_data(self, **kwargs):
                print(registry_object)
                context = super().get_context_data(**kwargs)
                context['object_headers'] = registry_object.object_headers
                context['app_name'] = registry_object.model._meta.app_label.lower()
                context['model_name'] = registry_object.model.__name__.lower()
                
                
                return context     

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
            template_name = 'apps/CRUD/detail.html'
            context_object_name = 'object'


        
        return ModelDetailView
    
    def delete_view(registry_object, **kwargs):
        
        class ModelDeleteView(DeleteView):
            
            model = registry_object.model
            template_name = 'apps/CRUD/delete.html'
            success_url = registry_object.success_url


        
        return ModelDeleteView
    
    