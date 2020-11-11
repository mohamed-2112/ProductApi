from django.db import models

# Create your models here.
# product_code, name, price, quantity
#category_id, name, parent_category


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    parent_category = models.CharField(max_length=100, null=True)


class Products(models.Model):
    product_code = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
