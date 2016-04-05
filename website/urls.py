from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'import/([\w\s]+)$', views.test),
    url(r'$', views.index),
]
