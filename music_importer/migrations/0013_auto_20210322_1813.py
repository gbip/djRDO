# Generated by Django 3.1.7 on 2021-03-22 18:13

from django.db import migrations, models
import music.key


class Migration(migrations.Migration):

    dependencies = [
        ("music_importer", "0012_auto_20210322_1707"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musictrack",
            name="key",
            field=models.CharField(
                blank=True,
                choices=[
                    (music.key.OpenKey["D1"], "1d"),
                    (music.key.OpenKey["D2"], "2d"),
                    (music.key.OpenKey["D3"], "3d"),
                    (music.key.OpenKey["D4"], "4d"),
                    (music.key.OpenKey["D5"], "5d"),
                    (music.key.OpenKey["D6"], "6d"),
                    (music.key.OpenKey["D7"], "7d"),
                    (music.key.OpenKey["D8"], "8d"),
                    (music.key.OpenKey["D9"], "9d"),
                    (music.key.OpenKey["D10"], "10d"),
                    (music.key.OpenKey["D11"], "11d"),
                    (music.key.OpenKey["D12"], "12d"),
                    (music.key.OpenKey["M1"], "1m"),
                    (music.key.OpenKey["M2"], "2m"),
                    (music.key.OpenKey["M3"], "3m"),
                    (music.key.OpenKey["M4"], "4m"),
                    (music.key.OpenKey["M5"], "5m"),
                    (music.key.OpenKey["M6"], "6m"),
                    (music.key.OpenKey["M7"], "7m"),
                    (music.key.OpenKey["M8"], "8m"),
                    (music.key.OpenKey["M9"], "9m"),
                    (music.key.OpenKey["M10"], "10m"),
                    (music.key.OpenKey["M11"], "11m"),
                    (music.key.OpenKey["M12"], "12m"),
                ],
                max_length=3,
                null=True,
            ),
        ),
    ]
