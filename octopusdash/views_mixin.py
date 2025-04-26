from django.db.models import Q
from .utils import get_model_admin
from django.shortcuts import render
from .exceptions import AppNotFound, ModelNotFound
from .forms import form_factory
from django.urls import reverse_lazy
from django.apps import apps
import json


class BaseContextMixin:
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) or {}


class AppLookupMixin:
    model = None
    model_name = None
    app_name = None
    model_admin = None
    queryset = None

    def dispatch(self, request, *args, **kwargs):
        app_name = kwargs.get("app")
        try:
            self.app_config = apps.get_app_config(app_name)
        except LookupError:
            return render(request, 'errors/app_not_found.html', {'app_name': app_name})
        return super().dispatch(request, *args, **kwargs)


class ModelLookupMixin(AppLookupMixin):
    def dispatch(self, request, *args, **kwargs):
        app_name = kwargs.get('app')
        model_name = kwargs.get("model_name")

        try:
            self.app_config = apps.get_app_config(app_name)
            self.model = self.app_config.get_model(model_name)
            self.model_admin = get_model_admin(self.model._meta.app_config, self.model)
            self.app_name = self.model._meta.app_config.label
            self.model_name = self.model._meta.model_name
            self.form_class = form_factory(self.model)
            self.success_url = reverse_lazy("list-objects", args=[self.app_config.label, model_name])
        except LookupError:
            return render(request, 'errors/model_not_found.html', {'model_name': model_name})

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('id')


class ModelContextMixin(ModelLookupMixin, BaseContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = self.app_name
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['model_admin'] = self.model_admin
        context['model'] = self.model
        context['objects_count'] = self.get_queryset().count()
        return context


class SearchMixin(BaseContextMixin):
    searched_fields = []
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        self.searched_fields = []
        search_fields = self.model_admin.model_search_fields

        if not query or not search_fields:
            return queryset

        q_object = Q()
        for field in search_fields:
            if field in self.model_admin.list_display:
                q_object |= Q(**{f'{field}__icontains': str(query).lower()})
                self.searched_fields.append(field)

        return queryset.filter(q_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("query")
        context['searched_fields'] = self.searched_fields
        return context


class FiltersMixin(BaseContextMixin):
    active_filters = None

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = self.get__filters()

        if filters:
            f_object = Q()
            for model_filter in filters:
                f_object &= Q(**model_filter)
            queryset = queryset.filter(f_object)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filters'] = self.active_filters
        return context

    def get__filters(self):
        filters = []
        active_filters = {}

        for filter_obj in self.model_admin.model_filter_fields:
            field_name = filter_obj.get("field")
            value = self.request.GET.get(field_name)
            query = {}

            if filter_obj.get('is_bool'):
                if value:
                    query[field_name] = value == 'on'
                    filter_obj['value'] = value
                    filter_obj['type'] = 'boolean'
                    active_filters[field_name] = filter_obj

            elif filter_obj.get('is_date') or filter_obj.get('is_time') or filter_obj.get('is_datetime'):
                from_value = self.request.GET.get(f'from_{field_name}')
                to_value = self.request.GET.get(f'to_{field_name}')
                filter_type = 'date' if filter_obj.get('is_date') else 'time' if filter_obj.get('is_time') else 'datetime'

                if from_value and to_value:
                    query[f'{field_name}__range'] = [from_value, to_value]
                elif from_value:
                    query[f'{field_name}__gte'] = from_value
                elif to_value:
                    query[f'{field_name}__lte'] = to_value

                if to_value:
                    active_filters[f'to_{field_name}'] = {
                        'name': f"To {filter_obj.get('name')}",
                        'field': f'to_{field_name}',
                        'value': to_value,
                        'type': filter_type
                    }

                if from_value:
                    active_filters[f'from_{field_name}'] = {
                        'name': f"From {filter_obj.get('name')}",
                        'field': f'from_{field_name}',
                        'value': from_value,
                        'type': filter_type
                    }

            elif value:
                query[field_name] = value
                filter_obj['value'] = value

            if query:
                filters.append(query)

        self.active_filters = active_filters
        return filters


class ListViewMixin(ModelContextMixin, FiltersMixin, SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ids_json'] = json.dumps(list(self.get_queryset().values("id")))
        return context


class SearchFilterMixin(FiltersMixin, SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ids_json'] = json.dumps(list(self.get_queryset().values("id")))
        return context
