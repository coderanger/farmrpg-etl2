# Generated by Django 4.1.5 on 2023-03-13 04:21

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("items", "0004_alter_item_description_alter_itemevent_description"),
        ("pghistory", "0005_events_middlewareevents"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("npc", models.CharField(db_index=True, max_length=255)),
                ("title", models.CharField(db_index=True, max_length=255)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("main_quest", models.BooleanField()),
                ("description", models.TextField()),
                ("required_silver", models.IntegerField()),
                ("required_farming_level", models.IntegerField()),
                ("required_fishing_level", models.IntegerField()),
                ("required_crafting_level", models.IntegerField()),
                ("required_exploring_level", models.IntegerField()),
                ("required_cooking_level", models.IntegerField()),
                ("required_tower_level", models.IntegerField()),
                ("required_npc_id", models.IntegerField()),
                ("required_npc_level", models.IntegerField()),
                ("reward_silver", models.IntegerField()),
                ("reward_gold", models.IntegerField()),
                (
                    "pred",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="quests.quest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestItemRequired",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quests.quest"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QuestItemReward",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="items.item"
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quests.quest"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QuestItemRewardEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("quantity", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="items.item",
                    ),
                ),
                (
                    "pgh_context",
                    models.ForeignKey(
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="pghistory.context",
                    ),
                ),
                (
                    "pgh_obj",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="event",
                        to="quests.questitemreward",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="quests.quest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QuestItemRequiredEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("quantity", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="items.item",
                    ),
                ),
                (
                    "pgh_context",
                    models.ForeignKey(
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="pghistory.context",
                    ),
                ),
                (
                    "pgh_obj",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="event",
                        to="quests.questitemrequired",
                    ),
                ),
                (
                    "quest",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="quests.quest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="QuestEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("npc", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("main_quest", models.BooleanField()),
                ("description", models.TextField()),
                ("required_silver", models.IntegerField()),
                ("required_farming_level", models.IntegerField()),
                ("required_fishing_level", models.IntegerField()),
                ("required_crafting_level", models.IntegerField()),
                ("required_exploring_level", models.IntegerField()),
                ("required_cooking_level", models.IntegerField()),
                ("required_tower_level", models.IntegerField()),
                ("required_npc_id", models.IntegerField()),
                ("required_npc_level", models.IntegerField()),
                ("reward_silver", models.IntegerField()),
                ("reward_gold", models.IntegerField()),
                (
                    "pgh_context",
                    models.ForeignKey(
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="pghistory.context",
                    ),
                ),
                (
                    "pgh_obj",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="event",
                        to="quests.quest",
                    ),
                ),
                (
                    "pred",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="quests.quest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="quest",
            name="required_items",
            field=models.ManyToManyField(
                related_name="required_for_quest",
                through="quests.QuestItemRequired",
                to="items.item",
            ),
        ),
        migrations.AddField(
            model_name="quest",
            name="reward_items",
            field=models.ManyToManyField(
                related_name="reward_for_quest",
                through="quests.QuestItemReward",
                to="items.item",
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="questitemreward",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "quests_questitemrewardevent" ("id", "item_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "quest_id") VALUES (NEW."id", NEW."item_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."quest_id"); RETURN NULL;',
                    hash="c489d4d16d9568bdb2756c868aa203851a812487",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_272f4",
                    table="quests_questitemreward",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="questitemreward",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "quests_questitemrewardevent" ("id", "item_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "quest_id") VALUES (NEW."id", NEW."item_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."quest_id"); RETURN NULL;',
                    hash="0ab39c18e16e0617983db61703924bb18b50a6fd",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_b391c",
                    table="quests_questitemreward",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="questitemrequired",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "quests_questitemrequiredevent" ("id", "item_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "quest_id") VALUES (NEW."id", NEW."item_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."quest_id"); RETURN NULL;',
                    hash="d564e6b238820eb9ff03b39185e3b84995d115cf",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_33d3b",
                    table="quests_questitemrequired",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="questitemrequired",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "quests_questitemrequiredevent" ("id", "item_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "quest_id") VALUES (NEW."id", NEW."item_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."quest_id"); RETURN NULL;',
                    hash="4f932fd5b0bbcd8fb770a646e71f3d206dd9a646",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_8962c",
                    table="quests_questitemrequired",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="quest",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "quests_questevent" ("author", "description", "end_date", "id", "main_quest", "npc", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pred_id", "required_cooking_level", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level", "required_npc_id", "required_npc_level", "required_silver", "required_tower_level", "reward_gold", "reward_silver", "start_date", "title") VALUES (NEW."author", NEW."description", NEW."end_date", NEW."id", NEW."main_quest", NEW."npc", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."pred_id", NEW."required_cooking_level", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level", NEW."required_npc_id", NEW."required_npc_level", NEW."required_silver", NEW."required_tower_level", NEW."reward_gold", NEW."reward_silver", NEW."start_date", NEW."title"); RETURN NULL;',
                    hash="06ca10bc326960cc26e827ad154847fe7b4296a6",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_d9ad1",
                    table="quests_quest",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="quest",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "quests_questevent" ("author", "description", "end_date", "id", "main_quest", "npc", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pred_id", "required_cooking_level", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level", "required_npc_id", "required_npc_level", "required_silver", "required_tower_level", "reward_gold", "reward_silver", "start_date", "title") VALUES (NEW."author", NEW."description", NEW."end_date", NEW."id", NEW."main_quest", NEW."npc", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."pred_id", NEW."required_cooking_level", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level", NEW."required_npc_id", NEW."required_npc_level", NEW."required_silver", NEW."required_tower_level", NEW."reward_gold", NEW."reward_silver", NEW."start_date", NEW."title"); RETURN NULL;',
                    hash="afd176190a4343a0837114289a33eaf9247902af",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_f7ef5",
                    table="quests_quest",
                    when="AFTER",
                ),
            ),
        ),
    ]
