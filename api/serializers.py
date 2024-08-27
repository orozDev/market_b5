from rest_framework import serializers

from store.models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    # category = serializers.CharField(source='category.name')
    # category_id = serializers.CharField(source='category.id')

    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('content',)




