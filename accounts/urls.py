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
<<<<<<< HEAD
    url(r'^post-job/$', views.post_job,name="post-job"),
    url(r'^accounts/create-freelancer/$', views.create_freelancer,name="create-freelancer"),
    url(r'^accounts/create-employer/$', views.create_employer,name="create-employer"),  
=======
    url(r'^post-job/$', views.post_job,name="post-job"),  
<<<<<<< HEAD
    url(r'^dashboard/$', views.dashboard,name="dashboard"),
    url(r'^myjobs/$', views.myjobs,name="myjobs"),    
=======
    url(r'^dashboard/$', views.dashboard,name="dashboard"),  
>>>>>>> 7a6047e951fd1907ae6d09017ed2877e555897e8
>>>>>>> c0d8a3c5c05c998d412563555273853c8626f1a8
    ]