# What I Learned

📹 [Ref→](https://www.youtube.com/watch?v=c708Nf0cHrs&list=WL&index=11)

## [2:59:45] Default DRF Settings

- Authentication & Permissions

  - How to define DRF default settings in _settings.py_

  ```python
  REST_FRAMEWORK = {
     "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "users.authentications.CustomTokenAuthentication",
     ],
     "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
     ],
  }
  ```

  - `permission_classes` can be overided in a view class

- Throttling
  - It is more desirable to use NGINX rate limiting(throttling) than DRF built-in throttling

📚 [Ref→](https://www.django-rest-framework.org/api-guide/settings/)

<br/>

## [03:25:51] URLs, Reverse, & Serializers

- 3 ways to return the URL
  - `return f"/api/products/{obj.pk}"`
  - `reverse(VIEW_NAME, kwargs={"pk": obj.pk}, request=request)`
  - `hyperlink = serializers.HyperlinkedIdentityField(view_name=VIEW_NAME, lookup_field="pk", read_only=True)`

<br/>

## [04:24:30] Pagination

📚 [Ref→](https://www.django-rest-framework.org/api-guide/pagination/)

- How to use DRF pagination in APIView

  ```python
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
  ```

<br/>

## [04:32:36] A Django Based Search for Product API

```python
# Django Default Search Engine
# Search results only depends on the target model (more like filtering)
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = models.Q(title__icontains=query) | models.Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user:
            qs_ = self.filter(user=user).filter(lookup)
            qs = (qs | qs_).distinct()
        return qs


class ProductMangaer(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(
            query,
            user=user,
        )
```

<br/>

## [04:48:34] Building your Search Engine on Algolia

- Ref _products.client_, _products.index_

<br/>

## [05:30:22] Unified Design of Serializers & Indices

- How to rename a certain field
  1.  Define `@property` in a model
      - There is a problem that it is necessary to keep the original field in the serializer for PUT or PATCH.
  2.  Add a field in a serializer and give it a property `source`.
  3.  (Optional) For Algolia searching, it is necessary to define a method field by using `@property`.

---

# 💡 Questions

1. When clicking URL or hyperlink, what happens?

   1. DNS resolution

      - Browser translate human-readable URL into an IP address.
      - Computer communicate with other computers with an IP address not a domain-name.

   2. Opening connection to the web server that hosts the website
      - It is done using HTTP or HTTPS.
   3. Sending request
      - The request includes various information such as the type of request, headers, pages or resource requested etc.
   4. Processing requestwhat happend when we clicked the url or hyperlink.
      - The web server generates an HTTP response containg the requested data like HTML file.
   5. Receiving response
      - The browser receives the HTTP response from the web server.
   6. Rendering the page
      - The browser interprets the received data (often static files like html, css, js).
      - It renders the web pages based on this data.

2. What is the difference between simply clicking a link and calling an HTTP method with a request?

   - Cliking a link
     - A User initiates the action and the browser handles the entire process of navigating to the new URL.
   - Calling an HTTP method
     - It is a code-based programmatic action that allows user to interact with the web server, often as a part of building web application.

3. What is REST API and RESTful API?

   - 📚[ref→](https://engulfedinflames.github.io/categories/python/django/5)

4. Explain how to get credential with postman in the session-based authentication application.

   - Session authentication can be acheived by manuallymanaging cookies or tokens.
   - (So,) It is necessary to send an initial request to get cookies or tokens
   - (And then,) The subsequent requests are allowed to be sent to web server with session identifier (cookies or tokens)

5. `ATOMIC_REQUESTS`

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}
```

- By using `@method_decorator(transaction.non_atomic_requests)`, `atomic_requests` can be invalidated.
  - This decorator is only allowed in the DISPATCH method.
  - The `dispatch` method is the one that runs to process the request before other HTTP methods.
- `with transaction.atomic()`
