# Generated by Django 3.1.7 on 2021-03-31 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("music_collection", "0001_initial"),
        ("music_importer", "0002_musictrackwithnumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musictrackwithnumber",
            name="collection",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="track",
                to="music_collection.musiccollection",
            ),
        ),
        migrations.AlterField(
            model_name="musictrackwithnumber",
            name="track_ptr",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collection",
                to="music_importer.musictrack",
            ),
        ),
    ]
