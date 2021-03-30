from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from music import key
from music_importer.models import MusicTrack


class MusicCollectionListView(ListView, LoginRequiredMixin):
    model = MusicTrack
    template_name = "music_collection/music_collection.html"
    paginate_by = 100

    def get_queryset(self):
        order = self.request.GET.get("order_by", "import_date")
        dir = self.request.GET.get("dir", "asc")
        tracks = MusicTrack.objects.filter(user=self.request.user).order_by(order)
        if dir == "desc":
            tracks = tracks.reverse()
        return tracks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_color_map"] = key.openKeyColors
        return context
