from django.db import migrations


def add_default_password_group(apps, schema_editor):
    PasswordGroup = apps.get_model("passwords", "PasswordGroup")
    db_alias = schema_editor.connection.alias
    PasswordGroup.objects.using(db_alias).get_or_create(
        id=0, defaults={"name": "Passwords"}
    )


class Migration(migrations.Migration):

    dependencies = [
        ("passwords", "0001_initial"),
    ]

    operations = [migrations.RunPython(add_default_password_group)]
