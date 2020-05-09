from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^gigs/create-resume/$', views.create_resume,name="create-resume"),
    url(r'^gigs/create-job/$', views.create_job,name="create-job"),
    url(r'^gigs/create-services/$', views.create_services,name="create-services"),
    url(r'^gigs/search-gigs/$', views.search_api,name="search-gigs"),
    url(r'^gigs/service-files/(?P<id>[-\w]+)/$', views.add_service_files,name="services-files"),
    url(r'^gigs/search-gigs/$', views.search_api,name="search-gigs"),
    url(r'^gigs/order/(?P<id>[-\w]+)/$', views.order,name="order"),
    url(r'^gigs/create-order/$', views.create_order,name="create-order"),
    url(r'^gigs/create-request/$', views.create_request,name="create-request"),
    url(r'^gigs/accept-request/(?P<id>[-\w]+)/$', views.accept_request,name="accept-request"),
    url(r'^gigs/get-categories/$', views.get_categories,name="get-categories"),

    url(r'^gigs/update-order-status/$', views.updateOrder,name="update-order"),
    ]