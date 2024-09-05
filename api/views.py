from pprint import pprint
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.decorators import api_view

from api.serializers import DetailProductSerializer, ListProductSerializer, ProductSerializer, \
    BulkCreateProductAttributeSerializer, ProductAttributeSerializer, UpdateAttributeForProductSerializer
from store.models import Product, ProductAttribute
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status


@api_view(['GET', 'POST'])
def list_create_products(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            read_serializer = ListProductSerializer(product, context={'request': request})
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(content__icontains=search)
        )

    orders = ['name', 'price', 'rating', 'created_at']
    ordering: str = request.GET.get('ordering')

    if ordering and ordering.split('-')[-1] in orders:
        products = products.order_by(ordering)

    page = request.GET.get('page') or 1
    page_size = request.GET.get('page_size') or 2
    count = products.count()

    pagin = Paginator(products, page_size)
    products = pagin.get_page(page)

    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response({
        'page': page,
        'page_size': page_size,
        'page_count': pagin.num_pages,
        'count': count,
        'data': serializer.data
    })


@api_view(['GET', 'PATCH', 'DELETE'])
def detail_update_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'PATCH':
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(instance=product, context={'request': request})
        return Response(read_serializer.data)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = DetailProductSerializer(instance=product, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def create_product_attributes(request):
    serializer = BulkCreateProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    attributes = serializer.validated_data.get('attributes')

    for attribute in attributes:
        ProductAttribute.objects.create(**attribute)

    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['DELETE', 'PATCH'])
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
