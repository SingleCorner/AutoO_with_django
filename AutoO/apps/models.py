# -*- coding: utf-8 -*-
# coding:utf8
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
      
class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    alias = models.CharField(unique=True, max_length=14, blank=True)
    name = models.CharField(max_length=14, blank=True)
    remark = models.CharField(max_length=14, blank=True)
    class Meta:
        managed = False
        db_table = 'project'

class Server(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Project, db_column='pid', blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True)
    ip_2 = models.CharField(max_length=15, blank=True)
    cpu = models.CharField(max_length=4)
    mem = models.CharField(max_length=4)
    disk = models.CharField(max_length=4)
    raid = models.CharField(max_length=2, blank=True)
    type = models.CharField(max_length=10, blank=True)
    srv = models.CharField(max_length=6, blank=True)
    desc = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(blank=True, null=True)
    cacti = models.CharField(max_length=4, blank=True)
    nagios = models.CharField(max_length=4, blank=True)
    class Meta:
        managed = False
        db_table = 'server'