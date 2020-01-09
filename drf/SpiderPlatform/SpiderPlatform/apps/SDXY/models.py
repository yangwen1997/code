from django.db import models

# Create your models here.

class Jbxx(models.Model):
    companyname = models.CharField(db_column='companyName', primary_key=True, max_length=255)  # Field name made lowercase.
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
        app_label = 'sdxydb'
