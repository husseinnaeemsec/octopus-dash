from django.views.generic import TemplateView,ListView
from ..contrib.admin import registry
from ..exceptions import AppNotFound,ModelNotFound
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from ..forms import inline_modelform_factory
from django.forms import modelformset_factory
from django.db.models import Case, When



from ..forms import DynamicFilterForm

class ODAppTemplateView(TemplateView):
    template_name = 'od/app/app.html'

    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(self.kwargs.get('app'))
        if not self.app:
            raise AppNotFound(f'App with label "{self.kwargs.get("app")}" not found')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app'] = self.app
        return context


class ODAppModelViewMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("od-login"))

    def dispatch(self, request, *args, **kwargs):
        self.app = registry.get_app(kwargs.get("app"))
        if not self.app:
            raise AppNotFound(f'App with label "{kwargs.get("app")}" not found')

        self.model_name = kwargs.get("model")
        self.model = self.app.get_model(self.model_name)
        self.model_admin = self.app.get_model_admin(self.model_name)

        if not self.model:
            raise ModelNotFound(f'Model with name "{self.model_name}" not found')

        self.filters_form = DynamicFilterForm(self.model_admin, request.GET)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self):
        
        context = super().get_context_data() or {} 
        
        context.update({
            'model_admin':self.model_admin,
            'app':self.app,
        })
        
        return context

    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('page_size')
        if page_size and page_size.isdigit():
            size = int(page_size)
            return size if size <= 100 else self.paginate_by
        return self.paginate_by

    def get_formset_queryset(self, queryset):
        ids = [obj.id for obj in queryset]
        preserved = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(ids)])
        return self.model.objects.filter(id__in=ids).order_by(preserved)

class ODAppModelListView(ODAppModelViewMixin, ListView):
    template_name = 'od/app/model.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model_admin.manager.all()
        queryset = self._apply_filters(queryset)
        if not queryset.query.order_by:
            queryset = queryset.order_by(self.model._meta.pk.name)
        
        query = self.request.GET.get("query",None)
        
        if query is not None and self.model_admin.search_fields:
            queryset = self.model_admin.manager.search(query,self.model_admin.search_fields,queryset)
        
        return queryset

    def _apply_filters(self, queryset):
        if self.model_admin.get_filter_fields():
            filter_query = self.filters_form.get_filter_query()
            if filter_query:
                queryset = queryset.filter(**filter_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context.get("page_obj",None)
        queryset_page = page_obj.object_list if page_obj is not None else []
        context.update({
            'app': self.app,
            'model': self.model,
            'model_admin': self.model_admin,
            'model_name': self.model_name,
            'ids': [obj.id for obj in queryset_page],
            'queryset': queryset_page,
            'query': self.request.GET.get("query"),
            'current_page_count': len(queryset_page),
        })

        # Inline formset
        
        context['formset'] = self.get_formset(queryset_page)
        

        return context

    def get_formset(self,queryset_page,data=None,files=None):
        form = inline_modelform_factory(self.model_admin)
        FormSet = modelformset_factory(self.model, extra=0, form=form)
        formset_queryset = self.get_formset_queryset(queryset_page)
        
        return FormSet(data,files,queryset=formset_queryset)
        

