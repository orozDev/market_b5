from pprint import pprint

from rest_framework import serializers

from store.models import Product, Category, Tag, ProductAttribute, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class AttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ImageForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('product',)


class ListProductSerializer(serializers.ModelSerializer):

    # category = serializers.CharField(source='category.name')
    # category_id = serializers.CharField(source='category.id')

    attributes = AttributeForProductSerializer(many=True)
    images = ImageForProductSerializer(many=True)
    image = serializers.ImageField()

    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('content',)


class DetailProductSerializer(serializers.ModelSerializer):

    attributes = AttributeForProductSerializer(many=True)
    images = ImageForProductSerializer(many=True)
    image = serializers.ImageField()

    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(validators=[])

    class Meta:
        model = Product
        fields = '__all__'

    # def create(self, validated_data):
    #
    #     image = validated_data.pop('image')
    #     tags = validated_data.pop('tags')
    #
    #     product = Product.objects.create(**validated_data)
    #     product.tags.add(*tags)
    #     product.save()
    #
    #     product_image = ProductImage.objects.create(product=product)
    #     product_image.image.save(image.name, image)
    #     product_image.save()
    #
    #     return product

    def create(self, validated_data):
        # request = self.context['request']

        image = validated_data.pop('image')
        product = super().create(validated_data)

        product_image = ProductImage.objects.create(product=product)
        product_image.image.save(image.name, image)
        product_image.save()

        return product

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        product: Product = super().update(instance, validated_data)

        if image:
            product_image = product.images.first()
            product_image.image.save(image.name, image)
            product_image.save()

        return product


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class BulkCreateProductAttributeSerializer(serializers.Serializer):

    attributes = ProductAttributeSerializer(many=True)


class UpdateAttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)





