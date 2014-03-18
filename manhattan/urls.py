from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.landing'), 
    url(r'^login/$', 'accounts.views.login'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^sign_up/$', 'accounts.views.sign_up'),
    url(r'^main/$', 'products.views.main'),
    
    # search function
    url(r'^search/$', 'products.views.search_product'),

    # products
    url(r'^products/', include('products.urls')),
)
