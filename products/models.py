from django.db import models
from django.contrib.auth.models import User

from accounts.models import Profile

import datetime

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', blank=True, null=True)

class Products(models.Model):
    product_name = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=1000,blank=True,null=True)
    image = models.CharField(max_length=100,blank=True,null=True)
    category = models.ForeignKey(Categories)
    slug = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    
  
class Features(models.Model):
    feature_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,blank=True,null=True)
    product = models.ForeignKey(Products)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(default=datetime.datetime.now)

class Comments(models.Model):
    product = models.ForeignKey(Products)
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    

    


    
