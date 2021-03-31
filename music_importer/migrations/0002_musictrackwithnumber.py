# Generated by Django 3.1.7 on 2021-03-31 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("music_collection", "0001_initial"),
        ("music_importer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MusicTrackWithNumber",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.PositiveSmallIntegerField()),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collection",
                        to="music_collection.musiccollection",
                    ),
                ),
                (
                    "track_ptr",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="music_importer.musictrack",
                    ),
                ),
            ],
        ),
    ]
