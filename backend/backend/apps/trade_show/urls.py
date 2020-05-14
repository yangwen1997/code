from django.conf.urls import url
from .views import trade_search_name,tradeInfo_API

urlpatterns = [
    url('^search_namelt',trade_search_name.as_view()),
    url('^tradeAPI',tradeInfo_API.as_view())
]
