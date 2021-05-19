from music.models import MusicTrack, MusicTrackWithNumber
from music_collection.models import MusicCollection, get_next_track_number
from utils.test import DjRDOTestHelper


class TestMusicCollection(DjRDOTestHelper):
    """
    Test that multiple user can't see each other data
    """

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

    def test_reorder_track(self):
        track_1 = MusicTrack.objects.create(title="Track 1", user=self.user)
        track_2 = MusicTrack.objects.create(title="Track 2", user=self.user)
        collection = MusicCollection.objects.create(title="Collection", user=self.user)
        MusicCollection.track_number_manager.add_track_to_collection(
            track_1, collection
        )
        MusicCollection.track_number_manager.add_track_to_collection(
            track_2, collection
        )
        self.assertEqual(
            collection.tracks.get(track_ptr__title=track_1.title).number, 1
        )
        self.assertEqual(
            collection.tracks.get(track_ptr__title=track_2.title).number, 2
        )

        MusicCollection.track_number_manager.change_track_number(1, 2, collection)
        self.assertEqual(
            collection.tracks.get(track_ptr__title=track_1.title).number, 2
        )
        self.assertEqual(
            collection.tracks.get(track_ptr__title=track_2.title).number, 1
        )
