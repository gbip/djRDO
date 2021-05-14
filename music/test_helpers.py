from django.contrib.auth import get_user_model

from music.models import Album, Artist, MusicTrack


def create_user(username, email=None):
    password = "s3crEt"
    return get_user_model().objects.create_user(
        username=username, password=password, email=email
    )


def create_artist(artist_name, user):
    return Artist.objects.get_or_create(name=artist_name, user=user)


def create_album(album_name, user, artist_name=None):
    artist = None
    if artist_name is not None:
        artist, _ = create_artist(artist_name, user)
        return (
            Album.objects.create(name=album_name, artist=artist, user=user),
            artist,
        )
    return Album.objects.create(name=album_name, artist=artist, user=user)


def create_track(title, user, album=None, artist=None):
    return MusicTrack.objects.create(title=title, user=user, album=album, artist=artist)
