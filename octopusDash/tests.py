from django.test import TestCase
from .core.registry.model.dynamic_forms import create_model_form
from .models import Post

class CustomModelFormTest(TestCase):
    def test_m2m_field_widget(self):
        form = create_model_form(Post)()
        self.assertIn('m2m_simple_model_options', form.fields)
        self.assertIn('m2m_simple_model_selected', form.fields)