from ...forms import model_form_factory

class DynamicFormMixin:
    def get_form_class(self):
        return model_form_factory(self.model_admin, self.model_admin.form_fields)