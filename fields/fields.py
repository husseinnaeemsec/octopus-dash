from django import forms
from django.utils.text import slugify
from datetime import datetime

INPUTS_STYLE_FILE = 'od/css/components/inputs/inputs.min.css'

class ODInput:
    
    ''' Base <input /> field takes styles from INPUTS_STYLE_FILE for common fields '''

    def __init__(self, *args,field=None,data=None, help_text=None, **kwargs):
        self.help_text = ''
        self.field = field
        self.data = data
        if field is not None and not help_text:
            self.help_text = field.help_text or help_text
        elif help_text:
            self.help_text = help_text
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Ensure value is a list
        if self.field is not None:
            context['widget']['maxlength'] = getattr(self.field,'max_length',None)
            context['widget']['field_type'] = self.field.__class__.__name__

        if self.data is not None:
            context['widget']['data'] = self.data
        
        context['choices'] = list(self.choices) if hasattr(self,'choices') else None
        context['widget']['help_text'] = self.help_text 
        context['widget']['value'] = value
        context['widget']['type'] = getattr(self,'input_type','')
        context['widget']['label'] = context['widget']['name'].replace("_"," ").title()
        return context

    
    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE]
        }


class ODDateFilterField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convert the raw input value to a Python list of dates.
        Expected format: 'YYYY-MM-DD&YYYY-MM-DD'
        """
        if not value:
            return []

        try:
            parts = value.split("&")
            dates = [
                datetime.strptime(part.strip(), "%Y-%m-%d").date()
                for part in parts if part.strip()
            ]
            return dates
        except ValueError:
            raise forms.ValidationError("Enter a valid date range in YYYY-MM-DD&YYYY-MM-DD format.")

    def validate(self, value):
        """ Optionally add more validation here """
        super().validate(value)
        if len(value) > 2:
            raise forms.ValidationError("Enter no more than two dates.")

    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE]
        }




class ODTextInput(ODInput,forms.TextInput):
    input_type = 'text'  # Default type is 'text'
    template_name = 'od/fields/TextInput.html'

class ODNumberInput(ODInput,forms.NumberInput):
    input_type = 'number'  # Number input type
    template_name = 'od/fields/NumberInput.html'

class ODEmailInput(ODInput,forms.EmailInput):
    input_type = 'email'  # Email input type
    template_name = 'od/fields/EmailInput.html'

class ODDateTimeInput(ODInput,forms.DateTimeInput):
    input_type = 'datetime-local'  # Use the 'datetime-local' input type for datetime fields
    template_name = 'od/fields/DateTimeInput.html'

class ODDateInput(ODInput,forms.DateInput):
    input_type = 'date'  # Use the 'date' input type for date fields
    template_name = 'od/fields/DateInput.html'
    
class ODTimeInput(ODInput,forms.TimeInput):
    input_type = 'time'  # Use the 'time' input type for time fields
    template_name = 'od/fields/TimeInput.html'

class ODCheckboxSwitchInput(ODInput,forms.NullBooleanSelect):
    input_type = 'checkbox'  # Use 'checkbox' input type for boolean values
    template_name = 'od/fields/CheckboxSwitchInput.html'
    
    class Media:
        css = {
            'all': ['od/css/components/inputs/checkbox/checkbox.min.css']
        }



class ODFileInput(ODInput,forms.FileInput):
    template_name  = 'od/fields/FileInput.html'

    class Media:
        css = {
            'all':[INPUTS_STYLE_FILE,'od/css/components/inputs/file/file.min.css']
        }

class ODURLField(ODInput,forms.URLInput):
    input_type = 'url'  # URL input type
    template_name = 'od/fields/URLInput.html'

class ODSlugInput(ODInput,forms.TextInput):
    input_type = 'text'  # SlugField uses a text input type
    template_name = 'od/fields/SlugInput.html'

    class Media:
        css = {
            "all": [INPUTS_STYLE_FILE]
        }

class ODTextArea(ODInput,forms.Textarea):
    input_type = 'textarea'  # Textarea type
    template_name = 'od/fields/TextArea.html'

    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE,'https://unpkg.com/trix@2.0.0/dist/trix.css','od/css/components/inputs/textarea/textarea.min.css']
        }
        js = ["https://unpkg.com/trix@2.0.0/dist/trix.umd.min.js"]

class ODCheckboxInput(ODInput,forms.CheckboxInput):
    input_type = 'checkbox'  # Checkbox input type
    template_name = 'od/fields/CheckboxSwitchInput.html'

    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE, 'od/css/components/inputs/checkbox/checkbox.min.css']
        }

class ODSelect(ODInput,forms.Select):
    input_type = 'select'  # Select dropdown input type
    template_name = 'od/fields/Select.html'

    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE, 'od/css/components/inputs/radio/radio_input.min.css']
        }

class ODSelectMultiple(ODInput,forms.SelectMultiple):
    input_type = 'select-multiple'  # Multiple select input type
    template_name = 'od/fields/SelectMultiple.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Ensure value is a list
        context['value'] = value or []
        context['choices'] = list(self.choices)
        return context

    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE]
        }
