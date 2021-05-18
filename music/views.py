from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    Http404,
    JsonResponse,
)
from django.shortcuts import render
from django.views import generic
from rest_framework.parsers import JSONParser

from music_collection.models import MusicCollection
from .models import MusicTrack, Album

# Create your views here.
from .serializer_w import MusicTrackSerializerW


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "music/import.html"
    context_object_name = "must_list"

    def get_queryset(self):
        return MusicCollection.objects.filter(user=self.request.user)


@login_required
def tracks_uploaded(request):
    return render(request, "")


@login_required
def upload(request):
    if request.method == "POST" and request.content_type == "application/json":
        data = JSONParser().parse(request)
        if isinstance(data, dict):
            music_data = data["tracks"]
            collection = data["collection"]
            if collection == "None":
                collection = None
        else:
            music_data = data
            collection = None

        if collection is not None:
            collection, _ = MusicCollection.objects.get_or_create(
                user_id=request.user.pk, title=collection
            )

        for t in music_data:
            if t is not None:
                t["user"] = request.user.pk
        serializer = MusicTrackSerializerW(data=music_data, many=True)
        if serializer.is_valid():
            tracks = serializer.save()
            if collection is not None:
                for track in tracks:
                    MusicCollection.track_number_manager.add_track_to_collection(
                        track, collection
                    )

            return JsonResponse(data=dict(), status=200)
        else:
            errors = {"errors": serializer.errors}
            return JsonResponse(errors, status=400)
    else:
        raise Http404("Page not found")


class AlbumListView(LoginRequiredMixin, generic.ListView):
    model = Album
    template_name = "music/albums.html"

    def get_queryset(self):
        query_set = Album.user_albums.get(user=self.request.user).order_by("name")
        album_list = [query_set[i : i + 4] for i in range(0, len(query_set), 4)]
        return album_list
