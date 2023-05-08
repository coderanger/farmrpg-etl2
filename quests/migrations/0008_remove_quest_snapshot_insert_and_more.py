# Generated by Django 4.2 on 2023-05-08 01:58

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quests", "0007_quest_completed_count"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="quest",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="quest",
            name="snapshot_update",
        ),
        migrations.AddField(
            model_name="quest",
            name="npc_img",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="questevent",
            name="npc_img",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="quest",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "quests_questevent" ("author", "created_at", "description", "end_date", "id", "main_quest", "npc", "npc_img", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pred_id", "required_cooking_level", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level", "required_npc_id", "required_npc_level", "required_silver", "required_tower_level", "reward_gold", "reward_silver", "start_date", "title") VALUES (NEW."author", NEW."created_at", NEW."description", NEW."end_date", NEW."id", NEW."main_quest", NEW."npc", NEW."npc_img", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."pred_id", NEW."required_cooking_level", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level", NEW."required_npc_id", NEW."required_npc_level", NEW."required_silver", NEW."required_tower_level", NEW."reward_gold", NEW."reward_silver", NEW."start_date", NEW."title"); RETURN NULL;',
                    hash="bd25f165d997626dcda1c2773d0d65995405ebd4",
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
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."npc" IS DISTINCT FROM (NEW."npc") OR OLD."npc_img" IS DISTINCT FROM (NEW."npc_img") OR OLD."title" IS DISTINCT FROM (NEW."title") OR OLD."author" IS DISTINCT FROM (NEW."author") OR OLD."pred_id" IS DISTINCT FROM (NEW."pred_id") OR OLD."start_date" IS DISTINCT FROM (NEW."start_date") OR OLD."end_date" IS DISTINCT FROM (NEW."end_date") OR OLD."main_quest" IS DISTINCT FROM (NEW."main_quest") OR OLD."description" IS DISTINCT FROM (NEW."description") OR OLD."required_silver" IS DISTINCT FROM (NEW."required_silver") OR OLD."required_farming_level" IS DISTINCT FROM (NEW."required_farming_level") OR OLD."required_fishing_level" IS DISTINCT FROM (NEW."required_fishing_level") OR OLD."required_crafting_level" IS DISTINCT FROM (NEW."required_crafting_level") OR OLD."required_exploring_level" IS DISTINCT FROM (NEW."required_exploring_level") OR OLD."required_cooking_level" IS DISTINCT FROM (NEW."required_cooking_level") OR OLD."required_tower_level" IS DISTINCT FROM (NEW."required_tower_level") OR OLD."required_npc_id" IS DISTINCT FROM (NEW."required_npc_id") OR OLD."required_npc_level" IS DISTINCT FROM (NEW."required_npc_level") OR OLD."reward_silver" IS DISTINCT FROM (NEW."reward_silver") OR OLD."reward_gold" IS DISTINCT FROM (NEW."reward_gold") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "quests_questevent" ("author", "created_at", "description", "end_date", "id", "main_quest", "npc", "npc_img", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "pred_id", "required_cooking_level", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level", "required_npc_id", "required_npc_level", "required_silver", "required_tower_level", "reward_gold", "reward_silver", "start_date", "title") VALUES (NEW."author", NEW."created_at", NEW."description", NEW."end_date", NEW."id", NEW."main_quest", NEW."npc", NEW."npc_img", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."pred_id", NEW."required_cooking_level", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level", NEW."required_npc_id", NEW."required_npc_level", NEW."required_silver", NEW."required_tower_level", NEW."reward_gold", NEW."reward_silver", NEW."start_date", NEW."title"); RETURN NULL;',
                    hash="29722373cdf94b5a1bbf94c684b58635d54d39e9",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_f7ef5",
                    table="quests_quest",
                    when="AFTER",
                ),
            ),
        ),
    ]
