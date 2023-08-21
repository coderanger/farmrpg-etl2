import factory

from items.models import Item


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.LazyAttribute(lambda obj: f"Item {obj.id}")
    image = ""
    type = ""
    xp = 0
    can_buy = False
    can_sell = False
    can_mail = False
    can_craft = False
    can_cook = False
    can_master = False
    can_locksmith = False
    can_flea_market = False
    buy_price = 0
    sell_price = 0
    crafting_level = 0
    base_yield_minutes = 0
    min_mailable_level = 0
    reg_weight = 1
    runecube_weight = 1
    flea_market_rotate = False
