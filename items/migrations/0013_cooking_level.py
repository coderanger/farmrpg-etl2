# Generated by Django 4.2 on 2023-05-22 04:26

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("items", "0012_manual_productions"),
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
        migrations.AddField(
            model_name="item",
            name="cooking_level",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="itemevent",
            name="cooking_level",
            field=models.IntegerField(blank=True, null=True),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="item",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "cooking_level", "cooking_recipe_item_id", "crafting_level", "created_at", "description", "id", "image", "locksmith_gold", "locksmith_grab_bag", "locksmith_key_id", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reg_weight", "runecube_weight", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."cooking_level", NEW."cooking_recipe_item_id", NEW."crafting_level", NEW."created_at", NEW."description", NEW."id", NEW."image", NEW."locksmith_gold", NEW."locksmith_grab_bag", NEW."locksmith_key_id", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reg_weight", NEW."runecube_weight", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="4ee7698b2a35d19d3774645d9e59d2a703306d9f",
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
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."name" IS DISTINCT FROM (NEW."name") OR OLD."image" IS DISTINCT FROM (NEW."image") OR OLD."type" IS DISTINCT FROM (NEW."type") OR OLD."xp" IS DISTINCT FROM (NEW."xp") OR OLD."can_buy" IS DISTINCT FROM (NEW."can_buy") OR OLD."can_sell" IS DISTINCT FROM (NEW."can_sell") OR OLD."can_mail" IS DISTINCT FROM (NEW."can_mail") OR OLD."can_craft" IS DISTINCT FROM (NEW."can_craft") OR OLD."can_master" IS DISTINCT FROM (NEW."can_master") OR OLD."description" IS DISTINCT FROM (NEW."description") OR OLD."buy_price" IS DISTINCT FROM (NEW."buy_price") OR OLD."sell_price" IS DISTINCT FROM (NEW."sell_price") OR OLD."crafting_level" IS DISTINCT FROM (NEW."crafting_level") OR OLD."cooking_level" IS DISTINCT FROM (NEW."cooking_level") OR OLD."base_yield_minutes" IS DISTINCT FROM (NEW."base_yield_minutes") OR OLD."min_mailable_level" IS DISTINCT FROM (NEW."min_mailable_level") OR OLD."reg_weight" IS DISTINCT FROM (NEW."reg_weight") OR OLD."runecube_weight" IS DISTINCT FROM (NEW."runecube_weight") OR OLD."locksmith_grab_bag" IS DISTINCT FROM (NEW."locksmith_grab_bag") OR OLD."locksmith_gold" IS DISTINCT FROM (NEW."locksmith_gold") OR OLD."locksmith_key_id" IS DISTINCT FROM (NEW."locksmith_key_id") OR OLD."cooking_recipe_item_id" IS DISTINCT FROM (NEW."cooking_recipe_item_id") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "cooking_level", "cooking_recipe_item_id", "crafting_level", "created_at", "description", "id", "image", "locksmith_gold", "locksmith_grab_bag", "locksmith_key_id", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reg_weight", "runecube_weight", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."cooking_level", NEW."cooking_recipe_item_id", NEW."crafting_level", NEW."created_at", NEW."description", NEW."id", NEW."image", NEW."locksmith_gold", NEW."locksmith_grab_bag", NEW."locksmith_key_id", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reg_weight", NEW."runecube_weight", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="ad3104bdc4a59ee2abe4800a7d8093a6f7425018",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_a9aca",
                    table="items_item",
                    when="AFTER",
                ),
            ),
        ),
    ]
