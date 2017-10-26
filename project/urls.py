from rest_framework.documentation import include_docs_urls
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='TTS API')),
    url(r'^', include('core.urls', namespace='core'))
]
