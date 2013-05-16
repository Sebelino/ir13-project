from django.http import HttpResponse
from django.template import Context, loader
from Search import Search
import GlobalConfiguration


def index(request):
    s = Search(GlobalConfiguration.DEFAULT_SOLR_URL)

    return HttpResponse("Hello, World " + s.search("a")[0])
