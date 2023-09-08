# Generated by Django 4.2 on 2023-05-03 05:46

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0005_remove_item_snapshot_insert_and_more"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="item",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="item",
            name="snapshot_update",
        ),
        migrations.RemoveField(
            model_name="itemevent",
            name="modified_at",
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="item",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "crafting_level", "created_at", "description", "id", "image", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reg_weight", "runecube_weight", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."crafting_level", NEW."created_at", NEW."description", NEW."id", NEW."image", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reg_weight", NEW."runecube_weight", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="a3bcd00a234df1d8b82f739fc9ac66498a2a1900",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_9fd5a",
                    table="items_item",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="item",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."name" IS DISTINCT FROM (NEW."name") OR OLD."image" IS DISTINCT FROM (NEW."image") OR OLD."type" IS DISTINCT FROM (NEW."type") OR OLD."xp" IS DISTINCT FROM (NEW."xp") OR OLD."can_buy" IS DISTINCT FROM (NEW."can_buy") OR OLD."can_sell" IS DISTINCT FROM (NEW."can_sell") OR OLD."can_mail" IS DISTINCT FROM (NEW."can_mail") OR OLD."can_craft" IS DISTINCT FROM (NEW."can_craft") OR OLD."can_master" IS DISTINCT FROM (NEW."can_master") OR OLD."description" IS DISTINCT FROM (NEW."description") OR OLD."buy_price" IS DISTINCT FROM (NEW."buy_price") OR OLD."sell_price" IS DISTINCT FROM (NEW."sell_price") OR OLD."crafting_level" IS DISTINCT FROM (NEW."crafting_level") OR OLD."base_yield_minutes" IS DISTINCT FROM (NEW."base_yield_minutes") OR OLD."min_mailable_level" IS DISTINCT FROM (NEW."min_mailable_level") OR OLD."reg_weight" IS DISTINCT FROM (NEW."reg_weight") OR OLD."runecube_weight" IS DISTINCT FROM (NEW."runecube_weight") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "crafting_level", "created_at", "description", "id", "image", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reg_weight", "runecube_weight", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."crafting_level", NEW."created_at", NEW."description", NEW."id", NEW."image", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reg_weight", NEW."runecube_weight", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="d67fea2950c3659bb831faec281d7d24bc762b20",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_a9aca",
                    table="items_item",
                    when="AFTER",
                ),
            ),
        ),
    ]