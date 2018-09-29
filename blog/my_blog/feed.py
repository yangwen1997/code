from django.contrib.syndication.views import Feed
from my_blog.models import Entry


# 订阅
'''
title link description 相当于三个html中的标签
里面的内容都可以随便写
items :获取数据的列表
item:相当于每条数据，item.title,item.abstract 就相当于把items中每条数据的这两个字段值返回
'''
class Subscribe(Feed):
    title = '冯的博客'
    link = '/f/'
    description = '冯的最新博客'
    def items(self):
        return Entry.objects.order_by('-created_time')[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.abstract



