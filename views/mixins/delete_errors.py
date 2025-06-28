from django.db.models import ProtectedError
from django.db import IntegrityError
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import messages


class DeleteErrorHandlingMixin:
    error_template = 'od/errors/object_not_found.html'

    def post(self, request, *args, **kwargs):
        error_message = None
        try:
            obj = self.get_object()
            messages.success(self.request,f"{self.model_admin.model_name} :{obj} was deleted.  ")
            obj.delete()
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            error_message = "Object is protected and cannot be deleted."
            return self.render_error(error_message, 'od/errors/object_protected.html')
        except IntegrityError:
            error_message = "Integrity error occurred on delete."
            return self.render_error(error_message, 'od/errors/integrity_error_on_delete.html')
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            return self.render_error(error_message, 'od/errors/unknown_error.html')


    def render_error(self, error_message, template):
        messages.error(self.request,error_message)
        return render(self.request, template, {'error_message': error_message, 'obj': getattr(self, 'object', None)})
