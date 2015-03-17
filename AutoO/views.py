# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator

import hashlib
import datetime, time
import json
import copy, pprint, netsnmp

#from apps.models import Project, Server
from apps.models import *
from common.models import *

def server(request):
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
            quit
        else:
          request.session['query_data']['pid'] = request.POST['pid']
      if 'ip' in request.POST:
        if request.POST['ip'] == "":
          try:
            request.session['query_data'].pop('ip__contains')
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
  def logRecord(r_action='', r_table='', r_data=''):
    record_name = request.session['user_name']
    record_time = time.strftime('%Y-%m-%d %H:%M',time.localtime())
    data_str = ''
    for temp in sorted(r_data):
      data_str += str(temp)+'='+r_data[temp]+' '
    log_op = Logrecord(user=record_name, time=record_time, action=r_action, table=r_table, data=data_str)
    log_op.save()
  
  if 'loginToken' in request.session and request.session['user_admin']:
    if module == 'project':
      if action != '':
        if action == "add" and request.session['user_sys']:
          proj_alias = request.POST['alias_name']
          proj_name = request.POST['name']
          proj_remark = request.POST['remark']
          obj = Project(alias=proj_alias, name=proj_name, remark=proj_remark)
          obj.save()
          logRecord(action, 'project', request.POST)
          result = {}
          result['code'] = 1
          result['message'] = "添加成功"
        elif action == "del":
          pid = request.POST['id']
          if request.session['user_sys'] or pid == request.session['user_proj']:
            Project.objects.get(id=pid).delete()
            logRecord(action, 'project', request.POST)
            result = {}
            result['code'] = 1
            result['message'] = "删除成功"
          else:
            result = {}
            result['code'] = 1
            result['message'] = "无权限删除"
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
        if action == "getinfo":
          if 'ipaddr' in request.POST and request.POST['ipaddr'] != "":
            ipaddr = request.POST['ipaddr']
            data_trans = request.POST['data_trans']
            snmpsession = netsnmp.Session(Version = 2, DestHost = ipaddr, Timeout=50000, ErrorStr='Cannot connect')
            oid_name = netsnmp.Varbind('.1.3.6.1.2.1.1.5.0')  #主机名oid
            bind_name = netsnmp.VarList(oid_name)

            oid_cpu = netsnmp.Varbind('.1.3.6.1.2.1.25.3.3.1.2')  #CPU负载oid
            bind_cpu = netsnmp.VarList(oid_cpu)

            oid_mem = netsnmp.Varbind('.1.3.6.1.2.1.25.2.2.0')  #内存总数oid
            bind_mem = netsnmp.VarList(oid_mem)

            oid_ip = netsnmp.Varbind('.1.3.6.1.2.1.4.20.1.1')  #IP地址oid
            bind_ip = netsnmp.VarList(oid_ip)

            snmp_name = snmpsession.get(bind_name)
            snmp_cpu = snmpsession.walk(bind_cpu)
            snmp_mem = snmpsession.get(bind_mem)
            snmp_ip = snmpsession.walk(bind_ip)

            result_name = snmp_name[0]

            i = 0
            for data in snmp_cpu:
              if data != '':
                i += 1

            result_cpu = i

            result_mem = int(snmp_mem[0])/1024
            if data_trans == "1":
              if result_mem <= 512:
                result_mem = 512
              else:
                result_mem = (result_mem/1024 + 1) * 1024

            result_ip = []
            i = 0
            for data in snmp_ip:
              if data != '127.0.0.1':
                oid = '.1.3.6.1.2.1.4.20.1.2.' + str(data)
                oid_ip_index = netsnmp.Varbind(oid)
                bind_ip_index = netsnmp.VarList(oid_ip_index)
                snmp_ip_index = snmpsession.get(bind_ip_index)
                ip_index = snmp_ip_index[0]
                oid_ip_name = netsnmp.Varbind('.1.3.6.1.2.1.2.2.1.2.' + str(ip_index))
                bind_ip_name = netsnmp.VarList(oid_ip_name)
                snmp_ip_name = snmpsession.get(bind_ip_name)
                ip_name = snmp_ip_name[0]
                result_ip.append(data)

            result = {}
            result['code'] = 0
            result['host'] = result_name
            result['cpu'] = result_cpu
            result['mem'] = result_mem
            result['ip'] = "|".join(result_ip)
            return HttpResponse(json.dumps(result), content_type="application/json")
          else:
            projects = Project.objects.all().order_by('alias')
            rsp = render(request, 'user_index.html', locals())
            return HttpResponse(rsp)
        elif action == "add":
          asset_pid = request.POST['pid']
          asset_ip = request.POST['ip']
          asset_hostname = request.POST['hostname']
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
          if request.session['user_sys'] or asset_pid == request.session['user_proj']:
            obj = Server(pid=pid,
                         ip=asset_ip,
                         hostname=asset_hostname,
                         cpu=asset_cpu,
                         mem=asset_mem,
                         disk=asset_disk,
                         type=asset_type,
                         srv=asset_srv,
                         desc=asset_desc,
                         status='1')
            obj.save()
            logRecord(action, 'asset', request.POST)
            result = {}
            result['code'] = 1
            result['message'] = "添加成功"
          else:
            result = {}
            result['code'] = 0
            result['message'] = "未授权的操作"
        elif action == "del":
          id = request.POST['id']
          del_data = Server.objects.filter(id=id)
          del_id = str(del_data[0].pid.id)
          if request.session['user_sys'] or del_id == request.session['user_proj']:
            try:
              Server.objects.get(id=id).delete()
              logRecord(action, 'asset', request.POST)
              result = {}
              result['code'] = 1
              result['message'] = "删除成功"
            except:
              result = {}
              result['code'] = 0
              result['message'] = "删除异常"
          else:
              result = {}
              result['code'] = 0
              result['message'] = "未授权的操作"
        elif action.isdigit():
          if 'update' in request.GET:
            asset_pid = request.POST['pid']
            asset_ip = request.POST['ip']
            asset_hostname = request.POST['hostname']
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
            if request.session['user_sys'] or asset_pid == request.session['user_proj']:
              try:
                Server.objects.filter(id=action).update(ip=asset_ip,
                  hostname=asset_hostname,
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
                logRecord('update', 'asset', request.POST)
                result = {}
                result['code'] = 1
                result['message'] = "资产修改成功"
              except:
                result = {}
                result['code'] = 0
                result['message'] = "资产修改未提交"
            else:
                result = {}
                result['code'] = 0
                result['message'] = "未授权的操作"
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
                  request.session['query_data'].pop('ip__contains')
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
          if request.session['user_sys']:
            servers = Server.objects.select_related().all()
          else:
            servers = Server.objects.select_related().filter(pid=request.session['user_proj'])
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
        if request.session['user_sys']:
          projects = Project.objects.all().order_by('alias')
        else:
          projects = Project.objects.filter(id=request.session['user_proj']).order_by('alias')
        rsp = render(request, 'admin_servers.html', locals())
        return HttpResponse(rsp)
    else:
      rsp = render(request, 'admin_base.html', locals())
      return HttpResponse(rsp)
  else:
    return HttpResponseRedirect('/')