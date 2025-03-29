from ...models import AppConfig,ModelConfig
from django import forms

class AppConfigModelForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        
        super().__init__(*args,**kwargs)
        
        for field_name,field in self.fields.items():            
            extra_classes = []
            
            if field.widget.attrs.get('disabled'):
                extra_classes.append("disabled ")
                extra_classes.append("bg-gray-500 ")
            
            field.widget.attrs['class'] = f'w-full p-2 px-5 bg-neutral-100 dark:bg-neutral-800 my-2 rounded-md '
            
            if extra_classes:
                field.widget.attrs['class'] +=' '.join(extra_classes)
            
            
            if(field.widget.__class__.__name__.lower() == 'textarea'):
                field.widget.attrs['class'] +=' textarea-widget '
    
    class Meta:
        model = AppConfig
        fields = ['name', 'description']