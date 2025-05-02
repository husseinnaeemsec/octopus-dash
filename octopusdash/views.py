from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib import messages
from .exceptions import AppNotFound
from .views_mixin import ListViewMixin,ModelContextMixin,AppLookupMixin,ModelLookupMixin
from django.shortcuts import render
from django.db.models import ProtectedError,RestrictedError
from .django_relatedobjects_fetcher.related_objects_fetcher import RelatedObjectsCollector
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .conf import settings
from django.apps import apps
from .forms import form_factory
from .utils import get_image_creation_model
from bs4 import BeautifulSoup


from .registry import dashboard
# Create your views here.

registry = dashboard.get_registry()

class ModelListView(ListViewMixin,ListView):
    model = None
    template_name = 'octopusdash/dynamic/list.html'
    paginate_by  = 10
    context_object_name = 'objects'



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






class CreateInstanceView(ModelContextMixin,CreateView):
    template_name = 'octopusdash/dynamic/create.html'

    def get_success_url(self):
        success_action = self.request.POST.get("__success__",None)
        
        if success_action == 'save-add' and self.request.method == 'POST':
            self.success_url = reverse_lazy('create-object',args=[self.app_name,self.model_name])

        return self.success_url
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    


    def form_valid(self, form):
        # Save the object first
        response = super().form_valid(form)
        instance = self.object
        print(self.request.FILES)
        # If this model has image creation enabled
        # Now: process each Trix field to extract image references
        for field in instance._meta.fields:
            if self.model_admin.fields_config.get(field.name):
                field_config = self.model_admin.fields_config.get(field.name)
                app_label, module, model_name = field_config.get("model").split(".")

                try:
                    image_creation_model = apps.get_model(app_label, model_name)
                    image_creation_form = form_factory(image_creation_model)
                    file_field_name = field_config.get("file_field_name")
                    instance_name = field_config.get("model_field_name")

                    images = self.request.FILES.getlist(f"{field.name}_image")
                    uploaded_image_urls = []

                    for image in images:
                        data = {
                            instance_name: instance
                        }
                        files = {
                            file_field_name: image
                        }
                        form = image_creation_form(data=data, files=files)

                        if form.is_valid():
                            image_instance = form.save()
                            uploaded_image_urls.append(image_instance.image.url)  # or getattr(image_instance, file_field_name).url
                        else:
                            print("Image form errors:", form.errors)

                    # Replace placeholder <img src=""> in the original content
                    content = getattr(instance, field.name)
                    soup = BeautifulSoup(content, "html.parser")

                    for img_tag, real_url in zip(soup.find_all("img"), uploaded_image_urls):
                        img_tag["src"] = real_url

                    # Save updated content back to instance
                    setattr(instance, field.name, str(soup))
                    instance.save(update_fields=[field.name])
                except LookupError:
                    raise LookupError(f"Model with the name {field_config.get("model")} can not be found to assosiate with {field.name} ")
                except Exception as e:
                    raise Exception(f"Unknown error  {e} ")
                
        return response

class UpdateInstanceView(ModelContextMixin,UpdateView):
    template_name = 'octopusdash/dynamic/update.html'
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


class DeleteInstanceView(ModelContextMixin,DeleteView):
    template_name = 'octopusdash/dynamic/delete.html'
    error_template = 'octopusdash/errors/object_not_found.html'
    context_object_name = 'object'
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except ObjectDoesNotExist:
            return render(request, self.error_template, {'error_message': 'Object not found'})

        context = self.get_context_data()
        return self.render_to_response(context)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['related_objects'] = RelatedObjectsCollector(self.get_object())
        
        
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except ObjectDoesNotExist:
            return render(request, self.error_template, {'error_message': 'Object not found'})

        context = self.get_context_data()
        context['obj'] = self.object
        
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        
        except ProtectedError:
            return render(request, 'errors/object_protected.html', context)

        except IntegrityError:
            return render(request, 'errors/integrity_error_on_delete.html', context)

        except Exception as e:
            context['exception'] = e
            return render(request, 'errors/unknown_error.html', context)

class AppView(AppLookupMixin,View):
    
    
    def get(self,request,app,*args,**kwargs):
        return render(request,'octopusdash/dynamic/app.html')



class ModelView(ModelLookupMixin,View):
    
    
    def get(self,request,app,*args,**kwargs):
        return render(request,'octopusdash/dynamic/model.html')







def apps_view(request):
    
    
    
    
    return render(request,'octopusdash/apps_list.html')