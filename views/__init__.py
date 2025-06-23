from django.views.generic import TemplateView

class DashboardView(TemplateView):
    
    template_name = 'od/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filters = {
            'name':"Hussein",
            'id':'12',
            'profile':'user_profile'
        }
        
        context['filters'] = filters
        
        return context

