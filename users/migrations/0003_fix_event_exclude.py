# Generated by Django 4.2 on 2023-05-25 05:56

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_snapshot_insert_and_more"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="user",
            name="snapshot_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="user",
            name="snapshot_update",
        ),
        migrations.RemoveField(
            model_name="userevent",
            name="modified_at",
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="user",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "users_userevent" ("created_at", "firebase_uid", "id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "role", "username") VALUES (NEW."created_at", NEW."firebase_uid", NEW."id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."role", NEW."username"); RETURN NULL;',
                    hash="bc0989797f04f6a1cc5749af659f348c4bfb3c21",
                    operation="INSERT",
                    pgid="pgtrigger_snapshot_insert_a79f7",
                    table="users_user",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="user",
            trigger=pgtrigger.compiler.Trigger(
                name="snapshot_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM (NEW."id") OR OLD."username" IS DISTINCT FROM (NEW."username") OR OLD."role" IS DISTINCT FROM (NEW."role") OR OLD."firebase_uid" IS DISTINCT FROM (NEW."firebase_uid") OR OLD."created_at" IS DISTINCT FROM (NEW."created_at"))',
                    func='INSERT INTO "users_userevent" ("created_at", "firebase_uid", "id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "role", "username") VALUES (NEW."created_at", NEW."firebase_uid", NEW."id", _pgh_attach_context(), NOW(), \'snapshot\', NEW."id", NEW."role", NEW."username"); RETURN NULL;',
                    hash="fae73e336f03754c54342cdcd8bcc9ff34049d4b",
                    operation="UPDATE",
                    pgid="pgtrigger_snapshot_update_e726b",
                    table="users_user",
                    when="AFTER",
                ),
            ),
        ),
    ]
