# Generated by Django 4.2 on 2023-05-01 02:06

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="pet",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="pet",
            name="snapshot_update",
        ),
        migrations.AddField(
            model_name="pet",
            name="game_id",
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="petevent",
            name="game_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="pet",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "pets_petevent" ("cost", "game_id", "id", "image", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level") VALUES (NEW."cost", NEW."game_id", NEW."id", NEW."image", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level"); RETURN NULL;',
                    hash="24e1dc69c49c43d603e4d78d38ebd9e71128a886",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_0ddae",
                    table="pets_pet",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="pet",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "pets_petevent" ("cost", "game_id", "id", "image", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "required_crafting_level", "required_exploring_level", "required_farming_level", "required_fishing_level") VALUES (NEW."cost", NEW."game_id", NEW."id", NEW."image", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."required_crafting_level", NEW."required_exploring_level", NEW."required_farming_level", NEW."required_fishing_level"); RETURN NULL;',
                    hash="882b0f32b25584ad8cfd05ee1f82104e38cb0cb5",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_fe0fe",
                    table="pets_pet",
                    when="AFTER",
                ),
            ),
        ),
    ]