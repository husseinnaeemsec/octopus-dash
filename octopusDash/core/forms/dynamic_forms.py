from django.forms import ModelForm

class DynamicForm(ModelForm):
    
    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        
        for field in self.Meta.readonly_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True
                self.fields[field].widget.attrs['required'] = False
        
        # Fields Tailwind CSS Classes 
        self.handle_field_styling()
        
    
    def handle_field_styling(self):
        for field_name, field in self.fields.items():
            
            
            
            extra_classes = []
            
            if field.widget.attrs.get('disabled'):
                extra_classes.append("disabled ")
                extra_classes.append("bg-gray-500 ")
            
            field.widget.attrs['class'] = f'w-full p-2 px-5 bg-neutral-800 my-2 rounded-md '
            
            if extra_classes:
                field.widget.attrs['class'] +=' '.join(extra_classes)
            
            
            if(field.widget.__class__.__name__.lower() == 'textarea'):
                field.widget.attrs['class'] +=' textarea-widget '
        
    class Meta:
        model = None
        fields = '__all__'
        readonly_fields = []


def generate_model_form(model,**kwargs):
    
    _meta = type("Meta",(),{
        'model': model,
        'fields': kwargs.get('fields', '__all__'),
        'exclude': kwargs.get('exclude', []),
        "readonly_fields": kwargs.get('readonly_fields',[])
    })
    
    return type(f"{model.__name__}DynamicModelForm",(DynamicForm,),{'Meta': _meta})