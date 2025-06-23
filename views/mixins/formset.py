from django.forms import modelformset_factory
from ...forms import inline_modelform_factory
from django.db.models import Case, When

class InlineFormsetMixin:
    def get_formset_queryset(self, queryset):
        ids = [obj.id for obj in queryset]
        preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(ids)])
        return self.model.objects.filter(id__in=ids).order_by(preserved_order)

    def get_formset(self, queryset, post=None, files=None):
        form = inline_modelform_factory(self.model_admin)
        FormSet = modelformset_factory(self.model, form=form, extra=0)
        return FormSet(queryset=queryset, data=post, files=files)
