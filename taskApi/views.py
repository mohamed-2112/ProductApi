from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from taskApi.serializers import ProductsSerializer, CategorysSerializer
from taskApi.models import Products
from taskApi.models import Category


# p2.article_set.clear()
def clearManyToManyRelation(product_code):
    try:
        #category = Category.objects.get(category_id=category_id)
        product = Products.objects.get(product_code=product_code)
        product.categories.clear()
        # product.categories.add(category)
    except Exception as e:
        print(e)
        return 'category does not exist'


def saveProductCategory(product_code, category_id):
    try:
        category = Category.objects.get(category_id=category_id)
        product = Products.objects.get(product_code=product_code)
        product.categories.add(category)
    except Exception as e:
        print(e)
        return 'category does not exist'


def ChekCategoryExist(category_id):
    try:
        print(category_id)
        category_data = Category.objects.get(category_id=category_id)
        print(category_data)
        return True
    except:
        return False


def addcategory(category_data):
    category_serializer = CategorysSerializer(data=category_data)
    print(category_serializer)
    if category_serializer.is_valid():
        category_serializer.save()
        return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def product(request):
    if request.method == 'GET':
        products_list = Products.objects.all()
        products_list_serializer = ProductsSerializer(products_list, many=True)
        return JsonResponse(products_list_serializer.data, safe=False)
    else:
        product_data = JSONParser().parse(request)
        product_serializer = ProductsSerializer(
            data=product_data['product_info'])
        if product_serializer.is_valid():
            print('valid data')
            product_serializer.save()
            product_categories = product_data['product_category']
            for category_code in product_categories:
                saveProductCategory(
                    product_data['product_info']['product_code'], category_code)
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('not valid')
            return JsonResponse({'message': 'Request Not Valid'}, status=status.HTTP_204_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def productid(request, product_code):
    try:
        product = Products.objects.get(product_code=product_code)
    except:
        return JsonResponse({'message': 'Products does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        product_serializer = ProductsSerializer(product)
        return JsonResponse(product_serializer.data)
    elif request.method == 'PUT':
        product_data = JSONParser().parse(request)
        product_serializer = ProductsSerializer(
            product, data=product_data['product_info'])
        if product_serializer.is_valid():
            product_serializer.save()
            product_categories = product_data['product_category']
            clearManyToManyRelation(
                product_data['product_info']['product_code'])
            for category_code in product_categories:
                saveProductCategory(
                    product_data['product_info']['product_code'], category_code)
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category(request):
    if request.method == 'GET':
        CategoryObj = Category.objects.all()
        Category_Serializer = CategorysSerializer(CategoryObj, many=True)
        return JsonResponse(Category_Serializer.data, safe=False)
    else:
        category_data = JSONParser().parse(request)
        # check if the parent category id exist
        if category_data["parent_category"]:
            if ChekCategoryExist(category_data["parent_category"]):
                return addcategory(category_data)
            return JsonResponse({'message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return addcategory(category_data)


@api_view(['GET', 'PUT', 'DELETE'])
def categoryid(request, category_id):
    try:
        category = Category.objects.get(category_id=category_id)
    except:
        return JsonResponse({'message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        category_serializer = CategorysSerializer(category)
        return JsonResponse(category_serializer.data)
    elif request.method == 'PUT':
        category_data = JSONParser().parse(request)
        try:
            CategoryTest = Category.objects.get(
                category_id=category_data["parent_category"])
            # one category cant be the parent of itself
            if int(category_id) != category_data["parent_category"]:
                category_serializer = CategorysSerializer(
                    category, data=category_data)
                if category_serializer.is_valid():
                    category_serializer.save()
                    return JsonResponse(category_serializer.data, status=status.HTTP_201_CREATED)
                return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponse("one category cant be the parent of itself")
        except:
            return JsonResponse({'message': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
    else:
        category.delete()
        return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
