# Generated by Django 3.1.7 on 2021-03-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music_importer", "0003_musictrack_date_released"),
    ]

    operations = [
        migrations.AddField(
            model_name="musictrack",
            name="genre",
            field=models.CharField(default="nogenre", max_length=200),
            preserve_default=False,
        ),
    ]
