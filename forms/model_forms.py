from django import forms
from django.utils.safestring import mark_safe
from ..utils import get_field_access_info
from django.utils.html import escape
from django.utils.timezone import localtime
from datetime import datetime, date, time


class DynamicModelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model_admin = self.ODMeta.model_admin
        readonly_fields, hidden_fields = get_field_access_info(model_admin)

        for field_name in list(self.fields.keys()):
            if field_name in hidden_fields:
                del self.fields[field_name]
                continue

            field = self.fields[field_name]

            if field_name in readonly_fields:
                field.disabled = True
                field.widget.attrs['readonly'] = True
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' opacity-60 pointer-events-none'

            # Assign custom widgets
            custom_widget = self.get_custom_widget(field)
            if custom_widget:
                field.widget = custom_widget
    def get_custom_widget(self, field):
        from ..fields import fields  # avoid top-level circular import

        widget = None

        if isinstance(field.widget, forms.TextInput) and field.__class__.__name__ == 'SlugField':
            widget = fields.ODSlugInput(field=field)
        elif isinstance(field.widget, forms.TimeInput):
            widget = fields.ODTimeInput(field=field)
        elif isinstance(field.widget, forms.DateInput):
            widget = fields.ODDateInput(field=field)
        elif isinstance(field.widget, forms.DateTimeInput):
            widget = fields.ODDateTimeInput(field=field)
        elif isinstance(field.widget, forms.FileInput):
            widget = fields.ODFileInput(field=field)
        elif isinstance(field.widget, forms.TextInput):
            widget = fields.ODTextInput(field=field)
        elif isinstance(field.widget, forms.NumberInput):
            widget = fields.ODNumberInput(field=field)
        elif isinstance(field.widget, forms.NullBooleanSelect):
            widget = fields.ODCheckboxSwitchInput(field=field)
        elif isinstance(field.widget, forms.EmailInput):
            widget = fields.ODEmailInput(field=field)
        elif isinstance(field.widget, forms.Textarea):
            widget = fields.ODTextArea(field=field)
        elif isinstance(field.widget, forms.SelectMultiple):
            widget = fields.ODSelectMultiple(choices=getattr(field, 'choices', []), field=field)
        elif isinstance(field.widget, forms.Select):
            widget = fields.ODSelect(choices=getattr(field, 'choices', []), field=field)
        elif isinstance(field.widget, forms.CheckboxInput):
            widget = fields.ODCheckboxInput(field=field)
        elif isinstance(field.widget, forms.URLInput):
            widget = fields.ODURLField(field=field)

        return widget

    class Meta:
        model = None
        fields = '__all__'

    class ODMeta:
        model_admin = None

class InlineEditModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            model_admin = self.Meta.model_admin
            readonly_fields, hidden_fields = get_field_access_info(model_admin)
            self.headers = model_admin.list_display

            base_class = 'w-full min-h-full px-2 p-1 focus:outline'

            for field_name in list(self.fields.keys()):
                if field_name in hidden_fields:
                    del self.fields[field_name]
                    continue

                field = self.fields[field_name]
                field_classes = base_class

                if isinstance(field.widget, forms.CheckboxInput):
                    field_classes += ' od-switch'
                    field_classes = field_classes.replace("min-h-full px-2 p-1", "")
                elif isinstance(field.widget, forms.FileInput):
                    field_classes += ' py-2 hover:bg-slate-200 dark:hover:bg-slate-800'

                if field_name in readonly_fields:
                    field.disabled = True
                    field.widget.attrs['readonly'] = True
                    field_classes += ' opacity-60 pointer-events-none'

                field.widget.attrs['class'] = field_classes
    def _centred_div(self, content):
        return f"<div class='flex items-center h-full justify-center w-full'>{content}</div>"

    def render_as_table_row(self):
        base_td_class = 'h-10 max-w-96 w-fit text-xs text-slate-400 overflow-x-auto  border-x border-slate-200 dark:border-slate-700'
        output = ''
        instance_id = getattr(self.instance, 'id', None)
        if instance_id:
            output += f'<input type="hidden" name="{self.prefix}-id" value="{instance_id}">'

        for field_name in self.Meta.model_admin.list_display:
            if field_name not in ['id', 'pk']:
                if field_name in self.fields:
                    field = self[field_name]
                    field_errors = self.errors.get(field_name)
                    # Start with base class
                    td_class = base_td_class
                    tippy_attrs = ''
                    if field_errors:
                        # Add red outline
                        td_class += ' outline outline-1 outline-rose-500 rounded'
                        # Tooltip content
                        error_html = "<ul class='w-96 rounded p-3 space-y-3'>" + \
                                    "".join(f'<li class="font-semibold p-1 rounded text-rose-50">{escape(e)}</li>' for e in field_errors) + \
                                    "</ul>"
                        tippy_attrs = f'data-tippy-error data-tippy-content="{escape(error_html)}"'

                    output += f'<td class="{td_class}" {tippy_attrs}>{self._centred_div(field)}</td>'
                else:
                    # Non-editable column
                    value = getattr(self.instance, field_name, '')
                    if isinstance(value, (datetime, date, time)):
                        value = localtime(value) if isinstance(value, datetime) else value
                        value = value.strftime("%Y-%m-%d %H:%M") if isinstance(value, datetime) \
                                else value.strftime("%H:%M") if isinstance(value, time) \
                                else value.strftime("%Y-%m-%d")
                    output += f'<td class="{base_td_class} px-3">{value}</td>'

        return {
            'html': mark_safe(output),
            'id': instance_id
        }

    class Meta:
        model = None
        fields = '__all__'
        model_admin = None


def inline_modelform_factory(model_admin):
    # Dynamically create a Meta class
    cls_model = model_admin.model
    cls_list_editable = model_admin.list_editable
    cls_model_admin = model_admin
    class Meta:
        model = cls_model
        fields = cls_list_editable
        model_admin = cls_model_admin
    
    # Dynamically create a form class with the dynamic Meta class
    form_class = type(f"DynamicInlineEditModelForm", (InlineEditModelForm,), {"Meta": Meta})
    
    return form_class



def model_form_factory(model_admin,fields='__all__'):
    # Dynamically create a Meta class
    cls_model = model_admin.model
    cls_fields = fields
    cls_model_admin = model_admin
    class Meta:
        model = cls_model
        fields = cls_fields
    
    class ODMeta:
        model_admin = cls_model_admin
    
    # Dynamically create a form class with the dynamic Meta class
    form_class = type(f"DynamicModelCreateForm", (DynamicModelCreateForm,), {"Meta": Meta,'ODMeta':ODMeta})
    
    return form_class
