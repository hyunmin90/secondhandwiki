from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^new_product/$', 'products.views.new_product'),

    # product page
    url(r'^view_product/(?P<slug>[a-zA-Z0-9\-\+]+)/$', 'products.views.view_product'),
    url(r'^view_product/(?P<slug>[a-zA-Z0-9\-\+]+)/tagging/$', 'products.views.view_product_tagging'),

    url(r'^delete_product/(?P<slug>[a-zA-Z0-9\-\+]+)/$', 'products.views.delete_product'),

    # for comments
    url(r'^new_comment/$', 'products.views.new_comment'),
    url(r'^delete_comment/$', 'products.views.delete_comment'),
    url(r'^edit_comment/$', 'products.views.edit_comment'),
    
    # for features
    url(r'^new_feature/$', 'products.views.new_feature'),

    # categories
    url(r'^camera/$', 'products.views.camera_page'),
    url(r'^(?P<category>.*)/$', 'products.views.view_category'),
)
