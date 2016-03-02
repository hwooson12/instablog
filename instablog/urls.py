"""instablog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog import views as blog_views

urlpatterns = [
    url(r'^post/(?P<pk>[0-9]+)/edit/$', blog_views.edit_post, name='edit_post'),
    url(r'^post/create/$', blog_views.create_post, name='create_post'),
    url(r'^$', blog_views.list_posts, name='list_posts'),
    url(r'^post/(?P<pk>[0-9]+)/$', blog_views.view_post, name='view_post'),
    url(r'^hello/$', blog_views.hello_with_tem),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', blog_views.delete_post, name='delete_post'),
    url(r'^comment/(?P<pk>[0-9]+)/delete/$', blog_views.delete_comment, name='delete_comment'),
    url(r'^admin/', admin.site.urls),
]
