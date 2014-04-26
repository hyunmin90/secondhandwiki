import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manhattan.settings")

from product.models import *
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


