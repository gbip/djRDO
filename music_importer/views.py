from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token

from .models import Music


# Create your views here.

class IndexView(generic.ListView):
    template_name = "music_importer/index.html"
    context_object_name = "must_list"

    def get_queryset(self):
        return Music.objects.get_queryset()[:5]


def upload(request):
    print("ALO")
    if request.method == 'POST' and request.content_type == 'application/json':
        print(request.body)
        return HttpResponse("Ok")
    else:
        raise Http404("Page not found")
