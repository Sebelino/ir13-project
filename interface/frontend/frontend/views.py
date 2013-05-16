from django.template.loader import get_template
from django.template import Context
from django.http import Http404,HttpResponse
import datetime

def hello(request):
    return HttpResponse("<b>Hello wooorld, this is meee...</b>")

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('interface.html')
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

def hours_ahead(request,offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now()+datetime.timedelta(hours=offset)
    html = "<html><body>Om %s timmar aer det %s.</body></html>"% (offset,dt)
    return HttpResponse(html)
