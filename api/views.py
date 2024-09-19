from pprint import pprint
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes as permission_classes_d, parser_classes, authentication_classes

from api.auth.permissions import IsSuperUser
from api.filters import ProductFilter
from api.mixins import SerializerByMethodMixin, UltraGenericAPIView
from api.paginations import SimplePagintion
from api.permissions import IsOwnerOrReadOnly
from api.serializers import DetailProductSerializer, ListProductSerializer, ProductSerializer, \
    BulkCreateProductAttributeSerializer, ProductAttributeSerializer, UpdateAttributeForProductSerializer
from store.models import Product, ProductAttribute
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, GenericAPIView, \
    ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView,\
    RetrieveUpdateDestroyAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend


class ListCreateProductApiView(UltraGenericAPIView):

    queryset = Product.objects.all()
    serializer_classes = {
        'get': ListProductSerializer,
        'post': ProductSerializer,
    }
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ['name', 'description', 'content']
    ordering = ['name', 'price', 'rating', 'created_at']
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


class DetailUpdateDeleteProductApiView(UltraGenericAPIView):
    queryset = Product.objects.all()
    serializer_classes = {
        'get': DetailProductSerializer,
        'patch': ProductSerializer,
    }
    permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly | IsSuperUser]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(instance=product)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = self.get_read_serializer(instance=product, context={'request': request})
        return Response(read_serializer.data)

    def delete(self,request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes_d([IsAuthenticated | IsSuperUser])
def create_product_attributes(request):
    serializer = BulkCreateProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    attributes = serializer.validated_data.get('attributes')

    for attribute in attributes:
        ProductAttribute.objects.create(**attribute)

    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['DELETE', 'PATCH'])
@permission_classes_d([IsAuthenticated | IsSuperUser])
def update_delete_product_attributes(request, id):
    attribute = get_object_or_404(ProductAttribute, id=id)

    if request.method == 'PATCH':
        serializer = UpdateAttributeForProductSerializer(data=request.data, instance=attribute, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
