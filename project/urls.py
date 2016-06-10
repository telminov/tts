"""project URL Configuration"""

from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

import core.views

UUID_REGEXP = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/some_model/')),
    url(r'^admin/', admin.site.urls),
    url(r'^some_model/$', core.views.SomeModelList.as_view()),
    url(r'^some_model/(?P<pk>[0-9]+)/$', core.views.SomeModelDetail.as_view()),
    url(r'^generate_speach/(.*)/$', core.views.generate_speach),
    url(r'^play_speach/(%s)/$' % UUID_REGEXP, core.views.play_speach),
]
