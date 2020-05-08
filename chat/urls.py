from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^chat/$', views.chat,name="chat"),

    # message api enpoints
    url(r'^chat/get-people/$', views.getPeople,name="get-people"),
    url(r'^chat/get-messages/$', views.getMessages,name="get-messages"),
]