# Generated by Django 4.2 on 2023-05-20 09:02

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("items", "0011_remove_item_snapshot_insert_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManualProduction",
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
                ("line_one", models.CharField(max_length=255)),
                ("line_two", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                ("sort", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manual_productions",
                        to="items.item",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ManualProductionEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("line_one", models.CharField(max_length=255)),
                ("line_two", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                ("sort", models.IntegerField(default=1)),
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
                        to="items.manualproduction",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="manualproduction",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "items_manualproductionevent" ("created_at", "id", "image", "item_id", "line_one", "line_two", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "sort", "value") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."item_id", NEW."line_one", NEW."line_two", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."sort", NEW."value"); RETURN NULL;',
                    hash="a03932a5406b4ddafae7b87575ffb28376b8ae54",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_a4046",
                    table="items_manualproduction",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="manualproduction",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."item_id" IS DISTINCT FROM (NEW."item_id") OR OLD."line_one" IS DISTINCT FROM (NEW."line_one") OR OLD."line_two" IS DISTINCT FROM (NEW."line_two") OR OLD."image" IS DISTINCT FROM (NEW."image") OR OLD."value" IS DISTINCT FROM (NEW."value") OR OLD."sort" IS DISTINCT FROM (NEW."sort") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "items_manualproductionevent" ("created_at", "id", "image", "item_id", "line_one", "line_two", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "sort", "value") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."item_id", NEW."line_one", NEW."line_two", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."sort", NEW."value"); RETURN NULL;',
                    hash="ac21cce9e68b2c21a7a22054a1133659ffcbfe6a",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_b26d4",
                    table="items_manualproduction",
                    when="AFTER",
                ),
            ),
        ),
    ]
