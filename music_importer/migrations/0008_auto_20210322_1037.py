# Generated by Django 3.1.7 on 2021-03-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music_importer", "0007_auto_20210322_0920"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musictrack",
            name="bpm",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]