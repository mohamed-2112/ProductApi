from rest_framework import serializers
from .models import Products
from .models import Category

class CategorysSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'name', 'parent_category')


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorysSerializer(read_only=True, many=True)
    class Meta:
        model = Products
        fields = ('product_code', 'name', 'price', 'quantity','categories')
