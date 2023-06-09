# Generated by Django 4.1.5 on 2023-03-13 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0004_alter_item_description_alter_itemevent_description"),
        ("quests", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quest",
            name="required_items",
        ),
        migrations.RemoveField(
            model_name="quest",
            name="reward_items",
        ),
        migrations.AlterField(
            model_name="questitemrequired",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="required_for_quest",
                to="items.item",
            ),
        ),
        migrations.AlterField(
            model_name="questitemrequired",
            name="quest",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="required_items",
                to="quests.quest",
            ),
        ),
        migrations.AlterField(
            model_name="questitemreward",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reward_for_quest",
                to="items.item",
            ),
        ),
        migrations.AlterField(
            model_name="questitemreward",
            name="quest",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reward_items",
                to="quests.quest",
            ),
        ),
    ]
