"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from my_blog.feed import Subscribe
from my_blog import views as blog_view
from django.conf.urls import handler404, handler500,handler403
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from my_blog.models import Entry



'''
站点地图 先导入
from django.contrib.sitemaps import GenericSitemap ：
from django.contrib.sitemaps.views import sitemap 
from my_blog.models import Entry ：这个是需要展示的模型
info_dict : 两个属性  第一个是展示模型的全部数据列表
            第二个属性是这个数据获取的一个时间
            
在路由模式中添加 url(r'^sitemap\.xml$',sitemap,{'sitemaps':{'my_blog':
                                               GenericSitemap(info_dict,priority=0.6)}},
                                                name='django.contrib.sitemaps.views.sitemap'),
       sitemap\.xml     api网络接口 路由   sitemap： 导入的站点地图
       name='django.contrib.sitemaps.views.sitemap' 把站点地图的配置给一个名字传递
        最后是在一个字典中键对应的值有是一个字典在这个字典 
        在这个字典里  my_blog是键 GenericSitemap（）这个函数是值
        里面的第一个属性是我们定义的info_dict，第二个属性priorrity:是给它一个优先级
'''
info_dict = {
    'queryset':Entry.objects.all(),
    'date_field':'modifyed_time',
}

'''
从djanjo.conf导入 settings项目配置文件
django.conf.urls.static导入static 静态资源方法
把上传的图片路由添加到url后面 形成映射关系
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('my_blog.urls',namespace='app')),
    url(r'sub/feed/$',Subscribe()),
    url(r'^sitemap\.xml$',sitemap,{'sitemaps':{'my_blog':
                                               GenericSitemap(info_dict,priority=0.6)}},
                                                name='django.contrib.sitemaps.views.sitemap'),
    url(r'^comments/',include('django_comments.urls')),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
#添加图片路由形成映射关系

# 自定义404页面
handler403 = blog_view.get_403
# handler404 = blog_view.page_not_found
handler404= blog_view.page_not_found
handler500 = blog_view.get_500



