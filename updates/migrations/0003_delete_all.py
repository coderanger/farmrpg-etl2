from django.db import migrations


def delete_all_updates(apps, schema_editor):
    Update = apps.get_model("updates", "Update")
    db_alias = schema_editor.connection.alias
    Update.objects.using(db_alias).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("updates", "0002_remove_update_snapshot_insert_and_more"),
    ]

    operations = [
        migrations.RunPython(delete_all_updates, migrations.RunPython.noop),
    ]
