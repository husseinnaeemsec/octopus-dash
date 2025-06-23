from .views_mixin import ODAppTemplateView, ODAppModelListView
from django.views.generic import ListView
from ..contrib.admin import registry
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
from ..forms import inline_modelform_factory
import json


class AppView(ODAppTemplateView):
    pass


class ModelView(ODAppModelListView):
    context_object_name = 'objects'
    filters = None
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'filters': self.filters,
            'filters_form': self.filters_form,
        })
        return context

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("query")
        if search_query and not self.model_admin.search_fields:
            messages.info(
                request,
                f"Please set 'search_fields' for model '{self.model_name}' in the model admin to enable search."
            )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_type = request.POST.get("request_type")
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if request_type == "custom_action":
            return self.handle_custom_action(request, context)

        elif request_type == "inline_bulk_update":
            return self.handle_inline_bulk_update(request, context)

        # Default fallback
        messages.error(request, "Invalid request type.")
        return self.render_to_response(context)

    def handle_custom_action(self, request, context):
        data = request.POST
        action = data.get("action")
        ids = data.get("ids")
        select_all = data.get("select_all") == 'true'

        if not action or (not ids and not select_all):
            messages.error(request, "Please select both an action and instances to perform the action on.")
            return self.render_to_response(self.get_context_data())

        if not hasattr(self.model_admin, action):
            messages.error(request, f"Model '{self.model._meta.model_name}' has no action called '{action}'.")
            return self.render_to_response(context)

        try:
            if select_all:
                queryset = self.model_admin.get_queryset()
            else:
                ids = json.loads(ids)
                queryset = self.model.objects.filter(id__in=ids)

            getattr(self.model_admin, action)(queryset)
            messages.success(request, f"Successfully applied '{action}' to {queryset.count()} instance(s).")

        except Exception as e:
            messages.error(request, f"Error performing '{action}': {str(e)}")

        return self.render_to_response(context)

    def handle_inline_bulk_update(self, request, context):
        queryset_page = context['page_obj'].object_list
        formset = self.get_formset(queryset_page, request.POST, request.FILES)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Successfully updated instances on this page.")
        else:
            messages.error(request, "Failed to update some instances. Please check the input.")

        context['formset'] = formset
        return self.render_to_response(context)
