from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime

def USER_LOGIN(request):
    if 'a' in request.GET and 'username' in request.POST:
        t = request.POST['username']
        return HttpResponse(t)
    else:
        t = render_to_response('login.html')
        return HttpResponse(t)

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
