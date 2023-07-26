from django.urls import path


from . import views

urlpatterns = [
    path(
        "",
        views.ProductAPIView.as_view(),
        name="product-list",
    ),
    path(
        "<int:pk>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path(
        "search/",
        views.SearchProductAPIView.as_view(),
        name="search-product",
    ),
    path(
        "algolia-search/",
        views.AlgoliaSearchProductAPIView.as_view(),
        name="algolia-search-product",
    ),
]
