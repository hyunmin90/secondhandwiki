from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import connection

from accounts.models import Profile
from products.models import Products, Features, Comments, Categories 

import re
from django.utils import simplejson


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

            # check whether product already exists
            cursor.execute("SELECT * FROM products_products WHERE product_name=%s OR slug=%s", [product_name, slug])
            product_list = cursor.fetchall()

            if len(product_list)>0: # product exists
                return render(request, 'new_product.html', {'exists':True, 'product_name':product_name, 'product_slug':slug})

            cursor.execute("INSERT INTO products_products(product_name, description, category_id, slug) VALUES(%s, %s, %s, %s)" , [product_name, description, the_category[0], slug])

        else:   # does not exist
            # add new category
            cursor.execute("INSERT INTO products_categories(category_name) VALUES(%s)", [category])

            # check whether product already exists
            cursor.execute("SELECT * FROM products_products WHERE product_name=%s or slug=%s", [product_name, slug])
            product_list = cursor.fetchall()

            if len(product_list)>0: # product exists
                return render(request, 'new_product.html', {'exists':True, 'product_name':product_name, 'product_slug':slug})

            # get category
            cursor.execute("SELECT * FROM products_categories WHERE category_name=%s", [category])
            category_list = cursor.fetchall()
            the_category = category_list[0]

            # add new product
            cursor.execute("INSERT INTO products_products(product_name, description, category_id, slug) VALUES(%s, %s, %s, %s)" , [product_name, description, the_category[0], slug])

        return HttpResponseRedirect('/products/view_product/'+slug)
    else:
        return render(request, 'new_product.html', {})


#@login_required
#@csrf_protect
#def new_description(request):


@login_required
def view_product(request,slug):
    # get product
    product = Products.objects.raw('SELECT * FROM products_products WHERE slug = %s', [slug])
    product = list(product)
    the_product = product[0]

    # get comments
    comments = Comments.objects.raw('SELECT * FROM products_comments WHERE product_id = %s', [the_product.id])
    comments = list(comments)

    comments_sorted = sorted(comments, key=lambda x: x.id)

    return render(request, 'view_product.html', {'product':the_product, 'comments':comments_sorted,})


@login_required
@csrf_protect
def delete_product(request, slug):
    cursor = connection.cursor()
    
    # delete features associated with product
    # delete comments associated with product 

    # delete the product itself
    cursor.execute("DELETE FROM products_products WHERE slug = %s", [slug])

@login_required
def camera_page(request):
    try:
        camera_category = Categories.objects.raw("SELECT * FROM products_categories WHERE category_name = 'camera'")[0]
        product_list = Products.objects.raw("SELECT * FROM products_products where category_id = %s", [camera_category.id])
        return render(request, 'category_page.html', {'product_list':product_list, 'category':"Camera"})
    except:
        return render(request, 'category_page.html', {'category':"Camera"})


@login_required
@csrf_protect
def new_comment(request):
    if request.method=="POST":
        comment_body = request.POST['comment_body']
        product_id = request.POST['product_id']
        cursor = connection.cursor()
        
        # add new comment 
        cursor.execute("INSERT INTO products_comments(product_id, body, author_id) VALUES(%s, %s, %s)" , [product_id, comment_body, request.user.id])
    
        # get the newly added comment
        comments = Comments.objects.raw("SELECT * FROM products_comments") 
        comments = list(comments)
        comment = comments[len(comments)-1]
        comment_id = comment.id

        data = {'first_name': request.user.first_name, 'comment_id': comment_id,}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    
    else:
        return HttpResponseRedirect("/")

@login_required
@csrf_protect
def delete_comment(request):
    if request.method=="POST":
        comment_id = request.POST['comment_id']

        cursor = connection.cursor()
        # delete comment
        cursor.execute("DELETE FROM products_comments WHERE id = %s" , [comment_id])
        data = {}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponseRedirect("/")    

@csrf_protect
def search_product(request):
    if request.method=='POST':
        search_query = request.POST['search_query']
        queryset = search_query.split()
        #default list
        product_list = []
        #for each word in the search query
        for q in queryset :
            #i am not too sure if i can mix SQL and django.object.raw syntax, LIKE is regex for SQL
            products = Products.objects.raw("SELECT * FROM products_products WHERE slug LIKE %s", tuple(["%"+q+"%"]))
            prod_to_list = list(products)
            product_list = product_list + prod_to_list
        
        #a list of all products that match the search results
        productlist_without_duplicates = list(set(product_list))
        productlist_with_first_5_results = productlist_without_duplicates[:5]

        return render(request, 'search_results.html', {'search_results': productlist_with_first_5_results })
    else:
        return HttpResponseRedirect('/')
   
def slugify(text):
    # convert spaces to dashes
    text = re.sub(r'\s+', '-', text.strip())
    # convert underscores to dashes
    text = re.sub(r'\_', '-', text.strip())
    # convert anything not a letter or number or - or _ or to empty string
    text = re.sub(r'[^a-zA-Z0-9\-\_]', '', text)
    # convert to lower case. That is all.
    return text.lower()
