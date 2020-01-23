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
    url(r'^accounts/create-freelancer/$', views.create_freelancer,name="create-freelancer"),
    url(r'^accounts/create-employer/$', views.create_employer,name="create-employer"),  
    url(r'^accounts/dashboard/$', views.dashboard,name="dashboard"),
    url(r'^accounts/myjobs/$', views.myjobs,name="myjobs"),
    url(r'^accounts/add-services/$', views.add_services,name="add-services"),
    ]