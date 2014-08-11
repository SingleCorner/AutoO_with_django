# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import hashlib
import datetime, time
import json

from apps.models import Project

def admin(request, module, action):
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
        else:         
          result = {}
          result['code'] = 0
          result['message'] = "操作失败"
        return HttpResponse(json.dumps(result), content_type="application/json")
      else:
        projects = Project.objects.all()
        rsp = render(request, 'admin_project.html', locals())
        return HttpResponse(rsp)
    elif module == 'proj':
      rsp = render(request, 'admin_project.html', locals())
      return HttpResponse(rsp)
    else:
      rsp = render(request, 'admin_base.html', locals())
      return HttpResponse(rsp)
  else:
    return HttpResponseRedirect('/')