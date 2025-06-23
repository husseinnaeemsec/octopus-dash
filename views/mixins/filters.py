class FilterMixin:
    def apply_filters(self, queryset):
        if self.model_admin.get_filter_fields():
            query = self.filters_form.get_filter_query()
            if query:
                return queryset.filter(**query)
        return queryset
