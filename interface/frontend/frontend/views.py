from django.template.loader import get_template
from django.template import Context
from django.http import Http404,HttpResponse
from django.shortcuts import render
import datetime

def hello(request):
    return HttpResponse("<b>Hello wooorld, this is meee...</b>")

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request,'index.html',{'current_date':now})

def searchgui(request):
    now = datetime.datetime.now()
    return render(request,'index.html')

def hours_ahead(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now()+datetime.timedelta(hours=offset)
    html = "<html><body>Om %s timmar aer det %s.</body></html>"% (offset,dt)
    return HttpResponse(html)
