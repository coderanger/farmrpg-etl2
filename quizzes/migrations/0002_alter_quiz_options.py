# Generated by Django 4.2 on 2023-05-08 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quizzes", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quiz",
            options={"verbose_name_plural": "quizzes"},
        ),
    ]
