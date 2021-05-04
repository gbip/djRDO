import svgwrite
from django.db.models import Max
from django.db.models.functions import Length

from utils import key


def music_set_to_svg(music_set, name):
    font_size = 16

    title_length = music_set.aggregate(title_len=Max(Length("title")))["title_len"]
    artist_length = music_set.aggregate(artist_len=Max(Length("artist__name")))[
        "artist_len"
    ]
    bpm_length = len(str(music_set.aggregate(bpm_len=Max("bpm"))["bpm_len"]))

    width = ((title_length + artist_length + bpm_length) * font_size) + 100
    height = font_size * (len(music_set) + 3)
    dwg = svgwrite.Drawing(
        "Cover",
        (
            width,
            height,
        ),
    )
    dwg.add(
        dwg.text(
            name,
            ((width / 2) - (len(name) * font_size) / 2, font_size),
            style="font-weight:bold;text-decoration:underline",
        )
    )
    paragraph = dwg.add(dwg.g(font_size=font_size))

    # First add track number and names
    for (i, music) in enumerate(music_set):
        line_index = (
            i + 3
        )  # Offset between the line number, and the item index in the query set
        track = music
        track_str = str(i + 1) + " - " + track.title
        # Track title
        paragraph.add(dwg.text(track_str, (0, line_index * font_size), fill="black"))
        # Track artist
        paragraph.add(
            dwg.text(
                track.artist.name, (title_length * font_size, line_index * font_size)
            )
        )
        # Track BPM
        paragraph.add(
            dwg.text(
                track.bpm,
                ((artist_length + title_length) * font_size, line_index * font_size),
            )
        )
        # Track Key
        color = "#" + track.get_key_color()
        paragraph.add(
            dwg.text(
                key.openKeyToCamelotKey[track.key].value,
                (
                    (artist_length + title_length + bpm_length) * font_size,
                    line_index * font_size,
                ),
                fill=color,
                style="font-weight:bold",
            )
        )

    return dwg
