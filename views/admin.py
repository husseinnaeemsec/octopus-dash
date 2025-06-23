from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
import json

from .mixins.context import AppModelContextMixin
from .mixins.permissions import StaffPermissionMixin
from .mixins.formset import InlineFormsetMixin
from .mixins.filters import FilterMixin
from .mixins.pagination import CustomPaginationMixin


class ModelView(
    StaffPermissionMixin,
    AppModelContextMixin,
    FilterMixin,
    InlineFormsetMixin,
    CustomPaginationMixin,
    ListView,
):
    template_name = 'od/app/model.html'
    context_object_name = 'objects'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model_admin.manager.all()
        queryset = self.apply_filters(queryset)
        if not queryset.query.order_by:
            queryset = queryset.order_by(self.model._meta.pk.name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_page = context['page_obj'].object_list

        context.update({
            'app': self.app,
            'model': self.model,
            'model_admin': self.model_admin,
            'model_name': self.model_name,
            'queryset': queryset_page,
            'filters_form': self.filters_form,
            'ids': [obj.id for obj in queryset_page],
            'formset': self.get_formset(self.get_formset_queryset(queryset_page)),
        })

        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("query") and not self.model_admin.search_fields:
            messages.info(
                request,
                f"Set `search_fields` for model '{self.model_name}' to enable search.",
            )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_type = request.POST.get("request_type")
        context = self.get_context_data()

        if request_type == "custom_action":
            return self.handle_custom_action(request, context)
        elif request_type == "inline_bulk_update":
            return self.handle_inline_bulk_update(request, context)

        messages.error(request, "Invalid request type.")
        return self.render_to_response(context)

    def handle_custom_action(self, request, context):
        data = request.POST
        action = data.get("action")
        ids = data.get("ids")
        select_all = data.get("select_all") == 'true'

        if not action or (not ids and not select_all):
            messages.error(request, "Please select instances and an action.")
            return self.render_to_response(self.get_context_data())

        if not hasattr(self.model_admin, action):
            messages.error(request, f"No such action '{action}' on this model.")
            return self.render_to_response(context)

        try:
            queryset = self.model_admin.get_queryset() if select_all else self.model.objects.filter(id__in=json.loads(ids))
            getattr(self.model_admin, action)(queryset)
            messages.success(request, f"Performed '{action}' on {queryset.count()} items.")
        except Exception as e:
            messages.error(request, f"Action failed: {str(e)}")

        return self.render_to_response(context)

    def handle_inline_bulk_update(self, request, context):
        queryset_page = context['page_obj'].object_list
        formset = self.get_formset(queryset_page, request.POST, request.FILES)

        if formset.is_valid():
            formset.save()
            messages.success(request, "Inline update successful.")
        else:
            messages.error(request, "Inline update failed. Please check errors.")

        context['formset'] = formset
        return self.render_to_response(context)

