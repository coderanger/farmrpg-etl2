# Generated by Django 4.2 on 2023-05-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0006_remove_quest_snapshot_insert_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quest",
            name="completed_count",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
