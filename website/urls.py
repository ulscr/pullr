from django.conf.urls import url

from . import views

app_name = 'website'
urlpatterns = [
    url(r'import/$', views.import_names, name="import"),
    url(r'$', views.index, name="index"),
]
