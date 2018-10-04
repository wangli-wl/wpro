from django.conf.urls import url
from agoods import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^list/$', views.list),
    url(r'^list/detail.html$', views.detail),
    url(r'^cart.html$', views.cart)
]
