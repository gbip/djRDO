# Generated by Django 3.1.7 on 2021-03-22 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music_importer", "0005_auto_20210319_1432"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="name",
            field=models.CharField(max_length=5000, unique=True),
        ),
    ]
