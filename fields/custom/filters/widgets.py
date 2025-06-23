from ....fields.fields import INPUTS_STYLE_FILE
from django import forms

class ODTrueFalseNoneWidget(forms.RadioSelect):
    input_type = 'select'  # Select dropdown input type
    template_name = 'od/fields/custom/TrueFalseNoneRadioGroup.html'
    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE, 'od/css/components/inputs/radio/radio_input.min.css']
        }


class TextInputWidget(forms.TextInput):
    input_type = 'select'  # Select dropdown input type
    template_name = 'od/fields/custom/TextInput.html'
    class Media:
        css = {
            'all': [INPUTS_STYLE_FILE]
        }


class DateTimeRangeWidget(forms.MultiWidget):
    
    template_name = 'od/fields/custom/DateTimeRange.html'
    
    def __init__(self,model_field, attrs=None):
        self.model_field = model_field
        widgets = [
            forms.DateTimeInput(),
            forms.DateTimeInput(),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value and isinstance(value, (list, tuple)) and len(value) == 2:
            return [value[0], value[1]]
        
        elif value:
            return value
        
        return [None, None]


    def value_from_datadict(self, data, files, name):
        # This is crucial: Django looks here to extract subwidget values
        return [
            data.get(f"{name}_start"),
            data.get(f"{name}_end"),
        ]


    def format_output(self, rendered_widgets):
        # Optional: You can define how both inputs are rendered together
        return f'{rendered_widgets[0]} & {rendered_widgets[1]}'


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = name.replace("_"," ").title()
        subwidgets = context['widget']['subwidgets']
        if len(subwidgets) >= 2:
            subwidgets[0]['name'] = f'{name}_start'
            subwidgets[0]['label'] = f'Start'
            subwidgets[1]['name'] = f'{name}_end'
            subwidgets[1]['label'] = f'End'
        return context


class DateRangeWidget(forms.MultiWidget):
    
    template_name = 'od/fields/custom/DateRange.html'
    
    def __init__(self,model_field, attrs=None):
        self.model_field = model_field
        widgets = [
            forms.DateInput(),
            forms.DateInput(),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value and isinstance(value, (list, tuple)) and len(value) == 2:
            return [value[0], value[1]]
        
        elif value:
            return value
        
        return [None, None]


    def value_from_datadict(self, data, files, name):
        # This is crucial: Django looks here to extract subwidget values
        return [
            data.get(f"{name}_start"),
            data.get(f"{name}_end"),
        ]


    def format_output(self, rendered_widgets):
        # Optional: You can define how both inputs are rendered together
        return f'{rendered_widgets[0]} & {rendered_widgets[1]}'


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = name.replace("_"," ").title()
        subwidgets = context['widget']['subwidgets']
        if len(subwidgets) >= 2:
            subwidgets[0]['name'] = f'{name}_start'
            subwidgets[0]['label'] = f'Start'
            subwidgets[1]['name'] = f'{name}_end'
            subwidgets[1]['label'] = f'End'
        return context


class TimeRangeWidget(forms.MultiWidget):
    
    template_name = 'od/fields/custom/TimeRange.html'
    
    def __init__(self,model_field, attrs=None):
        self.model_field = model_field
        widgets = [
            forms.TimeInput(),
            forms.TimeInput(),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value and isinstance(value, (list, tuple)) and len(value) == 2:
            return [value[0], value[1]]
        
        elif value:
            return value
        
        return [None, None]


    def value_from_datadict(self, data, files, name):
        # This is crucial: Django looks here to extract subwidget values
        return [
            data.get(f"{name}_start"),
            data.get(f"{name}_end"),
        ]


    def format_output(self, rendered_widgets):
        # Optional: You can define how both inputs are rendered together
        return f'{rendered_widgets[0]} & {rendered_widgets[1]}'


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = name.replace("_"," ").title()
        subwidgets = context['widget']['subwidgets']
        if len(subwidgets) >= 2:
            subwidgets[0]['name'] = f'{name}_start'
            subwidgets[0]['label'] = f'Start'
            subwidgets[1]['name'] = f'{name}_end'
            subwidgets[1]['label'] = f'End'
        return context
