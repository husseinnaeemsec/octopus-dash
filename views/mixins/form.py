from ...forms import get_model_create_form

class DynamicFormMixin:
    def get_form_class(self):
        return get_model_create_form(self.model_admin, self.model_admin.form_fields)