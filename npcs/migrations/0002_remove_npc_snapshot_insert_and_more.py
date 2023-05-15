# Generated by Django 4.2 on 2023-05-12 06:54

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("npcs", "0001_initial"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="npc",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="npc",
            name="snapshot_update",
        ),
        migrations.AddField(
            model_name="npc",
            name="short_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="npcevent",
            name="short_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="npcitem",
            name="relationship",
            field=models.CharField(
                choices=[("loves", "Loves"), ("likes", "Likes"), ("hates", "Hates")],
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="npcitemevent",
            name="relationship",
            field=models.CharField(
                choices=[("loves", "Loves"), ("likes", "Likes"), ("hates", "Hates")],
                max_length=32,
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="npc",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "npcs_npcevent" ("created_at", "id", "image", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "short_name") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."short_name"); RETURN NULL;',
                    hash="eec08abc3b1aaf79e36cdd83af55c09410e7fedc",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_d1bdb",
                    table="npcs_npc",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="npc",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."name" IS DISTINCT FROM (NEW."name") OR OLD."image" IS DISTINCT FROM (NEW."image") OR OLD."short_name" IS DISTINCT FROM (NEW."short_name") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "npcs_npcevent" ("created_at", "id", "image", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "short_name") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."short_name"); RETURN NULL;',
                    hash="42b92aeb1220d616ba4232a87074356bf2ada4ae",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_9156b",
                    table="npcs_npc",
                    when="AFTER",
                ),
            ),
        ),
    ]