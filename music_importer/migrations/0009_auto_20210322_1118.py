# Generated by Django 3.1.7 on 2021-03-22 11:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("music_importer", "0008_auto_20210322_1037"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musictrack",
            name="bpm",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="musictrack",
            name="import_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]