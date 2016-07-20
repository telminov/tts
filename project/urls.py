"""project URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework import routers
import core.views

UUID_REGEXP = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

router = routers.DefaultRouter()
router.register('SomeModel', core.views.SomeModelViewSet, base_name='SomeModelViewSet')

example_rest = [
    url(r'^some_model/$', core.views.SomeModelList.as_view(), name='some_models'),
    url(r'^some_model/(?P<pk>[0-9]+)/$', core.views.SomeModelDetail.as_view(), name='some_model'),
]

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/some_model/')),
    url(r'^admin/', admin.site.urls),
    url(r'example/', include(example_rest, namespace='example')),
    url(r'^generate_speech/$', core.views.generate_speach),
    url(r'^play_speech/$', core.views.play_speech),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
