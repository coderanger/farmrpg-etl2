# Generated by Django 4.2 on 2023-05-23 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("updates", "0003_delete_all"),
    ]

    operations = [
        migrations.AlterField(
            model_name="update",
            name="date",
            field=models.DateField(db_index=True),
        ),
    ]
