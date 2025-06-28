class FilterMixin:
    def apply_filters(self, queryset):
        if self.model_admin.get_filter_fields() and self.get_filters_form() is not None:
            query = self.get_filters_form().get_filter_query()
            if query:
                return queryset.filter(**query)
        return queryset

    def get_filters_form(self):
        
        return None
