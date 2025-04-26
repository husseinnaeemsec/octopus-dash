from django.db.models import Q
from .utils import get_model_admin
from django.shortcuts import render
from .exceptions import AppNotFound,ModelNotFound
from .forms import form_factory
from django.urls import reverse_lazy
from django.apps import apps
import json


class BaseContextMixin:
    
    def get_context_data(self):
        
        
        
        return super().get_context_data() or {}
    

class AppLookupMixin:
    
    model = None
    model_name = None
    app_name = None
    model_admin = None
    queryset = None
    
    
    def dispatch(self, request, *args, **kwargs):
        # Fetch app and model from kwargs
        app_name = kwargs.get("app", None)
        try:
            self.app_config = apps.get_app_config(app_name)
        except LookupError:
            app_name = kwargs.get("app",None)
            return render(request,'errors/app_not_found.html',{'app_name':app_name})
        return super().dispatch(request, *args, **kwargs)

class ModelLookupMixin(AppLookupMixin):
    
    def dispatch(self,request,*args,**kwargs):
        
        view = super().dispatch(request,*args,**kwargs)
        
        model_name = kwargs.get("model_name")
        
        try:
            self.model = self.app_config.get_model(model_name)
            self.queryset = self.model.objects.all().order_by('id')
            self.model_admin = get_model_admin(self.model._meta.app_config, self.model)
            self.app_name = self.model._meta.app_config.label
            self.model_name = self.model._meta.model_name
            self.form_class = form_factory(self.model)
            self.success_url = reverse_lazy(f"list-objects",args=[self.app_config.label,model_name])
        
        except LookupError:
            
            return render(request,'errors/model_not_found.html',{'model_name':model_name})

        
        return view

class ModelContexttMixin(ModelLookupMixin,BaseContextMixin):
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.model is not None:
            context['app_name'] = self.app_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
            context['model_name'] = self.model._meta.verbose_name
            context['model_admin'] = self.model_admin
            context['model'] = self.model
            context['objects_count'] = self.get_queryset().count()
            
        return context


class SearchMixin(BaseContextMixin):
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get search query 
        query = self.request.GET.get("query",None)
        self.search_query = query
        search_fields = self.model_admin.model_search_fields
        self.searched_fields = []
        
        if not query or not search_fields: return queryset
        
        q_object = Q()
        
        for field in search_fields:
            if field in self.model_admin.list_display:
                q_object |= Q(**{f'{field}__icontains':str(query).lower()})
                self.searched_fields.append(field)
        
        queryset = queryset.filter(q_object)
        
        return queryset
    
    def get_context_data(self):
        context = super().get_context_data()
        context['search_query'] = self.search_query
        context['searched_fields'] = self.searched_fields

        return context


class FiltersMixin(BaseContextMixin):
    
    active_filters = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filters = self.get__filters()
        
        if len(filters) >=1:
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
            value = self.request.GET.get(field_name, None)

            query = {}

            # Boolean field
            if filter_obj.get('is_bool'):
                if value:
                    query[field_name] = True if value == 'on' else False if value == 'off' else None
                    if query is not None:
                        filter_obj['value'] = value
                        filter_obj['type'] = 'boolean'
                        
                        if not active_filters.get(field_name):
                            active_filters[field_name] = filter_obj
                            
                        else:
                            active_filters[field_name]['value'] = value

            # Date/Time-based fields (date, time, datetime)
            elif filter_obj.get('is_date') or filter_obj.get('is_time') or filter_obj.get('is_datetime'):
                from_value = self.request.GET.get(f'from_{field_name}',None)
                filter_type = 'date' if filter_obj.get("is_date") else 'time' if filter_obj.get("is_time") else 'datetime' if filter_obj.get("is_datetime") else 'unknown'
                to_value = self.request.GET.get(f'to_{field_name}',None)
                from_filter = {
                        'name':f"From {filter_obj.get('name')}",
                        'field':f'from_{filter_obj.get('field')}',
                        'value':from_value,
                        'type':filter_type
                    }
                to_filter = {
                        'name':f"To {filter_obj.get('name')}",
                        'field':f'to_{filter_obj.get('field')}',
                        'value':to_value,
                        'type':filter_type
                    }
                if from_value and to_value:
                    query[f'{field_name}__range'] = [from_value, to_value]
                elif from_value:
                    query[f'{field_name}__gte'] = from_value
                elif to_value:
                    query[f'{field_name}__lte'] = to_value

                if to_value and not active_filters.get(to_filter['field']):
                    active_filters[to_filter['field']] = to_filter
                elif active_filters.get(to_filter['field']):
                    
                    if to_value:active_filters[to_filter['field']]['value'] = to_filter['value']
                    else: del active_filters[to_filter['field']]

                if from_value and not active_filters.get(from_filter['field']):
                    active_filters[from_filter['field']] = from_filter
                elif active_filters.get(from_filter['field']):
                    if from_value:active_filters[from_filter['field']]['value'] = from_filter['value']
                    else: del active_filters[from_filter['field']]

            # Regular text or other types of filters
            elif value:
                query[field_name] = value
                filter_obj['value'] = value

            if query is not None:
                filters.append(query)

        self.active_filters = active_filters
        
        return filters
    



class ListViewMixin(ModelContexttMixin,FiltersMixin,SearchMixin):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ids_json'] = json.dumps(list(self.get_queryset().values("id")))
        return context
    


class SearchFilterMixin(FiltersMixin,SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ids_json'] = json.dumps(list(self.get_queryset().values('id')))
        
        return context
    