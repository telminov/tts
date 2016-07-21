from django.conf.urls import url, include
import core.views

urlpatterns = [
    url(r'^generate_speech/$', core.views.generate_speech, name='generate_speech'),
    url(r'^play_speech/$', core.views.play_speech, name='play_speech'),
    url(r'^docs/', include('rest_framework_swagger.urls', namespace='docs'))
]
