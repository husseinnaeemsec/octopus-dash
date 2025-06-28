from django.views.generic import TemplateView
from .mixins.context import AppContextMixin


class AppView(AppContextMixin,TemplateView):
    
    template_name = 'od/app/app.html'


