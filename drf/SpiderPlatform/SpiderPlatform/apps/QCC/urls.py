from django.conf.urls import url
from .views import JBXX

urlpatterns = [
    url(r'^index/$',JBXX.as_view())
]
