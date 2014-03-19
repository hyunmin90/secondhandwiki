from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Add new
    url(r'^new_product/$', 'products.views.new_product'),
    url(r'^new_comment/(?P<product_slug>[a-zA-Z0-9\-\+]+)$', 'products.views.new_comment'),
    url(r'^new_description/(?P<product_slug>[a-zA-Z0-9\-\+]+)$', 'products.views.new_description'),


    url(r'^view_product/(?P<slug>[a-zA-Z0-9\-\+]+)$', 'products.views.view_product'),
    url(r'^delete_product/(?P<slug>[a-zA-Z0-9\-\+]+)$', 'products.views.delete_product'),

    

    # categories
    url(r'^camera/$', 'products.views.camera_page'),
)
