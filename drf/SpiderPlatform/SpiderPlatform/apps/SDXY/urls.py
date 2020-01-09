from django.conf.urls import url
from .views import sdxy

urlpatterns = [
    url('index/',sdxy.as_view())
]
