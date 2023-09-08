# Generated by Django 4.1.5 on 2023-03-19 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0004_alter_item_description_alter_itemevent_description"),
        ("quests", "0003_silver_bigint"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quest",
            name="pred",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="dependent_quests",
                to="quests.quest",
            ),
        ),
        migrations.AlterField(
            model_name="questitemrequired",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="required_for_quests",
                to="items.item",
            ),
        ),
        migrations.AlterField(
            model_name="questitemreward",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reward_for_quests",
                to="items.item",
            ),
        ),
    ]