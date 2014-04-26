import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manhattan.settings")

from products.models import Products, Categories, Features, ProductTags, Comments

import amazonproduct

def amazonPriceSearch( query ):
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

def amazonListSearch( query, num_results ):
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
    count = 0
    #product name, image url, features concatenated into a string
    product_list = []
    #looks at first search result and lookups the price for it
    for stuff in items:
        #gets the ASIN number for the product
        ASIN = stuff.ASIN
        asin_string = '%s' %(ASIN)
        imagesresult = api.item_lookup(asin_string, ResponseGroup = 'Images')
#         print etree.tostring(imagesresult, pretty_print=True)
        newproduct = "hi"
        productname = stuff.ItemAttributes.Title
#         print 'Name of Product: %s' %(productname)
        for item in imagesresult.Items.Item:
            imageURL = item.LargeImage.URL
            break
        
        mediumresult = api.item_lookup(asin_string, ResponseGroup = 'Large')
        for item in mediumresult.Items.Item:
#             print etree.tostring(item, pretty_print=True)
            featurecount = 0
            description = ''
            for stuff in item.ItemAttributes.Feature:
#                 print etree.tostring(stuff)
#                 print stuff
                description += stuff +', '
                featurecount+=1
                if featurecount == 4:
                    break
#             print etree.tostring(item.ItemAttributes.Feature)
        if count == num_results:
            break
        count+=1
        
        newproduct = (productname,imageURL,description)
        product_list.append(newproduct)
        
    return product_list

import re
def slugify(text):
    # convert spaces to dashes
    text = re.sub(r'\s+', '-', text.strip())
    # convert underscores to dashes
    text = re.sub(r'\_', '-', text.strip())
    # convert anything not a letter or number or - or _ or to empty string
    text = re.sub(r'[^a-zA-Z0-9\-\_]', '', text)
    # convert to lower case. That is all.
    return text.lower()

'''
these 2 lines below will change what we add to the database
'''
#category TV
target_category = Categories.objects.get(category_name = "TV")
newproductstoadd = amazonListSearch("hdtv", 5)

for newproduct in newproductstoadd:
	product_name = newproduct[0]
	print product_name
	imageURL = newproduct[1]
	print imageURL
	description = newproduct[2]
	print description
	slug = slugify(product_name)
	print slug
	price = amazonPriceSearch(product_name)
	print price
	print " "
	p1 = Products(product_name = product_name, image = imageURL , description = description, category = target_category, slug = slug, price = price)
	p1.save()



