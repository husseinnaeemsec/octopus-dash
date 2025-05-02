
from django import forms
from django.contrib.auth import get_user_model
from .conf import settings,default_settings
import importlib
from . import fields
import pathlib


User = get_user_model()





class DynamiModelForm(forms.ModelForm):
    
    fields_metadata = {}
    utils = importlib.import_module
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected super call
        widget = None
        # Optionally, you can loop through fields and print them or customize further
        for field_name, field in self.fields.items():
            # Handle SlugField
            if isinstance(field.widget, forms.TextInput) and field.__class__.__name__ == 'SlugField':
                widget = fields.ODSlugInput(field=field)

            # Handle TimeInput
            elif isinstance(field.widget, forms.TimeInput) and field.__class__.__name__ == 'TimeField':
                widget = fields.ODTimeInput(field=field)

            # Handle DateInput
            elif isinstance(field.widget, forms.DateInput) and field.__class__.__name__ == 'DateField' :
                widget = fields.ODDateInput(field=field)

            # Handle DateTimeInput
            elif isinstance(field.widget, forms.DateTimeInput) and field.__class__.__name__ == 'DateTimeField':
                print(field_name, 'Is Datetime input')
                widget = fields.ODDateTimeInput(field=field)

            elif isinstance(field.widget,forms.FileInput):
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
                widget = fields.ODTextArea()

            # Handle SelectMultiple
            elif isinstance(field.widget, forms.SelectMultiple):
                choices = getattr(field, 'choices', [])
                widget = fields.ODSelectMultiple(choices=choices)

            # Handle Select
            elif isinstance(field.widget, forms.Select):
                choices = getattr(field, 'choices', [])
                widget = fields.ODSelect(choices=choices)

            # Handle CheckboxInput
            elif isinstance(field.widget, forms.CheckboxInput):
                widget = fields.ODCheckboxInput(field=field)

            # Handle URLInput
            elif isinstance(field.widget, forms.URLInput):
                widget = fields.ODURLField()

            # If no match, continue
            else:
                continue

            if widget is not None:
                field.widget = widget
    class Meta:
        model = None
        fields = "__all__"

    
    def get_media(self):
        return self.media


form_class_fields = settings.get("USER_FORM_FIELDS",default_settings.get("USER_FORM_FIELDS"))
exclude_fields = []

if 'password' in form_class_fields:
    exclude_fields = ['password']
class UserModelForm(DynamiModelForm):
    
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
    form_class = type(f"DynamicModelForm", (DynamiModelForm,), {"Meta": Meta})
    
    return form_class


