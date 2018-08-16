from django.urls import path,include,re_path
from django.conf.urls import url
from django.contrib import admin
from .views import (post_create,post_list, post_detail,post_update,post_delete)
from . import views


app_name = 'polls'

urlpatterns = [
    path('', post_list, name="list"),
    path('create/', post_create),
    re_path(r'^(?P<id>\d+)/$', post_detail, name= "detail"),
    url(r'^(?P<id>\d+)/edit/', post_update,name="update"),
    re_path(r'^(?P<id>\d+)/delete/', post_delete),
  	
]
