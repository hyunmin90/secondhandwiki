from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import connection

from accounts.models import Profile
from django.contrib.auth.models import User
from products.models import Products, Features, ProductTags, Comments, Categories 

import re
from django.utils import simplejson


@login_required
@csrf_protect
def main(request):
    allcategories = Categories.objects.all()
    return render(request, 'main.html', {'categories' : allcategories})   

#added it here 
import amazonproduct
#searchs amazon and assigns the price of the product from Amazon.com
def amazonsearch( query ):
    from lxml import etree
    #API Access keys
    config = {
              'access_key': 'AKIAIKDCGPZIH4ZFFQGQ',
              'secret_key': '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',
              'associate_tag' : 'themanhproj-20',
              'locale' : 'us'
              }
    #configuration of API
    api = amazonproduct.API(cfg = config)
    #search for related items
    items = api.item_search('All', Keywords = query)
    Price = 0.00
    #looks at first search result and lookups the price for it
    for stuff in items:
        #gets the ASIN number for the product
        ASIN = stuff.ASIN
        asin_string = '%s' %(ASIN)
        result = api.item_lookup(asin_string, ResponseGroup = 'OfferSummary')
        for item in result.Items.Item:
            print 'Name of Product: %s' %(stuff.ItemAttributes.Title)
            print 'URL Link of Product: %s' %(stuff.DetailPageURL)
            Price = int(item.OfferSummary.LowestNewPrice.Amount)/100.0
            print 'Price amount: %s' %(Price)
    #         print etree.tostring(item.OfferSummary.LowestNewPrice.Amount, pretty_print=True)
            print " "
        #only want first search result, usually the most accurate
        break;
    return Price


@login_required
@csrf_protect
def new_product(request):
    if request.method == 'POST':
        category = request.POST['category']
        product_name = request.POST['product_name']
        url = request.POST['url']
        description = request.POST['description']

        slug = slugify(product_name)

        price = amazonsearch(product_name)

        # Check if category already exists
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products_categories WHERE category_name=%s", [category])
        category_list = cursor.fetchall()

        allcategories = Categories.objects.all()

        if category_list: # Category exists
            the_category = category_list[0]

            # check whether product already exists
            cursor.execute("SELECT * FROM products_products WHERE product_name=%s OR slug=%s", [product_name, slug])
            product_list = cursor.fetchall()

            if len(product_list)>0: # product exists
                return render(request, 'new_product.html', {'exists':True, 'product_name':product_name, 'product_slug':slug, 'categories':allcategories})

            cursor.execute("INSERT INTO products_products(product_name, image, description, category_id, slug, price) VALUES(%s, %s, %s, %s, %s, %s)" , [product_name, url, description, the_category[0], slug, price])

        else:   # does not exist
            # add new category
            cursor.execute("INSERT INTO products_categories(category_name) VALUES(%s)", [category])

            # check whether product already exists
            cursor.execute("SELECT * FROM products_products WHERE product_name=%s or slug=%s", [product_name, slug])
            product_list = cursor.fetchall()

            if len(product_list)>0: # product exists
                return render(request, 'new_product.html', {'exists':True, 'product_name':product_name, 'product_slug':slug, 'categories':allcategories})

            # get category
            cursor.execute("SELECT * FROM products_categories WHERE category_name=%s", [category])
            category_list = cursor.fetchall()
            the_category = category_list[0]

            # add new product
            cursor.execute("INSERT INTO products_products(product_name, image, description, category_id, slug, price) VALUES(%s, %s, %s, %s, %s, %s)" , [product_name, url, description, the_category[0], slug, price])

        return HttpResponseRedirect('/products/view_product/'+slug)
    else:
        return render(request, 'new_product.html', {'categories':allcategories})

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

    # get features
    features = Features.objects.raw('SELECT * FROM products_features WHERE product_id = %s', [the_product.id])
    features = list(features)

    allcategories = Categories.objects.all()
    return render(request, 'view_product.html', {'product':the_product, 'comments':comments_sorted, 'features':features,'categories':allcategories})

@login_required
@csrf_protect
def view_product_tagging(request,slug):
    if request.method=="POST":
        content = request.POST['content']
        x = request.POST['x']
        y = request.POST['y']
        width = request.POST['width']
        height = request.POST['height']

        # save the new tag
        p = Products.objects.get(slug=slug)
        new_tag = ProductTags(product=p,content=content,x=x,y=y,width=width,height=height)
        new_tag.save()
        
        # get new list of tags 
        image_url = p.image
        tag_list = ProductTags.objects.filter(product=p)

        return render(request, 'tagging.html', {'tags':tag_list, 'url':image_url, 'slug':slug})
        
    else:
        p = Products.objects.get(slug=slug)
        image_url = p.image
        tag_list = ProductTags.objects.filter(product=p)
        
        return render(request, 'tagging.html', {'tags':tag_list, 'url':image_url, 'slug':slug})

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
        allcategories = Categories.objects.all()
        camera_category = Categories.objects.raw("SELECT * FROM products_categories WHERE category_name = 'camera'")[0]
        product_list = Products.objects.raw("SELECT * FROM products_products where category_id = %s", [camera_category.id])
        return render(request, 'category_page.html', {'product_list':product_list, 'category':"Camera", 'categories' : allcategories})
    except:
        return render(request, 'category_page.html', {'category':"Camera"})

