from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'manhattan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'web.views.landing'), 
    url(r'^login/$', 'accounts.views.login'),
    url(r'^main/$', TemplateView.as_view(template_name='main.html')),
)
