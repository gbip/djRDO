from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse, Http404
from django.views import generic

from .models import MusicTrack


class TrackFrom(ModelForm):
    class Meta:
        model = MusicTrack
        fields = [
            "title",
            "artist",
            "album",
            "bpm",
            "key",
            "genre",
            "user",
            "date_released",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_released"].input_format(
            [
                "%Y",  # '2006'
                "%Y-%m-%d",  # '2006-10-25'
                "%m/%d/%Y",  # '10/25/2006'
                "%m/%d/%y",  # '10/25/06'
                "%b %d %Y",  # 'Oct 25 2006'
                "%b %d, %Y",  # 'Oct 25, 2006'
                "%d %b %Y",  # '25 Oct 2006'
                "%d %b, %Y",  # '25 Oct, 2006'
                "%B %d %Y",  # 'October 25 2006'
                "%B %d, %Y",  # 'October 25, 2006'
                "%d %B %Y",  # '25 October 2006'
                "%d %B, %Y",
            ]  # '25 October, 2006'
        )


# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "music_importer/index.html"
    context_object_name = "must_list"

    def get_queryset(self):
        return MusicTrack.objects.get_queryset()[:5]


@login_required
def upload(request):
    if request.method == "POST" and request.content_type == "application/json":
        return HttpResponse("Ok")
    else:
        raise Http404("Page not found")
