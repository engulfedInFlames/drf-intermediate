from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size_query_param = "page"


class ProductPaginationMixin:
    pagination_class = ProductPagination

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset=queryset,
            request=self.request,
            view=self,
        )

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
