from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib import messages
from .exceptions import AppNotFound
from .views_mixin import ListViewMixin,ModelContexttMixin
from django.shortcuts import render
from .django_relatedobjects_fetcher.related_objects_fetcher import RelatedObjectsCollector

from .registry import dashboard
# Create your views here.

registry = dashboard.get_registry()




class ModelListView(ListViewMixin,ListView):
    model = None
    template_name = 'dynamic/list.html'
    paginate_by  = 10
    context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("query")
        return context

    def get(self, request, *args, **kwargs):
        super().get(request,*args,**kwargs)
        # Set the queryset manually to avoid the object_list error
        self.object_list = self.get_queryset()
        
        paginate_by = request.GET.get("objects_per_page",self.paginate_by) 
        
        if str(paginate_by).isdigit() and int(paginate_by) >=1 and int(paginate_by) <=70:
            
            self.paginate_by = paginate_by
        

        context = self.get_context_data()  # Now this is safe
        context['app_name'] = kwargs.get("app")
        
        return self.render_to_response(context)






class CreateInstanceView(ModelContexttMixin,CreateView):
    template_name = 'dynamic/create.html'

    def get_success_url(self):
        success_action = self.request.POST.get("__success__",None)
        
        if success_action == 'save-add':
            self.success_url = reverse_lazy('create-object',args=[self.app_name,self.model_name])

        return self.success_url
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    


    def form_valid(self, form):
        # Save the new instance
        instance = form.save()
        # Add a success message with the instance's data
        messages.success(self.request, f"Successfully created {self.model._meta.verbose_name}: {instance}.")

        # Redirect to another page (could be the list view or detail view of the instance)
        return HttpResponseRedirect(self.success_url)


class UpdateInstanceView(ModelContexttMixin,UpdateView):
    template_name = 'dynamic/update.html'
    context_object_name = 'object'

    
    def get_success_url(self):
        
        
        obj = self.get_object()
        
        self.success_url = reverse_lazy("update-object",args=[self.app_name,self.model_name,obj.pk])
        
        return self.success_url


    def form_valid(self, form):
        # Save the new instance
        instance = form.save()

        # Add a success message with the instance's data
        messages.success(self.request, f"Successfully updated {self.model._meta.verbose_name}: {instance}.")

        # Redirect to another page (could be the list view or detail view of the instance)
        return super().form_valid(instance)


class DeleteInstanceView(ModelContexttMixin,DeleteView):
    template_name = 'dynamic/delete.html'
    context_object_name = 'object'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['related_objects'] = RelatedObjectsCollector(self.get_object())
        
        return context


    
    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            

            obj.delete()
            
            return HttpResponseRedirect(self.get_success_url())
        
        except Exception as e:
            print(e,"Exception")
            
            return JsonResponse(False,safe=False)

class AppView(View):
    
    def dispatch(self, request, *args, **kwargs):
        app_name = kwargs.get("app",None)
        app = dashboard.get_app(app_name)
        self.app = app
        
        if not self.app:
            raise AppNotFound(f" App not found  ")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,app,*args,**kwargs):
        return render(request,'dynamic/app.html')






def apps_view(request):
    
    
    
    
    return render(request,'apps_list.html')