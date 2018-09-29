from django.contrib import admin
from . import models

import tinymce

class EntryAdmin(admin.ModelAdmin):
    '''
    定制admin 站点管理的内容
    list_display:展示想要的字段
    sear_fields:搜索框
    list_filter: 过滤条件
    '''
    list_display = ['author','img','created_time','visiting']




admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Entry,EntryAdmin)