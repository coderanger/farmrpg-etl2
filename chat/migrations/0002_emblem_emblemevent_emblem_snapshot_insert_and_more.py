# Generated by Django 4.2 on 2023-05-08 08:10

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Emblem",
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
                ("name", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (None, "Everyone"),
                            ("patreon", "Patreon"),
                            ("staff", "Staff"),
                        ],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("keywords", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["created_at", "pk"],
            },
        ),
        migrations.CreateModel(
            name="EmblemEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("image", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            (None, "Everyone"),
                            ("patreon", "Patreon"),
                            ("staff", "Staff"),
                        ],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("keywords", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
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
                        to="chat.emblem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="emblem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "chat_emblemevent" ("created_at", "id", "image", "keywords", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "type") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."keywords", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."type"); RETURN NULL;',
                    hash="0f512a21e630c998eed7164ef20c30465de9aa23",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_a196b",
                    table="chat_emblem",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="emblem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."name" IS DISTINCT FROM (NEW."name") OR OLD."image" IS DISTINCT FROM (NEW."image") OR OLD."type" IS DISTINCT FROM (NEW."type") OR OLD."keywords" IS DISTINCT FROM (NEW."keywords") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "chat_emblemevent" ("created_at", "id", "image", "keywords", "name", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "type") VALUES (NEW."created_at", NEW."id", NEW."image", NEW."keywords", NEW."name", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."type"); RETURN NULL;',
                    hash="3655458fb8309b54b29dfd111c32084f2a26ba09",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_a0ad7",
                    table="chat_emblem",
                    when="AFTER",
                ),
            ),
        ),
    ]
