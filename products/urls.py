from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^new_product/$', 'products.views.new_product'),
    url(r'^view_product/(?P<slug>[a-zA-Z0-9\-\+]+)$', 'products.views.view_product'),
    url(r'^delete_product/(?P<slug>[a-zA-Z0-9\-\+]+)$', 'products.views.delete_product'),

    # categories
    url(r'^camera/$', 'products.views.camera_page'),
)
