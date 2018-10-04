from django.conf.urls import url
from auser import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$', views.register_exist),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^info/$', views.user_center_info),
    url(r'^info/user_center_info.html$', views.user_center_info),
    url(r'^info/user_center_order.html$', views.user_center_order),
    url(r'^info/user_center_site.html$', views.user_center_site),
    url(r'^loginout$', views.loginout)
]
