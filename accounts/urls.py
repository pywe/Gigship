from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^how-it-works/$', views.how_it_works,name="how-it-works"),
    url(r'^accounts/registration/$', views.registration,name="registration"),
    url(r'^accounts/login/$', views.mylogin,name="login"),
    url(r'^accounts/logout/$', views.mylogout,name="logout"),
    url(r'^forgot-password/$', views.forgot,name="forgot-password"),
    url(r'^faq/$', views.faq,name="faq"),
    url(r'^support/$', views.support,name="support"),
    url(r'^accounts/create-freelancer/$', views.create_gigger,name="create-freelancer"),
    url(r'^accounts/create-employer/$', views.create_shipper,name="create-employer"),
    url(r'^accounts/dashboard/$', views.dashboard,name="dashboard"),
    url(r'^accounts/mygigs/$', views.mygigs,name="mygigs"),
    url(r'^accounts/myorders/$', views.myorders,name="myorders"),
    url(r'^accounts/add-gigs/$', views.add_services,name="add-gigs"),
    url(r'^accounts/services/$', views.services,name="services"),
    ]