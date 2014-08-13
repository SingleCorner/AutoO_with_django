# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import hashlib
import datetime, time
import json

from apps.models import Project, Server

def asset(request):
  servers = Server.objects.select_related().all()
  rsp = render(request, 'user_assets.html', locals())
  return HttpResponse(rsp)

def admin(request, module="", action=""):
  if 'loginToken' in request.session and request.session['user_admin'] == "yes":
    if module == 'project':
      if action != '':
        if action == "add":
          proj_name = request.POST['name']
          proj_remark = request.POST['remark']
          obj = Project(name=proj_name, remark=proj_remark)
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
        projects = Project.objects.all()
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
        projects = Project.objects.all()
        servers = Server.objects.select_related().all()
        rsp = render(request, 'admin_servers.html', locals())
        return HttpResponse(rsp)
    else:
      rsp = render(request, 'admin_base.html', locals())
      return HttpResponse(rsp)
  else:
    return HttpResponseRedirect('/')