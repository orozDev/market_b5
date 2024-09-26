from api.auth.permissions import IsSuperUser
from api.filters import ProductFilter
from api.mixins import SerializerByMethodMixin, UltraGenericAPIView
from api.paginations import SimplePagintion
from api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import (
    DetailProductSerializer,
    ListProductSerializer,
    ProductSerializer,
    BulkCreateProductAttributeSerializer,
    ProductAttributeSerializer,
    UpdateAttributeForProductSerializer, CategorySerializer,
)
from store.models import Product, ProductAttribute, Category
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.mixins import (ListModelMixin, DestroyModelMixin, UpdateModelMixin)
from rest_framework.viewsets import ModelViewSet


class ListCreateProductApiView(UltraGenericAPIView):

    queryset = Product.objects.all()
    serializer_classes = {
        "get": ListProductSerializer,
        "post": ProductSerializer,
    }
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["name", "description", "content"]
    ordering = ["name", "price", "rating", "created_at"]
    # filterset_fields = ('category', 'tags', 'user', 'is_published',)
    filterset_class = ProductFilter
    pagination_class = SimplePagintion
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        products = self.filter_queryset(self.get_queryset())
        products = self.paginate_queryset(products)
        serializer = self.get_serializer(products, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(user=request.user)
        read_serializer = self.get_read_serializer(product)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class DetailUpdateDeleteProductApiView(
    ListModelMixin, DestroyModelMixin, UltraGenericAPIView
):
    queryset = Product.objects.all()
    serializer_classes = {
        "get": DetailProductSerializer,
        "patch": ProductSerializer,
    }
    permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly | IsSuperUser]
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # product = self.get_object()
        # serializer = self.get_serializer(instance=product)
        # return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(
            instance=product, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = self.get_read_serializer(
            instance=product, context={"request": request}
        )
        return Response(read_serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        # product = self.get_object()
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


class CreateProductApiView(GenericAPIView):
    queryset = ProductAttribute.objects
    serializer_class = BulkCreateProductAttributeSerializer
    permission_classes = [IsAuthenticated | IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attributes = serializer.validated_data.get("attributes")

        for attribute in attributes:
            self.get_queryset().create(**attribute)

        return Response(serializer.data, status.HTTP_201_CREATED)


class UpdateDeleteProduct(DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = ProductAttribute.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly | IsSuperUser]
    serializer_class = UpdateAttributeForProductSerializer

    def patch(self, request, id, *args, **kwargs):
        attribute = get_object_or_404(self.get_queryset(), id=id)
        serializer = self.get_serializer(
            data=request.data, instance=attribute, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, id, *args, **kwargs):
        attribute = get_object_or_404(self.get_queryset(), id=id)
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering = ["name", "created_at"]
    pagination_class = SimplePagintion
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)

