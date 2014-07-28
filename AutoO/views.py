from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import hashlib
import datetime, time
import json

from assets.models import Account

def USER_LOGIN(request):
    if 'loginToken' in request.session:
        t = render_to_response('index.html',{'name': request.session['user_name']})
        return HttpResponse(t)
    else:
        if 'a' in request.GET and request.GET['a'] == "login":
          user = request.POST['username']
          passwd = request.POST['password']
          user_query = Account.objects.filter(account = user)
          local_passwd = hashlib.sha1(user_query[0].passwd + str(request.session['loginTime'])).hexdigest()
          if passwd == local_passwd:
            result = {}
            result['code'] = 0
            request.session['loginToken'] = "123456"
            request.session['user_name'] = user_query[0].name
          else:
            result = {}
            result['code'] = -1
            result['message'] = "Error: Username or Password"
          return HttpResponse(json.dumps(result), content_type="application/json")
          #return HttpResponse(local_passwd)
        else:
          timestamp = time.time()
          request.session['loginTime'] = timestamp

          t = render_to_response('login.html',
                                 {'time': request.session['loginTime'],
                                  })
          return HttpResponse(t)

def USER_LOGOUT(request):
    request.session.clear()
    return HttpResponseRedirect('/')

def add_hours(request,offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def display_meta(request):

    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
