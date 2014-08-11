# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import hashlib
import datetime, time
import json

from common.models import Account

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
            local_passwd = hashlib.sha1(user_query[0].passwd + str(request.session['loginTime'])).hexdigest()
          else:
            local_passwd = ""
          if passwd == local_passwd and local_passwd != "":
            result = {}
            result['code'] = 0
            request.session['loginToken'] = "True"
            request.session['user_name'] = user_query[0].name
            if user_query[0].authorize == "1":
              request.session['user_admin'] = "yes"
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
  request.session.clear()
  return HttpResponseRedirect('/')
  
def sys(request, module):
  if 'loginToken' in request.session and request.session['user_admin'] == "yes":
    if module == 'account':
      account_list = Account.objects.all();
      rsp = render(request, 'admin_account.html', locals())
      return HttpResponse(rsp)
    else:
      return HttpResponseRedirect('account')
  else:
    return HttpResponseRedirect('/')

def display_meta(request):
    if'loginToken' in request.session:
      values = request.META.items()
      values.sort()
      html = []
      for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
      return HttpResponse('<table>%s</table>' % '\n'.join(html))
    else:
        return HttpResponseRedirect('/')
