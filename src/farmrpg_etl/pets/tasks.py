from ..cron.decorators import cron
from .models import Pet, PetItem
from ..utils.http import client


async def _update_pet_items(pet: Pet, level: int, items: str):
    seen_ids = []
    for i, item_id in enumerate(items.split(",")):
        pi, _ = await PetItem.objects.aupdate_or_create(
            pet=pet, level=level, item_id=int(item_id), defaults={"order": i}
        )
        seen_ids.append(pi.id)
    await (
        PetItem.objects.filter(pet=pet, level=level).exclude(id__in=seen_ids).adelete()
    )


@cron("@hourly")
async def scrape_pets():
    resp = await client.get("/api.php?method=pets")
    resp.raise_for_status()
    data = resp.json()

    for pet_data in data["pets"]:
        pet, _ = await Pet.objects.aupdate_or_create(
            game_id=pet_data["id"],
            defaults={
                "name": pet_data["name"],
                "image": f"/img/pets/{pet_data['img']}",
                "cost": pet_data["price"],
                "order": pet_data["display_order"],
                "required_farming_level": pet_data["farming_level"],
                "required_fishing_level": pet_data["fishing_level"],
                "required_crafting_level": pet_data["crafting_level"],
                "required_exploring_level": pet_data["exploring_level"],
                "required_cooking_level": pet_data["cooking_level"],
            },
        )
        await _update_pet_items(pet, 1, pet_data["items"])
        await _update_pet_items(pet, 3, pet_data["items3"])
        await _update_pet_items(pet, 6, pet_data["items6"])
