# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator

import hashlib
import datetime, time
import json
import copy

from apps.models import Project, Server

def asset(request):
  if 'page' in request.GET and request.GET['page'].isdigit():
    page_get = int(float(request.GET['page']))
  else:
    page_get = 1
  if 'query' in request.GET:
    if request.session['query'].has_key('op'):
      request.session['query'] = {'op':'True'}
      if 'pid' in request.POST:
        if request.POST['pid'] == "":
          try:
            request.session['query_data'].pop('pid')
          except:
            a = 1
        else:
          request.session['query_data']['pid'] = request.POST['pid']
      if 'ip' in request.POST:
        if request.POST['ip'] == "":
          try:
            request.session['query_data'].pop('ip')
          except:
            a = 1
        else:
          request.session['query_data']['ip__contains'] = request.POST['ip']
      if 'srv' in request.POST:
        if request.POST['srv'] == "":
          try:
            request.session['query_data'].pop('srv')
          except:
            a = 1
        else:
          request.session['query_data']['srv'] = request.POST['srv']
      if 'status' in request.POST:
        if request.POST['status'] == "":
          try:
            request.session['query_data'].pop('status')
          except:
            a = 1
        else:
          request.session['query_data']['status'] = request.POST['status']
      exper = request.session['query_data']
    else:
      request.session['query'] = {'op':'true'}          
      if 'pid' in request.POST and request.POST['pid'] != "":
        request.session['query_data']['pid'] = request.POST['pid']
      if 'ip' in request.POST and request.POST['ip'] != "":
        request.session['query_data']['ip__contains'] = request.POST['ip']
      if 'srv' in request.POST and request.POST['srv'] != "":
        request.session['query_data']['srv'] = request.POST['srv']
      if 'status' in request.POST and request.POST['status'] != "":
        request.session['query_data']['status'] = request.POST['status']
      exper = request.session['query_data']
    
    servers = Server.objects.filter(**exper)
  else:
    request.session['query'] = {}
    request.session['query_data'] = {}
    servers = Server.objects.select_related().all()
  pagin = Paginator(servers,20)
  page_max = pagin.num_pages
  if page_get > page_max:
    page = page_max
  else:
    page = page_get
  data_list = pagin.page(page)
  if 'query' in request.GET:
    url_fp = "?query&page=1"
    if page <= 1:
      url_pp = "?query&page=1"
    else:
      url_pp = "?query&page=" + str((page - 1))
    if page >= page_max:
      url_np = "?query&page=" + str(page_max)
    else:
      url_np = "?query&page=" + str((page + 1))
    url_lp = "?query&page=" + str(page_max)
  else:
    url_fp = "?page=1"
    if page <= 1:
      url_pp = "?page=1"
    else:
      url_pp = "?page=" + str((page - 1))
    if page >= page_max:
      url_np = "?page=" + str(page_max)
    else:
      url_np = "?page=" + str((page + 1))
    url_lp = "?page=" + str(page_max)
  projects = Project.objects.all()
  rsp = render(request, 'user_assets.html', locals())
  return HttpResponse(rsp)

