
from django import forms

class FieldMetaData:
    
    def __init__(self,field:forms.Field):
        pass
        # print(field.widget)
        
class DynamiModelForm(forms.ModelForm):
    
    fields_metadata = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected super call
        
        # Optionally, you can loop through fields and print them or customize further
        for field_name,field in self.fields.items():
            field.widget.attrs['class'] = 'w-full p-2 px-5 bg-neutral-100 my-2 rounded-md '
            if not self.fields_metadata.get(field_name):
                self.fields_metadata[field_name] = {
                    'metadata':FieldMetaData(field),
                    'field':field,
                }

    
    class Meta:
        model = None
        fields = "__all__"

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
