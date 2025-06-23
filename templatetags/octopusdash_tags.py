from django import template
from django.urls import reverse_lazy
from django.db.models import Model
import ast
import bleach
import re
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def get_attr(obj, field_name):
    return getattr(obj, field_name, None)



@register.filter
def image_field(obj, field_name):
    file = getattr(obj, field_name, None)

    return file.url if file else ''

@register.filter
def get(obj:dict,key,default=None):
    return obj.get(key,default)



@register.filter("contains")
def contains(text:str,value:str):
    return str(value).lower() in str(text).lower()

@register.simple_tag
def get_url(view_name, model_name, pk=None):
    return reverse_lazy(f"octopus:{view_name}-{model_name}", args=[pk] if pk else [])


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
    }
    # Optionally, you can add more metadata attributes as needed
    return metadata


@register.simple_tag
def startswith(path:str,text:str):
    
    return path.startswith(text)

@register.filter
def endswith(path:str,text:str):
    return path.endswith(text)

@register.filter
def is_filtred(field,active_filters:dict):
    if not active_filters:
        return False
    
    filtres_querystring = active_filters.keys()
    
    return field in filtres_querystring or f'from_{field}' in filtres_querystring or f'to_{field}' in filtres_querystring

@register.simple_tag
def cast_value(value,type):
    if type == 'str':
        return str(value)
    return str(value)

@register.filter
def highlight(value, search_term):
    if not search_term:
        return value

    pattern = re.escape(search_term)
    highlighted = re.sub(
        pattern,
        lambda m: f'<mark class="bg-amber-400/40 text-white">{m.group(0)}</mark>',
        str(value),
        flags=re.IGNORECASE
    )
    return mark_safe(highlighted)

@register.filter
def render_html(html):
    allowed_tags = ['b', 'i','svg', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'p', 'br']
    allowed_attributes = bleach.sanitizer.ALLOWED_ATTRIBUTES
    sanitized_value = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
    return mark_safe(sanitized_value)

@register.simple_tag
def startswith_list(path1:str,search_list:list):
    
    for item in search_list:
        if path1.startswith(item):
            return True
    
    return False

@register.simple_tag
def pass_args(func,*args,**kwargs):
    
    return func(*args,**kwargs)

@register.simple_tag
def replace(text:str,val,val2):
    
    return text.replace(val,val2)


@register.filter("replace_filter")
def replace_filter(text:str,args:str):
    args = args.split(",")
    return text.replace(text,args[0],args[1])


@register.simple_tag
def split(text:str,sep):
    
    return text.split(sep)



@register.simple_tag
def get_key_value(dictonary:dict,key):
    
    if dictonary is None:
        return None
    
    return dictonary.get(key,None)


@register.simple_tag
def replace_text(text:str,replace:str,replace_with:str = ' '):
    
    return text.replace(replace,replace_with)


@register.simple_tag
def join(text1:str,text2:str):
    
    return text1+text2


@register.simple_tag
def get_formset_input_name(field_name,index):
    
    """ Used in a form set to generate a formset form(field) name form-0-field_name """
    
    return f"form-{index}-{field_name}"

@register.simple_tag
def get_formset_form(formset,index:int):
    
    try:
        return formset.forms[index]
    
    except:
        return None

@register.simple_tag
def get_formset_form_field(form,field):
    
    try:
        return form[field]
    except:
        return None

@register.filter(name='format_time')
def human_readable_execution_time(value):
    """
    Convert a time in seconds (float) to a human-readable format
    that dynamically adjusts between seconds, minutes, hours.
    """
    if value < 1:
        # If the value is less than 1 second, return it in microseconds
        return f"{value * 1_000_000:.2f} microseconds"
    
    if value < 60:
        # If the value is less than 60 seconds, return it in seconds
        return f"{value:.2f} seconds"
    
    if value < 3600:
        # If the value is less than 3600 seconds (60 minutes), return it in minutes
        minutes = value // 60
        seconds = value % 60
        return f"{int(minutes)} minutes {seconds:.2f} seconds"
    
    # If the value is more than 3600 seconds (1 hour), return it in hours
    hours = value // 3600
    minutes = (value % 3600) // 60
    seconds = value % 60
    return f"{int(hours)} hours {int(minutes)} minutes {seconds:.2f} seconds"


@register.filter(name='format_profile_key')
def format_profile_key(value):
    try:
        # Ensure value is string before evaluating
        if isinstance(value, str):
            parsed = ast.literal_eval(value)
        else:
            parsed = value

        if (
            isinstance(parsed, tuple) and
            len(parsed) == 2 and
            isinstance(parsed[0], tuple) and len(parsed[0]) == 2
        ):
            app_name, model_name = parsed[0]
            category = parsed[1]
            return f"App: {app_name.replace('_', ' ').title()}, Model: {model_name.replace('_', ' ').title()}, Category: {category.replace('_', ' ').title()}"
    except Exception as e:
        pass
    
    val = str(value).replace("_"," ")

    # Fallback if not structured properly
    row_tuple_key = ast.literal_eval(val)
    
    return f" Key: {row_tuple_key[0]} , Category : {row_tuple_key[1]} "


@register.filter
def startswith(value, arg):
    """Check if the value starts with the given argument"""
    if isinstance(value, str):
        return value.startswith(arg)
    return False


@register.filter
def split_get_last(value,arg):
    """Check if the value starts with the given argument"""
    
    return value.split(arg)[-1]