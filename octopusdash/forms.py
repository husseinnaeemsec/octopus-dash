
from django import forms
from django.contrib.auth import get_user_model
from .conf import settings,default_settings
import importlib
from . import fields
import pathlib


User = get_user_model()




class DynamicModelForm(forms.ModelForm):
    
    fields_metadata = {}
    utils = importlib.import_module
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected super call

        # Loop through the form fields to dynamically set widgets
        for field_name, field in self.fields.items():
            
            widget = None
            # Handle SlugField
            if isinstance(field.widget, forms.TextInput) and field.__class__.__name__ == 'SlugField':
                widget = fields.ODSlugInput(field=field)

            # Handle TimeInput
            elif isinstance(field.widget, forms.TimeInput) and field.__class__.__name__ == 'TimeField':
                widget = fields.ODTimeInput(field=field)

            # Handle DateInput
            elif isinstance(field.widget, forms.DateInput) and field.__class__.__name__ == 'DateField':
                widget = fields.ODDateInput(field=field)

            # Handle DateTimeInput
            elif isinstance(field.widget, forms.DateTimeInput) and field.__class__.__name__ == 'DateTimeField':
                widget = fields.ODDateTimeInput(field=field)

            # Handle FileInput
            elif isinstance(field.widget, forms.FileInput):
                widget = fields.ODFileInput(field=field)

            # Handle other TextInput fields (default)
            elif isinstance(field.widget, forms.TextInput):
                widget = fields.ODTextInput(field=field)

            # Handle NumberInput
            elif isinstance(field.widget, forms.NumberInput):
                widget = fields.ODNumberInput(field=field)

            # Handle NullBooleanSelect (CheckboxSwitchInput)
            elif isinstance(field.widget, forms.NullBooleanSelect):
                widget = fields.ODCheckboxSwitchInput(field=field)

            # Handle EmailInput
            elif isinstance(field.widget, forms.EmailInput):
                widget = fields.ODEmailInput(field=field)

            # Handle Textarea
            elif isinstance(field.widget, forms.Textarea):
                widget = fields.ODTextArea(field=field)

            # Handle SelectMultiple
            elif isinstance(field.widget, forms.SelectMultiple):
                choices = getattr(field, 'choices', [])
                widget = fields.ODSelectMultiple(choices=choices,field=field)

            # Handle Select
            elif isinstance(field.widget, forms.Select):
                choices = getattr(field, 'choices', [])
                widget = fields.ODSelect(choices=choices,field=field)

            # Handle CheckboxInput
            elif isinstance(field.widget, forms.CheckboxInput):
                widget = fields.ODCheckboxInput(field=field)

            # Handle URLInput
            elif isinstance(field.widget, forms.URLInput):
                widget = fields.ODURLField(field=field)

            # If no match, continue to the next field
            if widget is not None:
                field.widget = widget
                

    class Meta:
        model = None
        fields = "__all__"

    def get_media(self):
        # Ensure that any media (JS, CSS) related to the widgets is included
        return self.media

    def clean(self):
        cleaned_data = super().clean()
        self._files_to_remove = [] 
        for field_name, field in self.fields.items():
            if isinstance(field, (forms.FileField,forms.ImageField)):
                remove_flag = f"{field_name}_removefile"
                print(self.data)
                if self.data.get(remove_flag) == '1':
                    cleaned_data[field_name] = None
                    self._files_to_remove.append(field_name)
        return cleaned_data



form_class_fields = settings.get("USER_FORM_FIELDS",default_settings.get("USER_FORM_FIELDS"))
exclude_fields = []

if 'password' in form_class_fields:
    exclude_fields = ['password']
class UserModelForm(DynamicModelForm):
    
    class Meta:
        model = User
        fields = form_class_fields
        exclude = exclude_fields

# Form factory function
def form_factory(model, fields='__all__'):
    # Dynamically create a Meta class
    cls_model = model
    cls_fields = fields
    class Meta:
        model = cls_model
        fields = cls_fields
    
    # Dynamically create a form class with the dynamic Meta class
    form_class = type(f"DynamicModelForm", (DynamicModelForm,), {"Meta": Meta})
    
    return form_class


