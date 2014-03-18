from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import connection

from products.models import Products, Features, Comments, Categories 


import re

# Create your views here.
@login_required
@csrf_protect
def main(request):
    return render(request, 'main.html', {})    

@login_required
@csrf_protect
def new_product(request):
    if request.method == 'POST':
        category = request.POST['category']
        product_name = request.POST['product_name']
        description = request.POST['description']

        slug = slugify(product_name)

        # Check if category already exists
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products_categories WHERE category_name=%s", [category])
        category_list = cursor.fetchall()

        if category_list: # Category exists
            the_category = category_list[0]

            cursor.execute("INSERT INTO products_products(`product_name`, `description`, `category_id`, `slug`) VALUES(%s, %s, %s, %s)" , [product_name, description, the_category[0], slug])

        else:   # does not exist
            # add new category
            cursor.execute("INSERT INTO products_categories(`category_name`) VALUES(%s)", [category])


            cursor.execute("SELECT * FROM products_categories WHERE category_name=%s", [category])
            category_list = cursor.fetchall()
        
            cursor.execute("INSERT INTO products_products(`product_name`, `description`, `category`, `slug`) VALUES(%s, %s, %s, %s)" , [product_name, description, len(category_list)+1, slug])

        return HttpResponseRedirect('/products/view_product/'+slug)
    else:
        return render(request, 'new_product.html', {})


@login_required
def view_product(request,slug):
    product = Products.objects.raw('SELECT * FROM products_products WHERE slug=%s', [slug])
    product = list(product)
    the_product = product[0]

    return render(request, 'view_product.html', {'product':the_product})
    
def slugify(text):
    # convert spaces to dashes
    text = re.sub(r'\s+', '-', text.strip())
    #Convert underscores to dashes
    text = re.sub(r'\_', '-', text.strip())
    # convert anything not a letter or number or - or _ or to empty string
    text = re.sub(r'[^a-zA-Z0-9\-\_]', '', text)

    # convert to lower case. That is all.
    return text.lower()
