from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^how-it-works/$', views.how_it_works,name="how-it-works"),
    url(r'^registration/$', views.registration,name="registration"),
    url(r'^login/$', views.login,name="login"),
    url(r'^forgot-password/$', views.forgot,name="forgot-password"),
    ]