# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models import ManyToManyField


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'})
    )
    





class NewUserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ['username','password','first_name','user_permissions','last_name','groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300',
                'placeholder': field.label  # Optional: Set placeholders dynamically
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.password:  # Ensure there's a password before hashing
            user.password = make_password(user.password)
        if commit:
            user.save()
        return user


def create_dynamic_model_form(model:models.Model,fields:list):
    model_name = model._meta.label.capitalize()
    meta_class = type("Meta",(),{
        "model":model,
        "fields":fields or "__all__"
    })
    
    class DynamicModelForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.has_m2m = False  # Track if the model has M2M fields
                # Iterate through all fields and filter M2M fields only
                for field in self.Meta.model._meta.get_fields():
                    if isinstance(field, ManyToManyField):
                        self.has_m2m = True  # Mark the model as having M2M fields
                        self.fields[field.name] = forms.ModelMultipleChoiceField(
                            queryset=field.related_model.objects.all(),
                            required=False,
                            widget=forms.SelectMultiple(attrs={'class': 'm2m-select'})
                        )
            
        def save(self, commit=True):
            instance = super().save(commit=False)  # Save instance but not yet commit

            if commit:
                instance.save()  # Save the instance first
                if self.has_m2m:
                    self.save_m2m()  # Only call save_m2m if M2M fields exist

            return instance

        class Meta:
            model = None
            fields = '__all__'
    
    
    model_form = type(f"{model_name}DynamiModelForm",(DynamicModelForm,),{
        "Meta":meta_class
    })
    
    
    return model_form