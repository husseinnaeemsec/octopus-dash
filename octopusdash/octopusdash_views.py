from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView,UpdateView,View
from django.contrib.auth import get_user_model
from .registry import ODModelAdmin
from .views_mixin import SearchFilterMixin
from .forms import UserModelForm
from .models import Field
User = get_user_model()


class ShowFields(View):
    
    def get(self,request):
        fields = Field.objects.all()
        return render(request,'octopusdash/test__show_fields.html',{'fields':fields})

class UpdateUserView(UpdateView):
    model = User
    form_class = UserModelForm
    template_name = 'octopusdash/users/update_user.html'
    
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, f"Successfully updated {self.model._meta.verbose_name}: {instance}.")
        return super().form_valid(form)

class UserAdmin(ODModelAdmin):
    list_display = ['username','is_superuser','is_staff','first_name','last_name','email','is_active']

class UserListView(SearchFilterMixin,ListView):
    model = User
    queryset = User.objects.all()
    model_admin = UserAdmin(User)
    model_name = User._meta.model_name
    app_name = User._meta.app_label
    paginate_by = 10
    context_object_name = 'users'
    template_name = 'octopusdash/users/users_list.html'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model_name
        context['app_name'] = self.app_name
        context['model_admin'] = self.model_admin
        
        return context

def login_view(request):
    if request.method == "POST":
        username_field = User.USERNAME_FIELD or 'username' # in case the user has not set or remove this field 
        # Getting the username value&argument from the USERNAME_FIELD attribute on the User Model class 
        username = request.POST.get(username_field,None)
        username_kwarg = {username_field:username}
        # Password
        password = request.POST.get("password")

        user = authenticate(request,**username_kwarg, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect("octopusdash-dashboard")  # update route as needed
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
                # optional: logout just in case
                logout(request)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "octopusdash/authentication/login.html")


def dashboard_view(request):
    return render(request,'octopusdash/index.html')
