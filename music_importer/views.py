from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    Http404,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from rest_framework.parsers import JSONParser

from .models import MusicTrack

# Create your views here.
from .serializer_w import MusicTrackSerializerW


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "music_importer/import.html"
    context_object_name = "must_list"

    def get_queryset(self):
        return MusicTrack.objects.get_queryset()[:5]


@login_required
def tracks_uploaded(request):
    return render(request, "")


@login_required
def upload(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = JSONParser().parse(request)
        for t in data:
            if t is not None:
                t["user"] = request.user.pk
        serializer = MusicTrackSerializerW(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=dict(), status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        raise Http404("Page not found")
