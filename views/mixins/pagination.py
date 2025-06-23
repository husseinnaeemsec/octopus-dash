
class CustomPaginationMixin:
    def get_paginate_by(self, queryset):
        page_size = self.request.GET.get('page_size')
        if page_size and page_size.isdigit():
            size = int(page_size)
            return size if size <= 100 else self.paginate_by
        return self.paginate_by
