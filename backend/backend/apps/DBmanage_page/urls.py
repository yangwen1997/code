from django.conf.urls import url
from .views import DBmanage
urlpatterns = [
    url('^dbpage',DBmanage.as_view())
]
