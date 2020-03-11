from django.conf.urls import url
from .views import JBXX,Shareholder

urlpatterns = [
    url(r'^index/$',JBXX.as_view()),
    url(r'^Shareholder/$',Shareholder.as_view())
]
