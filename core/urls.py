from django.conf.urls import url
import core.views

urlpatterns = [
    url(r'^$', core.views.index),
    url(r'^generate/$', core.views.generate, name='generate'),
    url(r'^get_file/$', core.views.get_file, name='get_file'),
]
