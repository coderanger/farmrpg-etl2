from django.db import migrations

BASE_DROP_RATES = {
    "Black Rock Canyon": 1 / 3,
    "Cane Pole Ridge": 2 / 7,
    "Ember Lagoon": 1 / 3,
    "Forest": 1 / 3,
    "Highland Hills": 1 / 4,
    "Misty Forest": 1 / 3,
    "Mount Banon": 1 / 3,
    "Small Cave": 2 / 5,
    "Small Spring": 1 / 3,
    "Whispering Creek": 4 / 15,
    "Jundland Desert": 4 / 15,
    "Haunted House": 2 / 5,
    "Santa's Workshop": 2 / 5,
}


def initial_base_drop_rates(apps, schema_editor):
    Location = apps.get_model("locations", "Location")
    for loc in Location.objects.all():
        if loc.name in BASE_DROP_RATES:
            loc.base_drop_rate = BASE_DROP_RATES[loc.name]
            loc.save(update_fields=["base_drop_rate"])


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0002_droprates_dropratesitem_droprates_location_flags_and_more"),
    ]

    operations = [
        migrations.RunPython(initial_base_drop_rates),
    ]
