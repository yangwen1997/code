from django.conf.urls import url
from .views import sdxy_data_search,sdxy_basic,bdxy_basic

urlpatterns = [
    url('^sdxy_data_search',sdxy_data_search.as_view()),
    url('^sdxy_basic',sdxy_basic.as_view()),
    url('^bdxy_basic',bdxy_basic.as_view()),
]

