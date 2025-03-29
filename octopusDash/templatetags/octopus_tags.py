from django import template
from django.urls import reverse_lazy

register = template.Library()

@register.filter(name='attr')
def attr(obj, field_name):
    return getattr(obj, field_name, None)




@register.simple_tag
def get_url(view_name, model_name, pk=None):
    return reverse_lazy(f"{view_name}-{model_name}", args=[pk] if pk else [])


@register.simple_tag
def get_field_metadata(field):
    """
    Custom tag to return the metadata of a form field.
    It returns a dictionary of metadata related to the field.
    """
    if not field or not hasattr(field, 'field'):
        return {}
    
    model_field = field.field  # Access the actual model field
    widget = field.field.widget  # Access the widget used to render the field
    
    # Extract widget HTML attributes
    widget_attrs = widget.attrs if hasattr(widget, 'attrs') else {}

    metadata = {
        'field_type': type(model_field).__name__,  # Type of the underlying model field
        'required': model_field.required,  # Whether the field is required
        'help_text': model_field.help_text,  # Help text for the field
        'label': model_field.label,  # Label of the field
        'widget_type': type(widget).__name__,  # Widget type used to render the field (e.g., TextInput, Select)
        'widget_attrs': widget_attrs,  # HTML attributes of the widget
        'widget':widget,
        'widget_dir':dir(widget),
    }
    # Optionally, you can add more metadata attributes as needed
    return metadata
