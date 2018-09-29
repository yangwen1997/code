from django.shortcuts import render, get_object_or_404, redirect
from my_blog.models import Entry,Category,Tag
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import Q
from django_comments import models as comment_models
from django_comments.models import Comment
# Create your views here.


# 当我们想要主页的时间默认为第一页 用重定向实现
def index(request):
    return HttpResponseRedirect('/app/1/',)

# 分页
def base(request,number):
    '''
    实现分页功能，获取所有的博客信息 用Paginator(entries,num)把每页展示num条数据
    用paginator.page(number)获取到用户要查看的是那一页的数据传递回模板
    '''
    entries = Entry.objects.all()
    paginator = Paginator(entries,2)
    entrys = paginator.page(number)
    return render(request,'my_blog/index.html',locals())





# 导入markdown富文本编辑器的库和高亮
import markdown,pygments
def detail(request,blog_id):
    # entry = Entry.objects.get(id=blog_id)
    # entry = get_object_or_404(Entry,id=blog_id)
    entry = get_object_or_404(Entry, id=blog_id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    entry.body = md.convert(entry.body)
    entry.toc = md.toc
    entry.increase_visiting()

    comment_list = list()

    def get_comment_list(comments):
        for comment in comments:
            comment_list.append(comment)
            children = comment.child_comment.all()
            if len(children) > 0:
                get_comment_list(children)

    top_comments = Comment.objects.filter(object_pk=blog_id, parent_comment=None,
                                          content_type__app_label='blog').order_by('-submit_date')

    get_comment_list(top_comments)
    return render(request,'my_blog/detail.html',locals())
# 博客详情页的视图函数
def catagory(request,category_id):
    '''
    获取从详情页面传递过来的分类category_id
    获取所有这类的博客信息，把这一类的博客信息给分页，获取用户的页码给它变成第一页
    request.GET.get('number',1)这里的number是用户输入的页码也就是在详情函数传递的形参，1是把
    这个形参变为第一页然后进行展示
    '''
    c = Category.objects.filter(id=category_id)
    entries = Entry.objects.filter(category=c)
    paginator = Paginator(entries,50)
    page = request.GET.get('number',1)
    entrys = paginator.page(page)
    return render(request,'my_blog/index.html',locals())

# 按照标签分类进行展示 方法和分类方法一样
def Tags(request,tags_id):
    t = Tag.objects.get(id=tags_id)
    entries = Entry.objects.filter(tags=t)
    paginator = Paginator(entries, 50)
    page = request.GET.get('number', 1)
    entrys = paginator.page(page)
    return render(request,'my_blog/index.html',locals())


# 搜索内容展示
def search(request):
    '''
    这里主要是使用Q对象 ， 从前段获取到keyword(搜索框的内容)
    在这里使用Q对象进行关键字的模糊查询，使用Q对象需要先导入库
    form djanjo.db.models import Q
    '''
    keyword = request.GET.get('keyword')
    entries = Entry.objects.filter(Q(title__icontains=keyword) |
                              Q(body__icontains=keyword) |
                              Q(abstract__icontains=keyword))
    page = request.GET.get('number',1)
    paginator = Paginator(entries,5)
    entrys = paginator.page(page)
    return render(request,'my_blog/index.html',locals())

# 归档展示
def archives(request,year,month):
    entries = Entry.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(entries,5)
    page = request.GET.get('number',1)
    entrys = paginator.page(page)
    return render(request, 'my_blog/index.html', locals())

# 403页面
def get_403(request):
    return render(request,'my_blog/403.html',locals())

# 404页面
def page_not_found(request):
    return render(request,'my_blog/404.html',locals())

# 500页面
def get_500(request):
    return render(request, 'my_blog/500.html', locals())

def reply(request, comment_id):
    if not request.session.get('login', None) and not request.user.is_authenticated():
        return redirect('/')
    parent_comment = get_object_or_404(comment_models.Comment, id=comment_id)
    return render(request, 'my_blog/reply.html', locals())
