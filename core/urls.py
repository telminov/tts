from django.conf.urls import url
from core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^generate/$', views.Generate.as_view(), name='generate'),
    url(r'^speech/(?P<uuid>[^/]+)/$', views.Speech.as_view(), name='speech'),
]
