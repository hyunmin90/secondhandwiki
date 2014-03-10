from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'web.views.landing'), 
    url(r'^login/$', 'accounts.views.login'),
    url(r'^sign_up/$', 'accounts.views.sign_up'),

    url(r'^main/$', TemplateView.as_view(template_name='main.html')),
)
