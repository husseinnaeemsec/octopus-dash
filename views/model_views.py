from .mixins.context import ModelContextMixin
from .mixins.filters import FilterMixin
from .mixins.formset import HandleFormsetPostRequest
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from .mixins.delete_errors import DeleteErrorHandlingMixin
from django.views.generic import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger
from ..forms import DynamicFilterForm



class ModelView(ModelContextMixin,ListView,FilterMixin,HandleFormsetPostRequest):
    template_name = 'od/app/model.html'
    context_object_name = 'objects'
    paginate_by = 10

    
    def post(self,request,*args,**kwargs):
        
        request_type = self.request.POST.get("request_type",None)
        
        
        if request_type == 'inline_bulk_update':
            return self._handle_formset_submit()
        
        elif request_type == 'cutom_action':
            return self._handle_custom_action_submit()
        
        
        messages.error(self.request,'You should use POST method only for <strong> custom_actions </strong> and <strong> inline_bulk_update </strong> ')
        return render(self.request,self.template_name,self.get_context_data())
        

    def get_context_data(self,*args,**kwargs):
        object_list = self.get_queryset()
        context = super().get_context_data(*args,object_list=object_list,**kwargs)
        queryset = context.get("page_obj",None).object_list if context.get("page_obj",None) else []
        queryset = self.get_formset_queryset(queryset)
        context.update({
            'filters_form':self.get_filters_form(),
            "query":self.request.GET.get("query",''),
            'formset':self.get_formset(queryset)
        })

        return context

    def get_queryset(self):
        queryset = self.model_admin.model.objects.all()
        queryset = self._apply_filters(queryset)
        search_query = self.request.GET.get("query",None)
        
        if search_query:
            queryset = self.model_admin.manager.search(search_query,self.model_admin.search_fields,queryset)

        return queryset
    
    def _apply_filters(self,queryset):
        if self.model_admin.get_filter_fields():
            filter_query = self.get_filters_form().get_filter_query()
            if filter_query.keys():
                queryset = queryset.filter(**filter_query)
            
        
        return queryset

    def get_filters_form(self):
        return DynamicFilterForm(self.model_admin,self.request.GET)
    

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size, orphans=self.get_paginate_orphans(), allow_empty_first_page=self.get_allow_empty())
        page = self.request.GET.get(self.page_kwarg) or 1

        try:
            page_number = paginator.validate_number(page)
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, ValueError):
            page_number = 1
            page_obj = paginator.page(1)
        except EmptyPage:
            page_number = paginator.num_pages
            page_obj = paginator.page(page_number)

        return paginator, page_obj, page_obj.object_list, page_number

    


class CreateInstanceView(ModelContextMixin, CreateView):
    template_name = 'od/app/model/create.html'

    def get_success_url(self):
        if self.request.POST.get("__success__") == 'save-add':
            return reverse_lazy('od-create-instance', args=[self.app.app_label, self.model_admin.model_name])
        return reverse_lazy('od-model-view', args=[self.app.app_label, self.model_admin.model_name])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.model.__name__} created successfully!")
        return response


class UpdateInstanceView(ModelContextMixin, UpdateView):
    template_name = 'od/app/model/update.html'
    context_object_name = 'object'

    def get_success_url(self):
        return reverse_lazy('od-update-instance', args=[self.app.app_label, self.model_admin.model_name, self.object.pk])


    def form_valid(self, form):
        instance = form.save()

        for field_name in getattr(form, '_files_to_remove', []):
            file_field = getattr(instance, field_name, None)
            if file_field:
                file_field.delete(save=False)
                setattr(instance, field_name, None)

        messages.success(self.request, f"Successfully updated {self.model._meta.verbose_name}: {instance}")
        return super().form_valid(form)


class DeleteInstanceView(DeleteErrorHandlingMixin,ModelContextMixin,DeleteView):
    template_name = 'od/app/model/delete.html'
    context_object_name = 'object'

    

    def get_success_url(self):
        return reverse_lazy('od-model-view', args=[self.app.app_label, self.model_admin.model_name])