@login_required
def view_category(request, category_name):
    try:
        allcategories = Categories.objects.all()
        current_category = Categories.objects.raw("SELECT * FROM products_categories WHERE category_name = category_name")[0]
        product_list = Products.objects.raw("SELECT * FROM products_products where category_id = %s", [current_category.id])

        return render(request, 'category_page.html', {'product_list':product_list, 'category':"Camera", 'categories' : allcategories})
    except:
        return render(request, 'category_page.html', {'category':category_name})

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
        comments = Comments.objects.raw("SELECT * FROM products_comments WHERE product_id = %s AND body = %s AND author_id = %s", [product_id, comment_body, request.user.id]) 
        new_comment = list(comments)[0]
        comment_id = new_comment.id

        html = "<li class=\'list-group-item\' id=\'comment_" + str(comment_id) + "\'><b>" + request.user.first_name + ":</b> " + comment_body + "<span style=\'float:right; color:blue;\' onclick=\"$(\'#id_comment_edit_" + str(comment_id) + "\').show(); $(\'#id_comment_edit_button_" + str(comment_id) + "\').show();\">Edit</span><span class=\'glyphicon glyphicon-remove\' style=\'float:right;\' onclick=\"delete_comment(" + str(comment_id) + ");\"></span><textarea id=\'id_comment_edit_" + str(comment_id) + "\' style=\'display:none;\'></textarea><button id=\'id_comment_edit_button_" + str(comment_id) + "\' style=\'display:none;\' onclick=\"edit_comment(" + str(comment_id) + ");\">submit edit</button></li>"

        allcategories = Categories.objects.all()

        data = {'first_name': request.user.first_name, 'comment_id': comment_id, 'html_string': html, 'body':new_comment.body, 'categories' : allcategories}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    
    else:
        return HttpResponseRedirect("/")

@login_required
@csrf_protect
def delete_comment(request):
    if request.method=="POST":
        comment_id = request.POST['comment_id']

        allcategories = Categories.objects.all()

        cursor = connection.cursor()
        # delete comment
        cursor.execute("DELETE FROM products_comments WHERE id = %s" , [comment_id])
        data = {'categories' : allcategories}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponseRedirect("/")    


@login_required
@csrf_protect
def edit_comment(request):
    if request.method=="POST":
        comment_id = request.POST['comment_id']
        comment_body = request.POST['comment_body']

        cursor = connection.cursor()
        # update comment
        cursor.execute("UPDATE products_comments SET body = %s WHERE id = %s", [comment_body, comment_id])

        #comment = Comments.objects.get(pk=comment_id)
        #comment.body = comment_body
        #comment.save()
        
        data = {"first_name":request.user.first_name}
        data = simplejson.dumps(data)
        return HttpResponse(data, mimetype='application/json')

    else:
        return HttpResponseRedirect("/")    

@login_required
@csrf_protect
def new_feature(request):
    if request.method=="POST":
        feature_name = request.POST['feature_name']
        feature_description = request.POST['feature_description']
        product_id = request.POST['product_id']

        # retrieve product
        the_product = Products.objects.get(id=product_id)
        slug = the_product.slug

        # save the new instance of feature
        new_feature = Features(feature_name = feature_name, description=feature_description, product = the_product, author = request.user)
        new_feature.save()

        return HttpResponseRedirect("/products/view_product/"+slug)
    else:
        # shouldn't come here ever
        return HttpResponseRedirect("/")


@csrf_protect
def search_product(request):
    if request.method=='POST':
        search_query = request.POST['search_query']
        queryset = search_query.split()

        product_list = []

        # 'with' search
        if 'with' in queryset:
            index = queryset.index('with')
            last_index = len(queryset)-1

            number = int(queryset[last_index-1])
            
            # query: 'with 3 features/comments'
            if index == 0:
                if queryset[last_index] == 'features' or queryset[last_index] == 'feature':
                    products = Products.objects.raw("SELECT * FROM products_products WHERE id IN (SELECT product_id FROM (SELECT product_id, COUNT(feature_name) FROM products_features GROUP BY product_id HAVING COUNT(feature_name) >= %s) AS sub_table)", [number])
                    products = list(products)            

                elif queryset[last_index] == 'comments' or queryset[last_index] == 'comment':
                    products = Products.objects.raw("SELECT * FROM products_products WHERE id IN (SELECT product_id FROM (SELECT product_id, COUNT(body) FROM products_comments GROUP BY product_id HAVING COUNT(body) >= %s) AS sub_table)", [number])
                    products = list(products)            
                
            # query: 'with 3 features and 2 comments'
            elif index == 0 and 'and' in queryset:
                # change all to plural form
                if 'feature' in queryset:
                    queryset = queryset.replace('feature', 'features')
                if 'comments' in queryset:
                    queryset = queryset.replace('comment', 'comments')
                
                feature_index = queryset.index('features')
                comment_index = queryset.index('comments')

                feature_num = queryset[feature_index-1]
                comment_num = queryset[comment_num-1]
                
                products = Products.objects.raw("SELECT *, COUNT(feature_name), COUNT(body) FROM products_products NATURAL JOIN products_features NATURAL JOIN products_comments GROUP BY COUNT(feature_name), COUNT(body) HAVING COUNT(feature_name) >= %s AND COUNT(body) >= %s",[feature_num, comment_num])
                products = list(products)
            
            return render(request, 'search_results.html', {'search_results': products})

        # user search
        elif 'user' in queryset:
            user_string = ''
            for q in queryset:
                if q != 'user':
                    user_string = user_string + q

            products = Products.objects.raw("SELECT id, product_name, description, image, category_id, slug FROM auth_user NATURAL JOIN accounts_profile NATURAL JOIN products_products WHERE first_name LIKE %s", tuple(["%"+user_string+"%"]))

            return render(request, 'search_results.html', {'search_results': products}) 

        # normal search
        else:
            #for each word in the search query
            for q in queryset :
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
