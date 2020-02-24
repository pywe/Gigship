from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^gigs/create-resume/$', views.create_resume,name="create-resume"),
    url(r'^gigs/create-job/$', views.create_job,name="create-job"),
    url(r'^gigs/create-services/$', views.create_services,name="create-services"),
    url(r'^gigs/search-gigs/$', views.search_api,name="search-gigs"),
    url(r'^gigs/service-files/(?P<id>[-\w]+)/$', views.add_service_files,name="services-files"),
    url(r'^gigs/search-gigs/$', views.search_api,name="search-gigs"),
    ]