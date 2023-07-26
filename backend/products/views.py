from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from . import client
from .models import Product
from .mixins import ProductPaginationMixin


class ProductAPIView(
    APIView,
    ProductPaginationMixin,
):
    serializer_class = serializers.ProductSerializer

    def get(self, request):
        products = Product.objects.all().order_by("id")
        page = self.paginate_queryset(products)
        if page:
            data = self.serializer_class(
                page,
                many=True,
            ).data
            serializer = self.get_paginated_response(data)
        else:
            serializer = self.serializer_class(
                products,
                many=True,
            )
        data = serializer.data
        # if not user.is_authenticated:
        #     return Response(status=status.HTTP_204_NO_CONTENT)

        # if not user.is_staff:
        #     products = products.filter(user=user)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content", title)
            serializer.save(
                user=request.user,
                content=content,
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductDetailAPIView(APIView):
    serializer_class = serializers.ProductDetailSerializer

    def get_object(self, pk):
        return get_object_or_404(
            Product,
            pk=pk,
        )

    def get(self, request, pk=None):
        try:
            product = self.get_object(pk)
            data = self.serializer_class(
                product,
                context={
                    "request": request,
                },
            ).data
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            product = self.get_object(pk)
            serializer = self.serializer_class(
                product,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            product = self.get_object(pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SearchProductAPIView(APIView):
    def get(self, request):
        keyword = request.GET.get("keyword")
        search_result = Product.objects.none()
        if keyword:
            qs = Product.objects.all()
            user = None
            if self.request.user.is_authenticated:
                user = request.user
            search_result = qs.search(
                keyword,
                user=user,
            )
        data = serializers.ProductSerializer(
            search_result,
            many=True,
        ).data

        return Response(data, status=status.HTTP_200_OK)


class AlgoliaSearchProductAPIView(APIView):
    def get(self, request):
        # user = None
        if request.user.is_authenticated:
            user = request.user.username
        keyword = request.GET.get("keyword", None)
        # public = str(request.GET.get("public")) != "0"
        tag = request.GET.get("tag", None)
        search_result = Product.objects.none()

        if not keyword and not tag:
            return Response(
                {"error_message": "검색어를 입력하세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_result = client.perform_search(
            keyword,
            tags=tag,
            # user=user,
            # public=public,
        )

        return Response(search_result, status=status.HTTP_200_OK)
