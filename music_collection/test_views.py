# Create your tests here.

from datetime import timedelta

# Create your tests here.
from django.urls import reverse
from django.utils.datetime_safe import datetime

from music_collection.models import MusicCollection
from music_importer.models import MusicTrack, Artist, Album
from utils import key
from utils.test import DjRDOTestHelper


class TestMusicCollectionViews(DjRDOTestHelper):
    def test_add_music_to_collection(self):
        """
        Test music collection view
        :return:
        """
        music = MusicTrack(title="toto", user=self.user)
        music.save()
        collection = MusicCollection(title="my_col", user=self.user)
        collection.save()

        self.login("user")

        response = self.client.post(
            reverse("music_collection:add_music_to_collection"),
            {"col_pk": collection.pk, "music_pk": music.pk},
        )

        self.assertRedirects(
            response,
            reverse("music_collection:collection_detail", kwargs={"pk": collection.pk}),
        )
        self.assertEqual(music.collection.collection.pk, collection.pk)

        response = self.client.post(
            reverse("music_collection:add_music_to_collection"),
            {"col_pk": collection.pk, "music_pk": music.pk},
        )

# FIXME
#        self.assertRedirects(response, reverse("music_collection:collection_detail", kwargs={"pk": collection.pk}))

    def test_delete_track_from_collection(self):
        music = MusicTrack(title="toto", user=self.user)
        music.save()
        collection = MusicCollection(title="my_col", user=self.user)
        collection.save()
        track_number = MusicCollection.track_number_manager.add_track_to_collection(
            music, collection
        )
        track_number.save()

        # Login with user
        self.login("user")

        response = self.client.post(
            reverse("music_collection:collection_remove_track"),
            {"col_pk": collection.pk, "music_pk": music.pk},
        )

        self.assertRedirects(
            response,
            reverse("music_collection:collection_detail", kwargs={"pk": collection.pk}),
        )

        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection.pk})
        )

        self.assertNotContains(response, music.title)

        def test_no_data_sharing(self):
            """
            Creates two user, with a single track each. Then tries to fetch the tracklist and make sure each user can only
            see their track
            """
            collection = MusicCollection(title="User1 music", user=self.user1)
            collection.save()

            # Login with user1
            self.login("user1")
            response = self.client.get(reverse("music_collection:collection_list"))
            # Verify that we can see our music
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, collection.title)

            # Login with client 2
            self.login("user2")
            response = self.client.get(reverse("music_collection:collection_list"))
            # Verify that we can see our music
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, collection.title)

    def test_same_name(self):
        """
        Test the detail view of a music collection : creates two collection with two distinct set of music and access them.
        """
        collection1 = MusicCollection(title="col1", user=self.user1)
        music1 = MusicTrack(title="music1", user=self.user1)
        music1.save()
        collection1.save()
        res = MusicCollection.track_number_manager.add_track_to_collection(
            music1, collection1
        )

        self.assertEqual(collection1.tracks.count(), 1)
        self.assertEqual(collection1.tracks.all()[0].track_ptr, music1)

        collection2 = MusicCollection(title="col2", user=self.user1)
        music2 = MusicTrack(title="music2", user=self.user1)
        music2.save()
        collection2.save()
        _ = MusicCollection.track_number_manager.add_track_to_collection(
            music2, collection2
        )
        self.assertEqual(collection2.tracks.count(), 1)
        self.assertEqual(collection2.tracks.all()[0].track_ptr, music2)
        self.login("user1")

        def response_is_about(
            self, server_response, col_ok, col_nok, music_ok, music_nok
        ):
            """
            Test that the response contains col_ok and music_ok and not music_nok and col_nok
            """
            self.assertEqual(server_response.status_code, 200)
            self.assertContains(server_response, col_ok.title)
            self.assertContains(server_response, music_ok.title)
            self.assertNotContains(server_response, col_nok.title)
            self.assertNotContains(server_response, music_nok.title)

        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection1.pk})
        )
        response_is_about(self, response, collection1, collection2, music1, music2)
        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection2.pk})
        )

        response_is_about(self, response, collection2, collection1, music2, music1)


class TestOrdering(DjRDOTestHelper):
    """
    Test the ordering of tracks on the music collection view
    """

    def ordering_test_helper(self, track_first, track_second, field_name):
        """
        Helper that allows to quickly check the ordering of tracks. The music collection list is fetched twice, one time
        ordered in an ascending order, one time in a descending order. The order in which the track are returned is then
        verified.
        :param track_first: The first track
        :param track_second: The second track
        :param field_name: The field to sort the track with
        """
        response = self.client.get(
            reverse("music_collection:music_list")
            + "?order_by="
            + field_name
            + "&dir=asc"
        )
        self.assertEqual(response.context["object_list"][0].pk, track_first.pk)
        self.assertEqual(response.context["object_list"][1].pk, track_second.pk)

        response = self.client.get(
            reverse("music_collection:music_list")
            + "?order_by="
            + field_name
            + "&dir=desc"
        )

        self.assertEqual(response.context["object_list"][1].pk, track_first.pk)
        self.assertEqual(response.context["object_list"][0].pk, track_second.pk)

    def test_ordering(self):
        self.login("user")
        artist_first = Artist(name="A", user=self.user)
        artist_first.save()
        album_first = Album(name="A", artist=artist_first, user=self.user)
        album_first.save()
        track_first = MusicTrack(
            title="First",
            album=album_first,
            artist=artist_first,
            bpm=50,
            date_released=datetime.today() - timedelta(1),
            key=key.OpenKey.M1,
            user=self.user,
        )
        track_first.save()

        artist_second = Artist(name="B", user=self.user)
        artist_second.save()
        album_second = Album(name="B", artist=artist_second, user=self.user)
        album_second.save()

        track_second = MusicTrack(
            title="Second",
            album=album_second,
            artist=artist_second,
            bpm=51,
            date_released=datetime.now(),
            key=key.OpenKey.M2,
            user=self.user,
        )
        track_second.save()

        self.ordering_test_helper(track_first, track_second, "title")
        self.ordering_test_helper(track_first, track_second, "album")
        self.ordering_test_helper(track_first, track_second, "artist")
        self.ordering_test_helper(track_first, track_second, "bpm")
        self.ordering_test_helper(track_first, track_second, "key")
        self.ordering_test_helper(track_first, track_second, "import_date")
        self.ordering_test_helper(track_first, track_second, "date_released")


class TestMultipleUserMusic(DjRDOTestHelper):
    """
    Test that multiple user can't see each other data
    """

    def test_no_data_sharing(self):
        """
        Creates two user, with a single track each. Then tries to fetch the tracklist and make sure each user can only
        see their track
        """
        music = MusicTrack(
            title="User1 music", date_released=datetime.today(), user=self.user1
        )
        music.save()

        # Login with user1
        self.login("user1")
        response = self.client.get(reverse("music_collection:music_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, music.title)
        self.assertContains(response, music.date_released.year)

        # Login with client 2
        self.login("user2")
        response = self.client.get(reverse("music_collection:music_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, music.title)
        self.assertNotContains(response, music.date_released)
