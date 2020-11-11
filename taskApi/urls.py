from django.urls import path
from django.conf.urls import url 
from . import views
urlpatterns = [
    url(r'^product$', views.product),
    url(r'^product/(.*)$', views.productid),
    url(r'^category$', views.category),
    url(r'^category/(.*)$', views.categoryid),
    #path('', views.index, name='index'),
]