from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# 创建分类的数据模型
class Category(models.Model):
    '''
    字段里面的第一个属性‘分类’：是在admin站点管理
    中做修改的不改的话是英文不方便用户体验
    verbose_name :把这个类名修改方便在admin中管理
    verbose_name_plural: 这个是复数 不写后面要加s
    '''
    name = models.CharField('分类',max_length=128)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

# 创建标签的数据模型
class Tag(models.Model):
    name = models.CharField('标签',max_length=128)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

# 创建博客模型
class Entry(models.Model):
    '''
    title:标题模型 author 关联用户的外键模型 img 图片模型
    body 内容模型 abstract 摘要  visiting 访问量 category 类别
    created_time 创建时间模型 modifyed_time 修改时间模型
    '''
    '''
    这里的author属性是在用户创建的外键，但是这个用户
    模型django帮我们设置好了已经，数据库auth_user表就是使用之前需要先
    导入from django.contrib.auth.models import User这个包，在这里
    verbose_name:修改的是author这个字段在admin站点管理中
    ondelete=models.CASCADE:是一种级联操作 删除主表会同时把从表数据删除
    null=True 是否可以不设置缺省参数（默认值） 
    blank=True 字段是否可以为空
    PositiveIntegerField 非负的正整数
    auto_now无论是你添加还是修改对象（数据模型），都会更新时间。
    auto_now_add创建对象（数据模型）时自动生成一个创建的时间，更新对象时不会有变动
    '''
    title = models.CharField('文章标题',max_length=128)
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog_img',null=True,blank=True,verbose_name='博客配图')
    body = models.TextField('正文',)
    abstract = models.TextField('摘要',max_length=256,null=True,blank=True)
    visiting = models.PositiveIntegerField('访问量',default=0)
    category = models.ManyToManyField('Category',verbose_name='博客分类')
    tags = models.ManyToManyField('Tag',verbose_name='标签')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    modifyed_time = models.DateTimeField('修改时间',auto_now=True)
    def __str__(self):
        return self.title
    '''
    当点击博客详情页的时候获取博客的id并把参数传递
    跳转到博客详情的函数展示博客的详情页面
    '''
    def get_absolute_url(self):
        return reverse("app:blog_detail",kwargs={"blog_id":self.id})
   # '''
   # 每当有人访问把访问量加等于1 再保存更新以后的访问量
   # '''

    def increase_visiting(self):
        self.visiting += 1
        self.save(update_fields=['visiting'])
    class Meta:
        ordering = ['-created_time']
        verbose_name = '博客正文'
        verbose_name_plural = verbose_name