def admin(request, module="", action=""):
  if 'loginToken' in request.session and request.session['user_admin'] == "yes":
    if module == 'project':
      if action != '':
        if action == "add":
          proj_alias = request.POST['alias_name']
          proj_name = request.POST['name']
          proj_remark = request.POST['remark']
          obj = Project(alias=proj_alias, name=proj_name, remark=proj_remark)
          obj.save()
          result = {}
          result['code'] = 1
          result['message'] = "添加成功"
        elif action == "del":
          pid = request.POST['id']
          Project.objects.get(id=pid).delete()
          result = {}
          result['code'] = 1
          result['message'] = "删除成功"
        elif action.isdigit():
          return HttpResponse(action)
        else:         
          result = {}
          result['code'] = 0
          result['message'] = "操作失败"
        return HttpResponse(json.dumps(result), content_type="application/json")
      else:
        projects = Project.objects.all().order_by('alias')
        rsp = render(request, 'admin_project.html', locals())
        return HttpResponse(rsp)
    elif module == 'servers':
      if action != '':
        if action == "add":
          asset_pid = request.POST['pid']
          asset_ip = request.POST['ip']
          asset_cpu = request.POST['cpu']
          asset_mem = request.POST['mem']
          asset_disk = request.POST['disk']
          if request.POST['type'] == '1':
            asset_type = "物理机"
          elif request.POST['type'] == '2':
            asset_type = "虚拟机"
          else:
            asset_type = "其他" 
          asset_srv = request.POST['srv']
          asset_desc = request.POST['desc']
          pid = Project.objects.get(id=asset_pid)
          obj = Server(pid=pid,
                       ip=asset_ip,
                       cpu=asset_cpu,
                       mem=asset_mem,
                       disk=asset_disk,
                       type=asset_type,
                       srv=asset_srv,
                       desc=asset_desc,
                       status='1')
          obj.save()
          result = {}
          result['code'] = 1
          result['message'] = "添加成功"
        elif action == "del":
          id = request.POST['id']
          try:
            Server.objects.get(id=id).delete()
            result = {}
            result['code'] = 1
            result['message'] = "删除成功"
          except:
            result = {}
            result['code'] = 0
            result['message'] = "删除异常"
        elif action.isdigit():
          if 'update' in request.GET:
            asset_pid = request.POST['pid']
            asset_ip = request.POST['ip']
            asset_cpu = request.POST['cpu']
            asset_mem = request.POST['mem']
            asset_disk = request.POST['disk']
            if request.POST['type'] == '1':
              asset_type = "物理机"
            elif request.POST['type'] == '2':
              asset_type = "虚拟机"
            else:
              asset_type = "其他" 
            asset_srv = request.POST['srv']
            asset_desc = request.POST['desc']
            asset_status = request.POST['status']
            asset_cacti = request.POST['cacti']
            asset_nagios = request.POST['nagios']
            try:
              Server.objects.filter(id=action).update(ip=asset_ip,
                cpu=asset_cpu,
                mem=asset_mem,
                disk=asset_disk,
                type=asset_type,
                srv=asset_srv,
                desc=asset_desc,
                status = asset_status,
                cacti = asset_cacti,
                nagios = asset_nagios
              )
              result = {}
              result['code'] = 1
              result['message'] = "资产修改成功"
            except:
              result = {}
              result['code'] = 0
              result['message'] = "资产修改未提交"
            return HttpResponse(json.dumps(result), content_type="application/json")
          else:
            try:
              queryset = Server.objects.select_related().get(id=action)
            except:
              return HttpResponse('无效ID')
            rsp = render(request, 'admin_display_server.html', locals())
            return HttpResponse(rsp)
        else:
          result = {}
          result['code'] = 0
          result['message'] = "操作失败"
        return HttpResponse(json.dumps(result), content_type="application/json")
      else:
        if 'page' in request.GET and request.GET['page'].isdigit():
          page_get = int(float(request.GET['page']))
        else:
          page_get = 1
        if 'query' in request.GET:
          if request.session['query'].has_key('op'):
            request.session['query'] = {'op':'True'}
            if 'pid' in request.POST:
              if request.POST['pid'] == "":
                try:
                  request.session['query_data'].pop('pid')
                except:
                  a = 1
              else:
                request.session['query_data']['pid'] = request.POST['pid']
            if 'ip' in request.POST:
              if request.POST['ip'] == "":
                try:
                  request.session['query_data'].pop('ip')
                except:
                  a = 1
              else:
                request.session['query_data']['ip__contains'] = request.POST['ip']
            if 'srv' in request.POST:
              if request.POST['srv'] == "":
                try:
                  request.session['query_data'].pop('srv')
                except:
                  a = 1
              else:
                request.session['query_data']['srv'] = request.POST['srv']
            if 'status' in request.POST:
              if request.POST['status'] == "":
                try:
                  request.session['query_data'].pop('status')
                except:
                  a = 1
              else:
                request.session['query_data']['status'] = request.POST['status']
            exper = request.session['query_data']
          else:
            request.session['query'] = {'op':'true'}          
            if 'pid' in request.POST and request.POST['pid'] != "":
              request.session['query_data']['pid'] = request.POST['pid']
            if 'ip' in request.POST and request.POST['ip'] != "":
              request.session['query_data']['ip__contains'] = request.POST['ip']
            if 'srv' in request.POST and request.POST['srv'] != "":
              request.session['query_data']['srv'] = request.POST['srv']
            if 'status' in request.POST and request.POST['status'] != "":
              request.session['query_data']['status'] = request.POST['status']
            exper = request.session['query_data']
          
          servers = Server.objects.filter(**exper)
        else:
          request.session['query'] = {}
          request.session['query_data'] = {}
          servers = Server.objects.select_related().all()
        pagin = Paginator(servers,20)
        page_max = pagin.num_pages
        if page_get > page_max:
          page = page_max
        else:
          page = page_get
        data_list = pagin.page(page)
        if 'query' in request.GET:
          url_fp = "?query&page=1"
          if page <= 1:
            url_pp = "?query&page=1"
          else:
            url_pp = "?query&page=" + str((page - 1))
          if page >= page_max:
            url_np = "?query&page=" + str(page_max)
          else:
            url_np = "?query&page=" + str((page + 1))
          url_lp = "?query&page=" + str(page_max)
        else:
          url_fp = "?page=1"
          if page <= 1:
            url_pp = "?page=1"
          else:
            url_pp = "?page=" + str((page - 1))
          if page >= page_max:
            url_np = "?page=" + str(page_max)
          else:
            url_np = "?page=" + str((page + 1))
          url_lp = "?page=" + str(page_max)
        projects = Project.objects.all().order_by('alias')
        rsp = render(request, 'admin_servers.html', locals())
        return HttpResponse(rsp)
    else:
      rsp = render(request, 'admin_base.html', locals())
      return HttpResponse(rsp)
  else:
    return HttpResponseRedirect('/')