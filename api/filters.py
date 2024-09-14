from django_filters import rest_framework as filters

from store.models import Product, Category


class ProductFilter(filters.FilterSet):

    # price = django_filters.NumericRangeFilter()

    price_from = filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = filters.NumberFilter(lookup_expr='lte', field_name='price')
    categories = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(), field_name='category')

    # total_price_from = django_filters.NumberFilter(method='filter_total_price_from')
    # total_price_to = django_filters.NumberFilter(method='filter_total_price_to')

    class Meta:
        model = Product
        fields = ['tags', 'user', 'receive_type', 'rating', 'is_published']

    # def filter_total_price_from(self, queryset, name, value, *args, **kwargs):
    #
    #     product_ids = [product.id
    #                    for product in list(filter(lambda product: product.total_price <= value, queryset))]
    #
    #     return queryset.filter(id__in=product_ids)
    #
    # def filter_total_price_to(self, queryset, name, value, *args, **kwargs):
    #
    #     product_ids = [product.id
    #                    for product in list(filter(lambda product: product.total_price >= value, queryset))]
    #
    #     return queryset.filter(id__in=product_ids)
    #
    #

