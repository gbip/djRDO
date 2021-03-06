import io

import django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    FileResponse,
    HttpResponse,
)
from django.shortcuts import render
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView

from music.models import MusicTrack, Album, Artist
from music_collection.models import MusicCollection
from utils.http import redirect_to_referer_or


class MusicCollectionListView(LoginRequiredMixin, ListView):
    """
    Provide a list view of all utils collection for a user
    """

    model = MusicCollection
    template_name = "music_collection/music_collection_list.html"
    paginate_by = 100
    ordering = ["date_created"]

    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(user=self.request.user)
            .order_by(*self.ordering)
        )


class MusicCollectionDetailView(LoginRequiredMixin, DetailView):
    model = MusicCollection
    template_name = "music_collection/music_collection_detail.html"

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)


@login_required
def add_music_to_collection(request):
    if request.method == "POST":
        if "col_pk" in request.POST and "music_pk" in request.POST:
            col_pk = request.POST["col_pk"]
            music_pk = request.POST["music_pk"]
            collection = MusicCollection.objects.get(user=request.user, pk=col_pk)
            music = MusicTrack.objects.get(user=request.user, pk=music_pk)
            try:
                MusicCollection.track_number_manager.add_track_to_collection(
                    music, collection
                )
                messages.info(
                    request,
                    '"<b>{}</b>" has been added to collection "<b>{}</b>"'.format(
                        music.title, collection.title
                    ),
                )
                return redirect_to_referer_or(
                    request,
                    HttpResponseRedirect(
                        reverse(
                            "music_collection:collection_detail", kwargs={"pk": col_pk}
                        )
                    ),
                )
            except django.db.utils.IntegrityError:
                messages.error(
                    request,
                    'Can\'t add track to collection :<br>"<b>{}</b>" is already in collection "<b>{}</b>"'.format(
                        music.title, collection.title
                    ),
                )
            return redirect_to_referer_or(
                request,
                HttpResponseRedirect(
                    reverse("music_collection:collection_detail", kwargs={"pk": col_pk})
                ),
            )
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


@login_required
def create_collection(request):
    """
    Create a new collection
    """
    if request.method == "POST":
        if "name" in request.POST:
            name = request.POST["name"]
            MusicCollection.objects.create(title=name, user=request.user)
            return HttpResponseRedirect(reverse("music_collection:collection_list"))
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


class MusicTrackListView(LoginRequiredMixin, ListView):
    """
    Provide a list view of all utils tracks for a user.
    Allows two parameter in the request :
    * order_by : specify a field to order the track
    * dir : specify the ordering order (ascending, descending)
    """

    model = MusicTrack
    template_name = "music_collection/music_track_list.html"
    paginate_by = 100

    def get_queryset(self):
        order = self.request.GET.get("order_by", "import_date")
        direction = self.request.GET.get("dir", "asc")
        # Reverse ordering by prepending "-"
        if direction == "desc":
            order = "-" + order
        tracks = self.model.objects.filter(user=self.request.user).order_by(order)
        return tracks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = MusicCollection.objects.filter(user=self.request.user)
        context["collections"] = collection
        return context


@login_required
def delete_all_user_tracks(request):
    """
    Delete a user track's collection.
    """
    if request.method == "POST":
        tracks = MusicTrack.objects.filter(user=request.user).all()
        tracks.delete()
        albums = Album.objects.filter(user=request.user).all()
        albums.delete()
        artists = Artist.objects.filter(user=request.user).all()
        artists.delete()
        collections = MusicCollection.objects.filter(user=request.user).all()
        collections.delete()
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


@login_required
def remove_track(request):
    if request.method == "POST":
        col_pk = request.POST["col_pk"]
        music_pk = request.POST["music_pk"]
        collection = MusicCollection.objects.get(user=request.user, pk=col_pk)
        music = MusicTrack.objects.get(user=request.user, pk=music_pk)
        collection_link = collection.tracks.get(track_ptr=music)
        collection_link.delete()
        return HttpResponseRedirect(
            reverse("music_collection:collection_detail", kwargs={"pk": collection.pk})
        )
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


@login_required
def get_album_cover(request, pk):
    if request.method == "GET":
        album = Album.objects.get(user=request.user, pk=pk)
        buffer = io.BytesIO()
        svg = album.to_svg()

        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
        )
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@login_required
def get_collection_cover(request, pk):
    if request.method == "GET":
        collection = MusicCollection.objects.get(user=request.user, pk=pk)
        svg = collection.to_svg()
        return HttpResponse(svg.tostring(), content_type="image/svg+xml")
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@login_required
def get_collection_cover_pdf(request, pk):
    if request.method == "GET":
        buffer = io.BytesIO()

        collection = MusicCollection.objects.get(user=request.user, pk=pk)
        svg = collection.to_svg()

        renderPDF.drawToFile(svg, buffer)
        buffer.seek(0)

        return FileResponse(
            buffer, as_attachment=True, filename=collection.title + ".pdf"
        )
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@login_required
def reorder_track(request, col_pk, track_pk, new_number):
    collection = MusicCollection.objects.get(id=col_pk, user=request.user)
    track = collection.tracks.get(track_ptr_id=track_pk)
    # track = MusicTrack.objects.get(id=track_pk, user=request.user)

    if request.method == "POST":
        MusicCollection.track_number_manager.change_track_number(
            track.number, new_number, collection
        )
        return HttpResponseRedirect(
            reverse("music_collection:collection_detail", kwargs={"pk": col_pk})
        )
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])
