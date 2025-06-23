from django import forms 
from ..fields.fields import ODDateFilterField,ODTextInput
from ..fields.custom.filters.fields import RadioGroupField,DateOnlyRangeField,TimeRangeField,DateTimeRangeField
from django.db import models
from datetime import datetime, date, time
from .model_forms import get_model_create_form,inline_modelform_factory,InlineEditModelForm


class DynamicFilterForm(forms.Form):
    
    def __init__(self, model_admin, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_admin = model_admin

        if not self.model_admin.model or not self.model_admin.get_filter_fields():
            return

        self.filter_fields = self.model_admin.get_filter_fields()

        for field in self.model_admin.model._meta.get_fields():
            if field.name in self.filter_fields:
                if isinstance(field, models.BooleanField):
                    self.fields[field.name] = RadioGroupField(model_field=field,required=False)

                elif isinstance(field, models.DateTimeField):
                    self.fields[field.name] = DateTimeRangeField(model_field=field,required=False)
                
                elif isinstance(field,models.DateField):
                    self.fields[field.name] = DateOnlyRangeField(model_field=field,required=False)
                
                elif isinstance(field,models.TimeField):
                    self.fields[field.name] = TimeRangeField(model_field=field,required=False)


    def get_filter_summary(self):
        """
        Return a list of dicts with detailed info about each filter field:
        - name
        - value (from cleaned_data if available)
        - field type
        - label
        - widget info
        """
        summary = []
        
        value = None
        

        for name, field in self.fields.items():
            
            if self.is_valid():
                value = self.cleaned_data.get(name) if hasattr(self,'cleaned_data') else self.data.get(name)
                field_data = {
                "name": name,
                "label": field.label,
                "value":value,
                "model_field":getattr(field,'model_field',None),
                'field':field,
                "is_bool":isinstance(getattr(field,'model_field',None),models.BooleanField),
                "is_datetime":isinstance(getattr(field,'model_field',None),models.DateTimeField),
                "is_date":isinstance(getattr(field,'model_field',None),models.DateField),
                "is_time":isinstance(getattr(field,'model_field',None),models.TimeField),
            }
            
            
                summary.append(field_data)
            
        return summary

    def get_filter_query(self):
        query = {}
        
        
        for filter in self.get_filter_summary():
            is_bool = filter['is_bool']
            is_datetime = filter['is_datetime']
            is_date = filter['is_date']
            is_time = filter['is_time']
            value = filter['value']
            name = filter['name']
            field = filter['field']
            
            
            if is_bool:           
                if name not in query and value is not None:
                    query[name] = value

            elif is_datetime or is_date or is_time:
                if isinstance(value,(list,tuple)) and len(value) == 2:
                    
                    
                    if value[0] and value[1]:
                        query[f'{name}__range'] = value

                    elif value[0]:
                        
                        query[f'{name}__gte'] = value[0]
                    
                    elif value[1]:
                        query[f'{name}__lte'] = value[1]
                    
                else:
                    continue
        
        return query