from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Music


# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "music_importer/index.html"
    context_object_name = "must_list"

    def get_queryset(self):
        return Music.objects.get_queryset()[:5]


@login_required
def upload(request):
    print("ALO")
    if request.method == 'POST' and request.content_type == 'application/json':
        return HttpResponse("Ok")
    else:
        raise Http404("Page not found")
