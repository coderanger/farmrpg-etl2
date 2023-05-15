# Generated by Django 4.2 on 2023-05-15 19:06

from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pghistory", "0005_events_middlewareevents"),
        ("items", "0006_remove_item_snapshot_insert_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Password",
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
                ("password", models.CharField(max_length=255, unique=True)),
                ("clue1", models.TextField(blank=True, null=True)),
                ("clue2", models.TextField(blank=True, null=True)),
                ("clue3", models.TextField(blank=True, null=True)),
                ("reward_silver", models.BigIntegerField(default=0)),
                ("reward_gold", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PasswordGroup",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PasswordItem",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="password_items",
                        to="items.item",
                    ),
                ),
                (
                    "password",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reward_items",
                        to="passwords.password",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PasswordItemEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
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
                    "password",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="passwords.password",
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
                        to="passwords.passworditem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PasswordEvent",
            fields=[
                ("pgh_id", models.AutoField(primary_key=True, serialize=False)),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                ("id", models.IntegerField()),
                ("password", models.CharField(max_length=255)),
                ("clue1", models.TextField(blank=True, null=True)),
                ("clue2", models.TextField(blank=True, null=True)),
                ("clue3", models.TextField(blank=True, null=True)),
                ("reward_silver", models.BigIntegerField(default=0)),
                ("reward_gold", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "group",
                    models.ForeignKey(
                        db_constraint=False,
                        default=0,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        related_query_name="+",
                        to="passwords.passwordgroup",
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
                        to="passwords.password",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="password",
            name="group",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passwords",
                to="passwords.passwordgroup",
            ),
        ),
        migrations.AddConstraint(
            model_name="passworditem",
            constraint=models.UniqueConstraint(
                fields=("password", "item"), name="password_item"
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="passworditem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "passwords_passworditemevent" ("created_at", "id", "item_id", "password_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity") VALUES (NEW."created_at", NEW."id", NEW."item_id", NEW."password_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity"); RETURN NULL;',
                    hash="5e656dc921ef942a89363ef7d7fd84271f8d66e5",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_13a1c",
                    table="passwords_passworditem",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="passworditem",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."password_id" IS DISTINCT FROM (NEW."password_id") OR OLD."item_id" IS DISTINCT FROM (NEW."item_id") OR OLD."quantity" IS DISTINCT FROM (NEW."quantity") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "passwords_passworditemevent" ("created_at", "id", "item_id", "password_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "quantity") VALUES (NEW."created_at", NEW."id", NEW."item_id", NEW."password_id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."quantity"); RETURN NULL;',
                    hash="ec7ec68f75c3a8b8ae2798e88f58256e52e53c91",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_c47f0",
                    table="passwords_passworditem",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="password",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "passwords_passwordevent" ("clue1", "clue2", "clue3", "created_at", "group_id", "id", "password", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reward_gold", "reward_silver") VALUES (NEW."clue1", NEW."clue2", NEW."clue3", NEW."created_at", NEW."group_id", NEW."id", NEW."password", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reward_gold", NEW."reward_silver"); RETURN NULL;',
                    hash="3aefafb0a032b8c472dd37bf07d1c69751980589",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_0dd3b",
                    table="passwords_password",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="password",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."group_id" IS DISTINCT FROM (NEW."group_id") OR OLD."password" IS DISTINCT FROM (NEW."password") OR OLD."clue1" IS DISTINCT FROM (NEW."clue1") OR OLD."clue2" IS DISTINCT FROM (NEW."clue2") OR OLD."clue3" IS DISTINCT FROM (NEW."clue3") OR OLD."reward_silver" IS DISTINCT FROM (NEW."reward_silver") OR OLD."reward_gold" IS DISTINCT FROM (NEW."reward_gold") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "passwords_passwordevent" ("clue1", "clue2", "clue3", "created_at", "group_id", "id", "password", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "reward_gold", "reward_silver") VALUES (NEW."clue1", NEW."clue2", NEW."clue3", NEW."created_at", NEW."group_id", NEW."id", NEW."password", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."reward_gold", NEW."reward_silver"); RETURN NULL;',
                    hash="69428bd603c2d292903616bce83e04b7458f9d2b",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_96276",
                    table="passwords_password",
                    when="AFTER",
                ),
            ),
        ),
    ]
