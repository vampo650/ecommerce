__author__ = 'vamsi'

from django.conf.urls import url, include
from django.contrib import admin
from views import Home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^$', Home.as_view()),
                  url(r'^admin/', admin.site.urls),
                  url(r'^catalogue/', include('catalogue.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
