from django.forms import modelformset_factory
from ...forms import inline_modelform_factory
from django.shortcuts import render
from django.db.models import Case, When
from django.contrib import messages
class InlineFormsetMixin:
    def get_formset_queryset(self, queryset):
        ids = [obj.id for obj in queryset]
        preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(ids)])
        return self.model.objects.filter(id__in=ids).order_by(preserved_order)

    def get_formset(self, queryset, post=None, files=None):
        form = inline_modelform_factory(self.model_admin)
        FormSet = modelformset_factory(self.model, form=form, extra=0)
        return FormSet(queryset=queryset, data=post, files=files)

class HandleFormsetPostRequest(InlineFormsetMixin):
    
    def _handle_formset_submit(self):
        
        context = self.get_context_data()
        
        queryset = self.get_queryset()
        
        formset_queryset = self.get_formset_queryset(queryset)
        
        
        
        formset = self.get_formset(formset_queryset,self.request.POST,self.request.FILES)
        
        if formset.is_valid():
            formset.save()
            messages.success(self.request,f'Updated {queryset.count()} instances')
        
        else:
            messages.error(self.request,'Please check the forms befoer submitting the form')
        
        
        context['formset'] = formset
        return render(self.request,self.template_name,context)
    def _handle_custom_action_submit(self):
            return render(self.request,self.template_name,self.get_context_data())
        