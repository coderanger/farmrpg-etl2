# Generated by Django 4.2.2 on 2023-08-21 07:08

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("items", "0025_item_fields_fm"),
    ]

    operations = [
        migrations.CreateModel(
            name="TempleReward",
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
                ("input_quantity", models.IntegerField()),
                ("silver", models.BigIntegerField(blank=True, null=True)),
                ("gold", models.IntegerField(blank=True, null=True)),
                ("min_level_required", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "input_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="temple_rewards",
                        to="items.item",
                    ),
                ),
            ],
            options={
                "ordering": ["input_item", "input_quantity"],
            },
        ),
        migrations.CreateModel(
            name="TempleRewardItem",
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
                ("order", models.IntegerField()),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="temple_reward_items",
                        to="items.item",
                    ),
                ),
                (
                    "temple_reward",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="items.templereward",
                    ),
                ),
            ],
            options={
                "ordering": ["temple_reward", "order"],
            },
        ),
        migrations.CreateModel(
            name="TempleRewardItemEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("order", models.IntegerField()),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
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
                        to="items.templerewarditem",
                    ),
                ),
                (
                    "temple_reward",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="items.templereward",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TempleRewardEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("input_quantity", models.IntegerField()),
                ("silver", models.BigIntegerField(blank=True, null=True)),
                ("gold", models.IntegerField(blank=True, null=True)),
                ("min_level_required", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "input_item",
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
                        to="items.templereward",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddConstraint(
            model_name="templerewarditem",
            constraint=models.UniqueConstraint(
                fields=("temple_reward", "order"), name="temple_reward_order"
            ),
        ),
        migrations.AddConstraint(
            model_name="templereward",
            constraint=models.UniqueConstraint(
                fields=("input_item", "input_quantity"),
                name="input_item_input_quantity",
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="templerewarditem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_templerewarditemevent" ("created_at", "id", "item_id", "order", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "temple_reward_id") VALUES (NEW."created_at", NEW."id", NEW."item_id", NEW."order", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."temple_reward_id"); RETURN NULL;',
                    hash="7a08ace613b39a1f49c55be809fa7bdc0aa2628b",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_2317b",
                    table="items_templerewarditem",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="templerewarditem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."temple_reward_id" IS DISTINCT FROM (NEW."temple_reward_id") OR OLD."order" IS DISTINCT FROM (NEW."order") OR OLD."item_id" IS DISTINCT FROM (NEW."item_id") OR OLD."quantity" IS DISTINCT FROM (NEW."quantity") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "items_templerewarditemevent" ("created_at", "id", "item_id", "order", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity", "temple_reward_id") VALUES (NEW."created_at", NEW."id", NEW."item_id", NEW."order", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity", NEW."temple_reward_id"); RETURN NULL;',
                    hash="e949bb9a80f4ab3c948a039c4ddee6f70693eda7",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_96a0d",
                    table="items_templerewarditem",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="templereward",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_templerewardevent" ("created_at", "gold", "id", "input_item_id", "input_quantity", "min_level_required", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "silver") VALUES (NEW."created_at", NEW."gold", NEW."id", NEW."input_item_id", NEW."input_quantity", NEW."min_level_required", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."silver"); RETURN NULL;',
                    hash="d6e459f9ea477b24de21b9d99109d70a68639807",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_91d0a",
                    table="items_templereward",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="templereward",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."input_item_id" IS DISTINCT FROM (NEW."input_item_id") OR OLD."input_quantity" IS DISTINCT FROM (NEW."input_quantity") OR OLD."silver" IS DISTINCT FROM (NEW."silver") OR OLD."gold" IS DISTINCT FROM (NEW."gold") OR OLD."min_level_required" IS DISTINCT FROM (NEW."min_level_required") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "items_templerewardevent" ("created_at", "gold", "id", "input_item_id", "input_quantity", "min_level_required", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "silver") VALUES (NEW."created_at", NEW."gold", NEW."id", NEW."input_item_id", NEW."input_quantity", NEW."min_level_required", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."silver"); RETURN NULL;',
                    hash="8c5b6d8fd9a341cd1a11d70cdcac00f0b0d744d7",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_1ce1c",
                    table="items_templereward",
                    when="AFTER",
                ),
            ),
        ),
    ]
