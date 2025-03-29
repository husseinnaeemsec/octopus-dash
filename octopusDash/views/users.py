from django.views.generic import CreateView
from ..forms import NewUserModelForm,create_dynamic_model_form
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User

class NewUserView(CreateView):
    form_fields = ['username','password','groups','user_permissions']
    form_class = create_dynamic_model_form(User,form_fields)
    template_name = 'users/add_new_user.html'
    success_url = reverse_lazy("octopus:users-list")