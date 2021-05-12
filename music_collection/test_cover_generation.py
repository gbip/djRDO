import json
from io import StringIO

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.parsers import JSONParser

from music.models import MusicTrack
from music.serializer_w import MusicTrackSerializerW
from music.tests import import_tracks_from_test_json
from utils.cover import MusicSetSvgRenderer
from utils.key import openKeyToCamelotKey


class SvgCoverGenerationTest(TestCase):
    def setUp(self):
        self.tracks = []
        self.user = get_user_model().objects.create(
            username="test_user", password="test_password"
        )
        with open("music/test_data/tracks.json", "rb") as file:
            data = JSONParser().parse(file)

        for t in data:
            if t is not None:
                t["user"] = self.user.pk
        serializer = MusicTrackSerializerW(data=data, many=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

    def test_svg_cover_gen(self):
        renderer = MusicSetSvgRenderer(MusicTrack.objects.all())
        svg = renderer.render("Test Collection")
        print(MusicTrack.objects.all())
        xml_io = StringIO()
        xml_io.seek(0)
        svg.write(xml_io)
        xml = xml_io.getvalue().replace("&amp;", "&")
        for track in MusicTrack.objects.all():
            self.assertTrue(track.title in xml)
            if track.artist:
                self.assertTrue(track.artist.name in xml)
            if track.bpm:
                self.assertTrue(str(track.bpm) in xml)
            if track.key:
                self.assertTrue(openKeyToCamelotKey[track.key].value in xml)
