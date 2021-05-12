import svgwrite
from django.db.models import Max
from django.db.models.functions import Length

from utils import key
from abc import ABC, abstractmethod


class MusicSetRenderer(ABC):
    """
    This class provide the default behaviour of a renderer that converts MusicTrack sets to some picture
    formats (png, pdf, svg, etc.).
    When deriving this class, you need to implement the following methods to provide a way for the renderer
    to draw the data :
        * _init_renderer is a convenient method that is supposed to hold your initialization code
        * _title_render is tasked with rendering a title
        * _pre_track_render is a method that is called after rendering the title, but before rendering the tracks
        * _track_render is called for each track, with it's index and the track data
        * _get_result is called to fetch the output of this process
    """

    @abstractmethod
    def _init_renderer(self):
        pass

    @abstractmethod
    def _title_render(self, title):
        pass

    @abstractmethod
    def _pre_track_render(self):
        pass

    @abstractmethod
    def _track_render(self, track, index):
        pass

    @abstractmethod
    def _get_result(self):
        """
        :return: A representation of the tracks data
        """
        pass

    def render(self, title):
        """
        Render a cover from a MusicTrack set and a title.

        :param title: The cover title
        :return: The reprensetation of the track data
        """
        self._init_renderer()
        self._title_render(title)
        self._pre_track_render()
        for (i, track) in enumerate(self.music_set):
            self._track_render(track, i)
        return self._get_result()

    def _compute_canvas_width(self, music_set):
        self.max_title_length = music_set.aggregate(title_len=Max(Length("title")))[
            "title_len"
        ]
        self.max_artist_name_length = music_set.aggregate(
            artist_len=Max(Length("artist__name"))
        )["artist_len"]
        self.max_bpm_length = len(
            str(music_set.aggregate(bpm_len=Max("bpm"))["bpm_len"])
        )
        width = (
            (
                (self.max_title_length or 0)
                + (self.max_artist_name_length or 0)
                + (self.max_bpm_length or 0)
            )
            * self.font_size
        ) + 100
        return width

    def __init__(self, music_set, font_size=16):
        self.font_size = font_size
        self.music_set = music_set
        self.width = self._compute_canvas_width(music_set)
        self.height = font_size * (len(music_set) + 3)


class MusicSetSvgRenderer(MusicSetRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _init_renderer(self):
        self.dwg = svgwrite.Drawing("Cover", (self.width, self.height))
        self.width = self.width
        self.height = self.height

    def _title_render(self, title):
        title_width = (self.width / 2) - (len(title) * self.font_size) / 2
        self.dwg.add(
            self.dwg.text(
                title,
                (title_width, self.font_size),
                style="font-weight:bold;text-decoration:underline",
            )
        )

    def _pre_track_render(self):
        self._tracks_container = self.dwg.add(self.dwg.g(font_size=self.font_size))

    def _track_render(self, track, index):
        line_index = (
            index + 3
        )  # Offset between the line number, and the item index in the query set
        track_str = str(index + 1) + " - " + track.title
        # Track title
        self._tracks_container.add(
            self.dwg.text(track_str, (0, line_index * self.font_size), fill="black")
        )

        if track.artist:
            # Track artist
            self._tracks_container.add(
                self.dwg.text(
                    track.artist.name,
                    (
                        self.max_title_length * self.font_size,
                        line_index * self.font_size,
                    ),
                )
            )
        if track.bpm:
            # Track BPM
            self._tracks_container.add(
                self.dwg.text(
                    track.bpm,
                    (
                        (self.max_artist_name_length + self.max_title_length)
                        * self.font_size,
                        line_index * self.font_size,
                    ),
                )
            )
        if track.key:
            # Track Key
            color = "#" + track.get_key_color()
            self._tracks_container.add(
                self.dwg.text(
                    key.openKeyToCamelotKey[track.key].value,
                    (
                        (
                            self.max_artist_name_length
                            + self.max_title_length
                            + self.max_bpm_length
                        )
                        * self.font_size,
                        line_index * self.font_size,
                    ),
                    fill=color,
                    style="font-weight:bold",
                )
            )

    def _get_result(self):
        return self.dwg
