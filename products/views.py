from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from accounts.models import *

# Create your views here.
@login_required
@csrf_protect
def main(request):
    return render(request, 'main.html', {})    

@login_required
@csrf_protect
def new_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        description = request.POST['description']
        Productobjects.objects.raw('
        ALTER TABLE Products
        ADD ( Product_name %s char(50) NOT NULL,
        Descriptor %s char(1000))
        ADD CONSTRAINT FOREIGN KEY feature_ID REFERENCES Features;
        ' , [product_name], [description], [)


    else:
        return render(request, 'new_product.html', {})

    
    

