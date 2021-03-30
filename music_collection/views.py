from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed
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
        direction = self.request.GET.get("dir", "asc")
        # Reverse ordering by prepending "-"
        if direction == "desc":
            order = "-" + order
        tracks = MusicTrack.objects.filter(user=self.request.user).order_by(order)
        return tracks


@login_required
def delete_collection(request):
    if request.method == "POST":
        tracks = MusicTrack.objects.filter(user=request.user)
        tracks.delete()
        context = dict()
        context["message"] = (
            "<strong>"
            + request.user.username
            + "</strong>"
            + " all your tracks have been deleted successfully."
        )
        return render(request, "display_message.html", context=context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])
