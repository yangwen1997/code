from django.conf.urls import url
from my_blog import views
'''
(?P<blog_id>[0-9]+): 传入一个参数blog_id为0-9至少一个 
'''
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)?/$', views.base, name='base'),
    url(r'^blog/(?P<blog_id>[0-9]+)',views.detail,name='blog_detail'),
    url(r'^categoy/(?P<category_id>[0-9]+)',views.catagory,name='blog_catagory'),
    url(r'^tags/(?P<tags_id>[0-9]+)$',views.Tags,name='blog_tags'),
    url(r'^search$',views.search,name='search'),
    url(r'^archives/(?P<year>[0-9]+)/(?P<month>[0-9]+)$',views.archives,name='blog_archives'),
    url(r'^reply/(?P<comment_id>\d+)/$', views.reply, name='comment_reply'),


]
