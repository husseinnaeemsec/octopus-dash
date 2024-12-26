from django import forms

# Assuming DynamicForm is a base form class that you want to inherit from
class DynamicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full p-2 rounded bg-gray-100 my-2'
        
def generate_form(model, **kwargs):
    # Dynamically create Meta class for the form
    meta_class = type("Meta", (), {
        "model": model,
        "fields": kwargs.get("fields", "__all__")
    })
    
    # Dynamically create the form class
    attrs = {
        "Meta": meta_class
    }
    
    # Generate the dynamic form class
    form_class_name = f"{model._meta.model_name.capitalize()}DynamicForm"
    return type(form_class_name, (DynamicForm,), attrs)
