from ..cron.decorators import cron
from .models import GamePet, Pet, PetItem


async def _update_pet_items(pet: Pet, level: int, items: str):
    seen_ids = []
    for i, item_id in enumerate(items.split(",")):
        pi, _ = await PetItem.objects.aupdate_or_create(
            pet=pet, level=level, item_id=int(item_id), defaults={"order": i}
        )
        seen_ids.append(pi.id)
    await PetItem.objects.filter(pet=pet, level=level).exclude(
        id__in=seen_ids
    ).adelete()


@cron("@hourly")
async def scrape_pets():
    async for gpet in GamePet.objects.all():
        pet, _ = await Pet.objects.aupdate_or_create(
            game_id=gpet.id,
            defaults={
                "name": gpet.name,
                "image": f"/img/pets/{gpet.img}",
                "cost": gpet.price,
                "order": gpet.display_order,
                "required_farming_level": gpet.farming_level,
                "required_fishing_level": gpet.fishing_level,
                "required_crafting_level": gpet.crafting_level,
                "required_exploring_level": gpet.exploring_level,
                "required_cooking_level": gpet.cooking_level,
            },
        )
        await _update_pet_items(pet, 1, gpet.items)
        await _update_pet_items(pet, 3, gpet.items3)
        await _update_pet_items(pet, 6, gpet.items6)
