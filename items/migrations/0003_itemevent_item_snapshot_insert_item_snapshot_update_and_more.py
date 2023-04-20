# Generated by Django 4.1.5 on 2023-01-08 01:51

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("items", "0002_item_buy_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItemEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("xp", models.IntegerField()),
                ("can_buy", models.BooleanField()),
                ("can_sell", models.BooleanField()),
                ("can_mail", models.BooleanField()),
                ("can_craft", models.BooleanField()),
                ("can_master", models.BooleanField()),
                ("description", models.TextField()),
                ("buy_price", models.IntegerField()),
                ("sell_price", models.IntegerField()),
                ("crafting_level", models.IntegerField()),
                ("base_yield_minutes", models.IntegerField()),
                ("min_mailable_level", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="item",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "crafting_level", "description", "id", "image", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."crafting_level", NEW."description", NEW."id", NEW."image", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="c0664d60d841db4ede19ceacf36c29f4d37b8e89",
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
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "items_itemevent" ("base_yield_minutes", "buy_price", "can_buy", "can_craft", "can_mail", "can_master", "can_sell", "crafting_level", "description", "id", "image", "min_mailable_level", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "sell_price", "type", "xp") VALUES (NEW."base_yield_minutes", NEW."buy_price", NEW."can_buy", NEW."can_craft", NEW."can_mail", NEW."can_master", NEW."can_sell", NEW."crafting_level", NEW."description", NEW."id", NEW."image", NEW."min_mailable_level", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."sell_price", NEW."type", NEW."xp"); RETURN NULL;',
                    hash="480f70000cf4693cc68db0a160881933a99d3d9c",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_a9aca",
                    table="items_item",
                    when="AFTER",
                ),
            ),
        ),
        migrations.AddField(
            model_name="itemevent",
            name="pgh_context",
            field=models.ForeignKey(
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="pghistory.context",
            ),
        ),
        migrations.AddField(
            model_name="itemevent",
            name="pgh_obj",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="event",
                to="items.item",
            ),
        ),
    ]
