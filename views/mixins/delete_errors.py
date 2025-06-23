from django.shortcuts import render
from django.db.models import ProtectedError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class DeleteErrorHandlingMixin:
    error_template = 'od/errors/object_not_found.html'

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except ObjectDoesNotExist:
            return self.render_error('Object not found', 'od/errors/object_not_found.html')

        try:
            self.object.delete()
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            return self.render_error("Object is protected and cannot be deleted.", 'od/errors/object_protected.html')
        except IntegrityError:
            return self.render_error("Integrity error occurred on delete.", 'od/errors/integrity_error_on_delete.html')
        except Exception as e:
            return self.render_error(f"Unexpected error: {str(e)}", 'od/errors/unknown_error.html')

    def render_error(self, message, template):
        return render(self.request, template, {'error_message': message, 'obj': getattr(self, 'object', None)})
