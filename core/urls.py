from django.conf.urls import url
from core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^generate/$', views.Generate.as_view(), name='generate'),
    url(r'^voice/(?P<uuid>[^/]+)/$', views.GetVoice.as_view(), name='voice'),
]
