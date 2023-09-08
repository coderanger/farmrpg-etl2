# Generated by Django 4.2 on 2023-05-27 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0010_questlines"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="questlinestep",
            constraint=models.UniqueConstraint(
                fields=("questline", "quest"), name="questline_quest"
            ),
        ),
    ]