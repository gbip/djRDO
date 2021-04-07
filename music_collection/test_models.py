from django.contrib.auth import get_user_model
from django.test import TestCase

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
        Test the basic behaviour of a utils collection
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