# Generated by Django 4.2 on 2023-05-27 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("community_center", "0002_output_gold"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="communitycenter",
            options={"ordering": ["-date"]},
        ),
    ]
