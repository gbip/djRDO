from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse

from music_importer.models import MusicTrack
from . import forms


@login_required
def stats(request):
    """
    Display detailed statistics about a user utils collection
    """
    if request.method == "GET":
        user_tracks = MusicTrack.objects.filter(user=request.user)
        bpm_distribution = user_tracks.all().values("bpm").annotate(Count("bpm"))
        key_distribution = user_tracks.all().values("key").annotate(Count("key"))
        context = dict()
        context["bpm_distribution"] = bpm_distribution
        context["key_distribution"] = key_distribution
        return render(request, "accounts/stats.html", context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@login_required
def my_profile(request):
    """
    Display profile detail about a user
    """
    if request.method == "GET":
        context = dict()
        user_tracks = MusicTrack.objects.filter(user=request.user)
        missing_key = user_tracks.filter(key__isnull=True).count()
        missing_bpm = user_tracks.filter(bpm__isnull=True).count()
        context["user"] = request.user
        context["tracks"] = user_tracks.count()
        context["missing_key"] = missing_key
        context["missing_bpm"] = missing_bpm
        return render(request, "accounts/profile.html", context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        context = dict()
        context["message"] = (
            "<strong>"
            + request.user.username
            + "</strong>"
            + " your account and all your data have been deleted successfully."
        )
        return render(request, "display_message.html", context=context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["POST"])


def signup(request):
    """
    Signup view implementation : either register is successful and redirect to the login view, or render the form html.
    """
    if request.method == "POST":
        form = forms.DjRdoUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("accounts:login"))
    else:
        form = forms.DjRdoUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
