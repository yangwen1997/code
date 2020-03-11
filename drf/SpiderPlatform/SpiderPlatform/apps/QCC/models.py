#encoding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

# 因为可以分批次查询抓取，不做一对多关系处理

# 企查查基本数据模型信息
class Jbxx(models.Model):
    companyname = models.CharField(db_column='companyName', primary_key=True, max_length=255)  #
    creditcode = models.CharField(db_column='creditCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    organizationcode = models.CharField(db_column='organizationCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registernum = models.CharField(db_column='registerNum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    businessstate = models.CharField(db_column='businessState', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industry = models.CharField(max_length=255, blank=True, null=True)
    legalman = models.CharField(db_column='legalMan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registermoney = models.CharField(db_column='registerMoney', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registertime = models.CharField(db_column='registerTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registorgan = models.CharField(db_column='registOrgan', max_length=255, blank=True, null=True)  # Field name made lowercase.
    confirmtime = models.CharField(db_column='confirmTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    businesstimeout = models.CharField(db_column='businessTimeout', max_length=255, blank=True, null=True)  # Field name made lowercase.
    companytype = models.CharField(db_column='companyType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registeraddress = models.CharField(db_column='registerAddress', max_length=255, blank=True, null=True)  # Field name made lowercase.
    businessscope = models.TextField(db_column='businessScope', blank=True, null=True)  # Field name made lowercase.
    personnelscale = models.CharField(db_column='personnelScale', max_length=255, blank=True, null=True)  # Field name made lowercase.
    insuredpersons = models.CharField(db_column='insuredPersons', max_length=255, blank=True, null=True)  # Field name made lowercase.
    usedname = models.CharField(db_column='usedName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    operation = models.CharField(max_length=255, blank=True, null=True)
    websource = models.CharField(db_column='webSource', max_length=255, blank=True, null=True)  # Field name made lowercase.
    storagetime = models.DateTimeField(db_column='storageTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'jbxx'

# 企查查股东信息数据模型,使用自动更新的时间时需要反向生成一下数据库，不然插入会执行不成功
class ShareHolder(models.Model):
    companyname = models.CharField(db_column='companyName', max_length=255, help_text='公司名',null=True)
    shareholdername = models.CharField(db_column='shareholdername', max_length=255, help_text='股东名称', blank=True, null=True)
    shareholderatio = models.CharField(db_column='shareholdingratio', max_length=255, help_text='持股比例', blank=True, null=True)
    shareholdetype = models.CharField(db_column='shareholdetype', max_length=255, help_text='股东类型', blank=True, null=True)
    subscription = models.CharField(db_column='subscription', max_length=255, help_text='认缴出资额', blank=True, null=True)
    subscriptiondate = models.CharField(db_column='subscriptiondate', max_length=255, help_text='认缴出资日期', blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'shareholder'
