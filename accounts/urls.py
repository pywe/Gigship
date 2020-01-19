from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^how-it-works/$', views.how_it_works,name="how-it-works"),
    url(r'^registration/$', views.registration,name="registration"),
    url(r'^login/$', views.login,name="login"),
    url(r'^forgot-password/$', views.forgot,name="forgot-password"),
    url(r'^faq/$', views.faq,name="faq"),
    url(r'^create-resume/$', views.create_resume,name="create-resume"),
    url(r'^support/$', views.support,name="support"), 
    url(r'^post-job/$', views.post_job,name="post-job"),  
    url(r'^dashboard/$', views.dashboard,name="dashboard"),  
    ]