from django.views.generic import TemplateView
from .mixins.context import AppContextMixin

class AppView(AppContextMixin, TemplateView):
    template_name = 'od/app/app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = self.app
        return context

