from .views_mixin import ODAppModelViewMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import ProtectedError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .mixins.form import DynamicFormMixin
from .mixins.delete_errors import DeleteErrorHandlingMixin


class CreateInstanceView(DynamicFormMixin, ODAppModelViewMixin, CreateView):
    template_name = 'od/app/model/create.html'

    def get_success_url(self):
        if self.request.POST.get("__success__") == 'save-add':
            return reverse_lazy('od-create-instance', args=[self.app.app_label, self.model_name])
        return reverse_lazy('od-model-view', args=[self.app.app_label, self.model_name])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.model.__name__} created successfully!")
        return response


class UpdateInstanceView(DynamicFormMixin, ODAppModelViewMixin, UpdateView):
    template_name = 'od/app/model/update.html'

    def get_success_url(self):
        return reverse_lazy('od-update-instance', args=[self.app.app_label, self.model_name, self.object.pk])

    def form_valid(self, form):
        instance = form.save()

        for field_name in getattr(form, '_files_to_remove', []):
            file_field = getattr(instance, field_name, None)
            if file_field:
                file_field.delete(save=False)
                setattr(instance, field_name, None)

        messages.success(self.request, f"Successfully updated {self.model._meta.verbose_name}: {instance}")
        return super().form_valid(form)


class DeleteInstanceView(DeleteErrorHandlingMixin, ODAppModelViewMixin, DeleteView):
    template_name = 'od/app/model/delete.html'
    context_object_name = 'object'

    def get_success_url(self):
        return reverse_lazy('od-model-view', args=[self.app.app_label, self.model_name])
