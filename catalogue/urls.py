__author__ = 'vamsi'

from django.conf.urls import url
from catalogue.api.views import CatalogueList, CatalogueDetail

urlpatterns = [
    url(r'^$', CatalogueList.as_view()),
    url(r'^(?P<catalogue_id>\w+)$', CatalogueDetail.as_view()),
]
