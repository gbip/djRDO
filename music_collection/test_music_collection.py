from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from music_collection.models import MusicCollection, get_next_track_number
from music_importer.models import MusicTrack, MusicTrackWithNumber


class TestMusicCollection(TestCase):
    """
    Test that multiple user can't see each other data
    """

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create(
            username="user1", password="test_password", email="toto@toto.com"
        )
        cls.user1.set_password("test_password")
        cls.user1.save()
        cls.user2 = get_user_model().objects.create(
            username="user2", password="test_password", email="toto2@toto.com"
        )
        cls.user2.set_password("test_password")
        cls.user2.save()

    def test_no_data_sharing(self):
        """
        Creates two user, with a single track each. Then tries to fetch the tracklist and make sure each user can only
        see their track
        """
        collection = MusicCollection(title="User1 music", user=self.user1)
        collection.save()

        # Login with user1
        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:collection_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collection.title)

        # Login with client 2
        logged_in = self.client.login(
            username=self.user2.username, password="test_password"
        )
        self.assertTrue(logged_in)
        response = self.client.get(reverse("music_collection:collection_list"))
        # Verify that we can see our music
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, collection.title)

    def test_same_name(self):
        """
        Test the detail view of a music collectio : creates two collection with two distinct set of music and access them.
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
        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )
        self.assertTrue(logged_in)

        def response_is_about(self, response, col_ok, col_nok, music_ok, music_nok):
            """
            Test that the response is about col_ok and music_ok and not about music_nok and col_nok
            """
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, col_ok.title)
            self.assertContains(response, music_ok.title)
            self.assertNotContains(response, col_nok.title)
            self.assertNotContains(response, music_nok.title)

        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection1.pk})
        )
        response_is_about(self, response, collection1, collection2, music1, music2)
        response = self.client.get(
            reverse("music_collection:collection_detail", kwargs={"pk": collection2.pk})
        )

        response_is_about(self, response, collection2, collection1, music2, music1)

    def test_track_number(self):
        """
        Test the track number generation system for one track
        """
        track = MusicTrack(title="toto", user=self.user1)
        track.save()

        collection = MusicCollection(title="toto tracks", user=self.user1)
        collection.save()
        track = MusicCollection.track_number_manager.add_track_to_collection(
            track, collection
        )

        self.assertEqual(track.number, 1)

    def test_multiple_track_number(self):
        """
        Test the track number generation system for 10 tracks
        """
        collection = MusicCollection(title="toto tracks", user=self.user1)
        collection.save()

        for i in range(1, 10):
            track = MusicTrack(title="toto" + str(i), user=self.user1)
            track.save()
            track_n = MusicCollection.track_number_manager.add_track_to_collection(
                track, collection
            )
            self.assertEqual(
                MusicTrackWithNumber.objects.get(
                    track_ptr=track, collection=collection
                ).number,
                i,
            )
            self.assertEqual(track_n.number, i)

        v = MusicTrackWithNumber.objects.get(number=4, collection=collection)
        v.delete()
        track = MusicTrack(title="I should be number 4", user=self.user1)
        track.save()
        track_n = MusicCollection.track_number_manager.add_track_to_collection(
            track, collection
        )
        self.assertEqual(track_n.number, 4)

    def test_get_next_track_number(self):
        """
        Test the track number generator function with a few edge cases
        :return:
        """
        test_vector = [
            ([], 1),
            ([1], 2),
            ([2], 1),
            ([10], 1),
            ([1, 3], 2),
            ([1, 2], 3),
            ([2, 4], 1),
            ([2, 3], 1),
            ([1, 2, 5], 3),
            ([1, 3, 4], 2),
            ([10, 11, 12], 1),
            ([1, 2, 3, 4, 5, 6], 7),
            ([1, 2, 3, 5, 6, 7], 4),
            ([2, 3, 4, 5, 6, 7], 1),
            ([1, 2, 3, 4, 5, 7], 6),
        ]

        for i in range(1, len(test_vector)):
            res = get_next_track_number(test_vector[i][0])
            self.assertEqual(
                res, test_vector[i][1], "test vector " + str(i) + " failed"
            )

    def test_music_collection_basic(self):
        """
        Test the basic behaviour of a music collection
        """
        music = MusicTrack(title="toto", user=self.user1)
        music.save()
        collection = MusicCollection(title="my_col", user=self.user1)
        collection.save()
        track = MusicCollection.track_number_manager.add_track_to_collection(
            music, collection
        )
        self.assertEqual(MusicCollection.objects.all().count(), 1)
        self.assertEqual(track.track_ptr, music)
        self.assertEqual(track.collection, collection)
        self.assertEqual(collection.tracks.get(track_ptr=music).track_ptr, music)

    def test_post_music_collection(self):
        music = MusicTrack(title="toto", user=self.user1)
        music.save()
        collection = MusicCollection(title="my_col", user=self.user1)
        collection.save()

        # Login with user1
        logged_in = self.client.login(
            username=self.user1.username, password="test_password"
        )
        self.assertTrue(logged_in)

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

        self.assertContains(response, "Error")

    def test_delete_music_collection(self):
        self.assertEqual(True, False)  # TODO
