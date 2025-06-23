from django import forms 
from datetime import datetime
from  . import widgets
from datetime import datetime, time, date
from django.core.exceptions import ValidationError


class RadioGroupField(forms.Field):
    
    def __init__(self,model_field,*args,**kwargs):
        kwargs.setdefault("widget",widgets.ODTrueFalseNoneWidget(attrs={'label':model_field.verbose_name}))
        super().__init__(*args,**kwargs)
        
        self.model_field = model_field
        

    def to_python(self, value):
        
        if value == 'on':
            return True
        
        elif value == 'off':
            return False
        
        return None

class DateTimeRangeField(forms.MultiValueField):
    def __init__(self , model_field , *args, **kwargs):
        fields = [
            forms.DateTimeField(required=False),
            forms.DateTimeField(required=False),
        ]
        self.model_field = model_field
        widget = widgets.DateTimeRangeWidget(model_field=self.model_field,attrs={'class':'od w-full','required':False,'placeholder':f' Start {self.model_field.name} '})

        super().__init__(fields=fields, widget=widget, require_all_fields=False, *args, **kwargs)

            
    def compress(self, data_list):
        """
        Converts the list of values [start, end] into a tuple or single value.
        """
        return data_list or (None,None)

    def value_from_datadict(self, data, files, name):
        # manually extract values
        start = data.get(f"{name}_start")
        end = data.get(f"{name}_end")
        return [start, end]

    def clean(self, value):
        # First, run the parent clean to convert inputs to Python objects
        cleaned_data = super().clean(value)

        start, end = cleaned_data

        # Validate that start is not after end
        if start and end and start > end:
            raise ValidationError("Start date/time must be before end date/time.")

        if start and end and end < start:
            ValidationError("End date/time must be after start date/time.")

        return cleaned_data


class DateOnlyRangeField(forms.MultiValueField):
    """
    Accepts 'YYYY-MM-DD,YYYY-MM-DD'
    Returns (start_date, end_date)
    """
    def __init__(self , model_field , *args, **kwargs):
        fields = [
            forms.DateField(required=False),
            forms.DateField(required=False),
        ]
        self.model_field = model_field
        widget = widgets.DateRangeWidget(model_field=self.model_field,attrs={'class':'od w-full','required':False,'placeholder':f' Start {self.model_field.name} '})

        super().__init__(fields=fields, widget=widget, require_all_fields=False, *args, **kwargs)

            
    def compress(self, data_list):
        """
        Converts the list of values [start, end] into a tuple or single value.
        """
        return data_list or (None,None)

    def value_from_datadict(self, data, files, name):
        # manually extract values
        start = data.get(f"{name}_start")
        end = data.get(f"{name}_end")
        return [start, end]

    def clean(self, value):
        # First, run the parent clean to convert inputs to Python objects
        cleaned_data = super().clean(value)

        start, end = cleaned_data

        # Validate that start is not after end
        if start and end and start > end:
            raise ValidationError("Start date/time must be before end date/time.")

        if start and end and end < start:
            ValidationError("End date/time must be after start date/time.")

        return cleaned_data


class TimeRangeField(forms.MultiValueField):
    """
    Accepts 'HH:MM,HH:MM'
    Returns (start_time, end_time)
    """
    def __init__(self , model_field , *args, **kwargs):
        fields = [
            forms.TimeField(required=False),
            forms.TimeField(required=False),
        ]
        self.model_field = model_field
        widget = widgets.TimeRangeWidget(model_field=self.model_field,attrs={'class':'od w-full','required':False,'placeholder':f' Start {self.model_field.name} '})

        super().__init__(fields=fields, widget=widget, require_all_fields=False, *args, **kwargs)

            
    def compress(self, data_list):
        """
        Converts the list of values [start, end] into a tuple or single value.
        """
        return data_list or (None,None)

    def value_from_datadict(self, data, files, name):
        # manually extract values
        start = data.get(f"{name}_start")
        end = data.get(f"{name}_end")
        return [start, end]

    def clean(self, value):
        # First, run the parent clean to convert inputs to Python objects
        cleaned_data = super().clean(value)

        start, end = cleaned_data

        # Validate that start is not after end
        if start and end and start > end:
            raise ValidationError("Start time must be before end time.")
        
        return cleaned_data