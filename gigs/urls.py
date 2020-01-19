from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^gigs/create-resume/$', views.create_resume,name="create-resume"),
    url(r'^gigs/create-job/$', views.create_job,name="create-job"),
    ]