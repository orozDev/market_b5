from pprint import pprint

from rest_framework.decorators import api_view

from api.serializers import ProductSerializer
from store.models import Product
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    pprint(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])
def detail_products(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(instance=product)
    pprint(serializer.data)
    return Response(serializer.data)