# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    account = models.CharField(unique=True, max_length=5, blank=True)
    name = models.CharField(max_length=8, blank=True)
    passwd = models.CharField(max_length=40, blank=True)
    tel = models.CharField(max_length=11, blank=True)
    mail = models.CharField(max_length=40, blank=True)
    status = models.IntegerField(blank=True, null=True)
    regist_time = models.DateTimeField(blank=True, null=True)
    authorize = models.CharField(max_length=40, blank=True)
    module = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = False
        db_table = 'Account'

class Backup(models.Model):
    id = models.IntegerField(primary_key=True)
    wid = models.ForeignKey('Websites', db_column='wid')
    status = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    filepath = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'Backup'

class Projmain(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    alias = models.CharField(max_length=40, blank=True)
    timestamp = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ProjMain'

class Projsub(models.Model):
    id = models.IntegerField(primary_key=True)
    mid = models.ForeignKey(Projmain, db_column='mid', blank=True, null=True)
    name = models.CharField(max_length=40, blank=True)
    class Meta:
        managed = False
        db_table = 'ProjSub'

class Websites(models.Model):
    id = models.IntegerField(primary_key=True)
    sid = models.ForeignKey(Projsub, db_column='sid')
    name = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=40, blank=True)
    upload = models.CharField(max_length=20, blank=True)
    backup = models.CharField(max_length=20, blank=True)
    release = models.CharField(max_length=40, blank=True)
    type = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=60, blank=True)
    class Meta:
        managed = False
        db_table = 'WebSites'

