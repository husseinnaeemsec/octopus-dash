from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.apps import apps
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from .utils import get_model_admin
from django.db.models import Q
from .exceptions import AppNotFound
from .forms import form_factory
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout

from .registry import dashboard
# Create your views here.

registry = dashboard.get_registry()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("octopusdash-dashboard")  # update route as needed
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
                # optional: logout just in case
                logout(request)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "authentication/login.html")


def dashboard_view(request):
    return render(request,'index.html')


def apps_view(request):
    
    
    
    return render(request,'apps_list.html')

class ModelContexttMixin:
    
    model = None
    model_name = None
    app_name = None
    model_admin = None
    queryset = None
    
    


    
    def dispatch(self, request, *args, **kwargs):
        # Fetch app and model from kwargs
        app_name = kwargs.get("app", None)
        model_name = kwargs.get("model_name", None)
        
        if app_name and model_name:
            try:
                app_config = apps.get_app_config(app_name)
                try:
                    self.model = app_config.get_model(model_name)
                    if not self.model:
                        raise ValueError(f"Model '{model_name}' not found.")
                except (KeyError, LookupError, ValueError) as e:
                    self.model = None
                    self.error_message = str(e)  # Store error message to show it later
            except LookupError:
                self.model = None
                self.error_message = f"App '{app_name}' not found or not installed."

        # If model is found, set the queryset, model admin, and other properties
        if self.model:
            self.queryset = self.model.objects.all().order_by('id')
            self.model_admin = get_model_admin(self.model._meta.app_config, self.model)
            self.app_name = self.model._meta.app_config.label
            self.model_name = self.model._meta.model_name
            success_action = request.POST.get("__success__",None)            
            self.form_class = form_factory(self.model)
            
            if success_action == 'save-add':
                self.success_url = reverse_lazy(f"create-object",args=[app_name,model_name])
            else:
                self.success_url = reverse_lazy(f"list-objects",args=[app_name,model_name])
        

        
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        # Use the queryset set in dispatch, or fallback
        if hasattr(self, 'queryset'):
            return self.queryset
        return super().get_queryset()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.model is not None:
            context['app_name'] = self.app_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
            context['model_name'] = self.model._meta.verbose_name
            context['model_admin'] = self.model_admin
            context['model'] = self.model
            context['objects_count'] = self.get_queryset().count()

        return context

class ModelListView(ModelContexttMixin,ListView):
    model = None
    template_name = 'dynamic/list.html'
    paginate_by  = 10
    context_object_name = 'objects'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("search", None)
        search_fields = self.model_admin.search_fields

        if query and search_fields:
            q_object = Q()
            for field in search_fields:
                q_object |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(q_object)

        return queryset
        
    def get(self, request, *args, **kwargs):
        super().get(request,*args,**kwargs)
        # Set the queryset manually to avoid the object_list error
        self.object_list = self.get_queryset()
        
        paginate_by = request.GET.get("objects_per_page",10)
        
        if str(paginate_by).isdigit() and int(paginate_by) >=1 and int(paginate_by) <=70:
            
            self.paginate_by = paginate_by
        

        context = self.get_context_data()  # Now this is safe
        context['app_name'] = kwargs.get("app")
        
        return self.render_to_response(context)



class UpdateModelView(ModelContexttMixin,UpdateView):
    
    model = None
    template_name = 'dynamic/list.html'
    
    
    def get(self, request,*args, **kwargs):
        
        self.app_config = apps.get_app_config(kwargs.get("app"))
        self.model = self.app_config.get_model(kwargs.get("model_name"))
        
        
        return super().get(request, *args, **kwargs)


class CreateInstanceView(ModelContexttMixin,CreateView):
    template_name = 'dynamic/create.html'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    


    def form_valid(self, form):
        # Save the new instance
        instance = form.save()

        # Add a success message with the instance's data
        messages.success(self.request, f"Successfully created {self.model._meta.verbose_name}: {instance}.")

        # Redirect to another page (could be the list view or detail view of the instance)
        return HttpResponseRedirect(self.success_url)


class UpdateInstanceView(ModelContexttMixin,CreateView):
    template_name = 'dynamic/update.html'

    


    def form_valid(self, form):
        # Save the new instance
        instance = form.save()

        # Add a success message with the instance's data
        messages.success(self.request, f"Successfully updated {self.model._meta.verbose_name}: {instance}.")

        # Redirect to another page (could be the list view or detail view of the instance)
        return HttpResponseRedirect(self.success_url)


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