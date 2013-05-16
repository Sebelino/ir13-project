from django.http import HttpResponse
from django.template import Context, loader
from Search import Search

def index(request):
    s = Search()
    return HttpResponse("Hello, World " + s.search("a")[0])
