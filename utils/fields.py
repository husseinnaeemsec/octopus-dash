from django.db import models

def get_field_input_type(field):
    


        ''' A function that will be used to detirmen input type '''
    
        if isinstance(field, models.CharField) and field.__class__.__name__ == 'SlugField':
            return 'slug'

        elif isinstance(field,models.CharField) and field.__class__.__name__ == 'URLField':
            return 'url'
        # Handle TimeInput
        elif isinstance(field, models.TimeField) and field.__class__.__name__ == 'TimeField':
            return 'time'

        # Handle DateInput
        elif isinstance(field, models.DateField) and field.__class__.__name__ == 'DateField':
            return 'date'

        # Handle DateTimeInput
        elif isinstance(field, models.DateTimeField) and field.__class__.__name__ == 'DateTimeField':
            return 'datetime'

        # Handle FileInput
        elif isinstance(field, (models.FileField,models.ImageField)):
            return 'file'

        # Handle other TextInput fields (default)
        elif isinstance(field, models.CharField):
            return 'text'

        # Handle NumberInput
        elif isinstance(field, models.PositiveIntegerField):
            return 'number'

        # Handle NullBooleanSelect (CheckboxSwitchInput)
        elif isinstance(field, models.BooleanField):
            return 'bool'

        # Handle EmailInput
        elif isinstance(field, models.EmailField):
            return 'email'

        # Handle Textarea
        elif isinstance(field, models.TextField):
            return 'textarea'

        # Handle URLInput
        elif isinstance(field, models.URLField):
            return 'url'

def get_field_access_info(model_admin):
    """
    Returns three sets:
    - readonly_fields: fields that should be shown but disabled
    - hidden_fields: fields that should be excluded from the form
    - exclude_fields: auto_now*, editable=False fields
    """
    model = model_admin.model
    readonly_fields = set(getattr(model_admin, "readonly_fields", []))
    hidden_fields = set(getattr(model_admin, "hidden_fields", []))

    for field in model._meta.fields:
        if isinstance(field, (models.DateField, models.DateTimeField)) and (field.auto_now or field.auto_now_add):
            readonly_fields.add(field.name)
        elif not field.editable:
            readonly_fields.add(field.name)

    return readonly_fields, hidden_fields