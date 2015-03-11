# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import *

import hashlib, random, string, re
import datetime, time
import json, netsnmp

from common.models import Account, Logrecord
from AutoO.apps.models import Project

def USER_LOGIN(request):
    if 'loginToken' in request.session:
      rsp = render(request, 'user_index.html', locals())
      return HttpResponse(rsp)
    else:
        if 'a' in request.GET and request.GET['a'] == "login":
          user = request.POST['username']
          passwd = request.POST['password']
          user_query = Account.objects.filter(account = user, status = 1)
          if user_query:
            local_passwd = user_query[0].secpasswd
          else:
            local_passwd = ""
          if check_password(passwd,local_passwd):
            result = {}
            result['code'] = 0
            request.session['loginToken'] = "True"
            request.session['logoutAuth'] = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 4)).replace(' ','').upper()
            request.session['user_id'] = user_query[0].id
            request.session['user_name'] = user_query[0].name
            #判断后台进入权限
            if user_query[0].authorize == "1":
              request.session['user_admin'] = True
            else:
              request.session['user_admin'] = False
            #判断项目权限
            if user_query[0].module == "-1":
              request.session['user_sys'] = True
            else:
              request.session['user_sys'] = False
              request.session['user_proj'] = user_query[0].module
          else:
            result = {}
            result['code'] = -1
            result['message'] = "用户验证出错，请联系管理员"
          return HttpResponse(json.dumps(result), content_type="application/json")
          #return HttpResponse(local_passwd)
        else:
          timestamp = time.time()
          request.session['loginTime'] = timestamp

          rsp = render(request, 'login.html', locals())
          return HttpResponse(rsp)

def USER_LOGOUT(request):
  if 'key' in request.GET and request.GET['key'] == request.session['logoutAuth']:
    request.session.clear()
  return HttpResponseRedirect('/')

def USER_CHGPASS(request):
  user_id = request.session['user_id']
  if 'passwd' in request.POST:
    passwd = request.POST['passwd']
  else:
    passwd = ''
    
  if 'passwd_cfm' in request.POST:
    passwd_c = request.POST['passwd_cfm']
  else:
    passwd_c = 'wrong'
    
  if passwd == passwd_c:
    passwd_sec = make_password(passwd, None, 'pbkdf2_sha256')
    try:
      Account.objects.filter(id=user_id).update(secpasswd=passwd_sec)
      passinfo = "密码修改成功"
    except:
      passinfo = "密码修改失败"    
  rsp = render(request, 'user_chgpass.html', locals())
  return HttpResponse(rsp)
  
def sys(request, module, action=""):
  if 'loginToken' in request.session and request.session['user_sys']:
    if module == 'account':
      if action == "add":
        account = request.POST['account']
        name = request.POST['name']
        passwd = make_password(request.POST['passwd'], None, 'pbkdf2_sha256')
        mgr = request.POST['mgr']
        project = request.POST['project']
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        try:
          obj = Account(account=account,
                        name=name,
                        secpasswd=passwd,
                        status=1,
                        regist_time=date,
                        authorize=mgr,
                        module=project)
          obj.save()
          result = {}
          result['code'] = 1
          result['message'] = date
        except:
          result = {}
          result['code'] = 0
          result['message'] = "添加失败"
        return HttpResponse(json.dumps(result), content_type="application/json")
      else:
        if 'ctrl' in request.POST:
          ctrl = request.POST['ctrl']
          accnt_id = request.POST['id']
          accnt = Account.objects.get(id=accnt_id)
          if ctrl == "status":
            accnt_status = accnt.status
            if accnt_status == 1:
              Account.objects.filter(id=accnt_id).update(status=0)
            else:
              Account.objects.filter(id=accnt_id).update(status=1)
            result = {}
            result['code'] = 1
            result['message'] = "状态变更成功"
          elif ctrl == "admin":
            accnt_admin = accnt.authorize
            if accnt_admin == '1':
              Account.objects.filter(id=accnt_id).update(authorize='0')
            else:
              Account.objects.filter(id=accnt_id).update(authorize='1')
            result = {}
            result['code'] = 1
            result['message'] = "后台权限变成成功"
          else:
            result = {}
            result['code'] = 0
            result['message'] = "无操作"
          return HttpResponse(json.dumps(result), content_type="application/json")
        else:
          project_list = Project.objects.all()
          account_list = Account.objects.all()
          rsp = render(request, 'admin_account.html', locals())
          return HttpResponse(rsp)
    elif module == 'log':
      log_list = Logrecord.objects.all();
      rsp = render(request, 'admin_log.html', locals())
      return HttpResponse(rsp)
    else:
      return HttpResponseRedirect('account')
  else:
    return HttpResponseRedirect('/')
