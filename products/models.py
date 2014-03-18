from django.db import models
from accounts.models import Profile

class Products(models.Model):
    product_name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=1000,blank=True,null=True)
    image = models.CharField(max_length=100,blank=True,null=True)
    category = models.ForeignKey('Categories')
  
class Features(models.Model):
    feature_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,blank=True,null=True)
    product = models.ForeignKey('Products')

class Comments(models.Model):
    author = models.ForeignKey('accounts.Profile')
    product = models.ForeignKey('Products')
    body = models.CharField(max_length=1000)

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('Categories', blank=True, null=True)
    


    