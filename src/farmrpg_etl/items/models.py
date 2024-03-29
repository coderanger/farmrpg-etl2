import pghistory
from django.db import models


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class Item(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    xp = models.IntegerField()
    can_buy = models.BooleanField()
    can_sell = models.BooleanField()
    can_mail = models.BooleanField()
    can_craft = models.BooleanField()
    can_cook = models.BooleanField()
    can_master = models.BooleanField()
    can_locksmith = models.BooleanField()
    can_flea_market = models.BooleanField()
    description = models.TextField(blank=True)
    buy_price = models.IntegerField()
    flea_market_price = models.IntegerField(null=True, blank=True)
    flea_market_rotate = models.BooleanField()
    sell_price = models.IntegerField()
    crafting_level = models.IntegerField()
    cooking_level = models.IntegerField(null=True, blank=True)
    base_yield_minutes = models.IntegerField()
    min_mailable_level = models.IntegerField()
    reg_weight = models.IntegerField()
    runecube_weight = models.IntegerField()
    from_event = models.BooleanField(default=False)

    locksmith_grab_bag = models.BooleanField(null=True, default=False)
    locksmith_gold = models.IntegerField(null=True, blank=True)
    locksmith_key = models.ForeignKey(
        "Item",
        on_delete=models.SET_NULL,
        related_name="locksmith_key_items",
        null=True,
        blank=True,
    )

    # This should be a OneToOneField but that triggers a bug in Strawberry.
    # https://github.com/blb-ventures/strawberry-django-plus/issues/222
    cooking_recipe_item = models.OneToOneField(
        "Item",
        on_delete=models.SET_NULL,
        related_name="cooking_recipe_cookable",
        null=True,
        blank=True,
    )

    manual_fishing_only = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class RecipeItem(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="recipe_items"
    )
    ingredient_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="recipe_ingredient_items"
    )
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "ingredient_item"], name="item_ingredient_item"
            )
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class LocksmithItem(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="locksmith_items"
    )
    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="locksmith_output_items"
    )
    quantity_min = models.IntegerField(null=True, blank=True)
    quantity_max = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "output_item"], name="item_output_item"
            )
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class WishingWellItem(models.Model):
    input_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="wishing_well_input_items"
    )
    chance = models.FloatField()
    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="wishing_well_output_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["input_item", "output_item"], name="input_output"
            )
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class ManualProduction(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="manual_productions"
    )
    line_one = models.CharField(max_length=255)
    line_two = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    href = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255)
    sort = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class SkillLevelReward(models.Model):
    SKILL_FARMING = "farming"
    SKILL_FISHING = "fishing"
    SKILL_CRAFTING = "crafting"
    SKILL_EXPLORING = "exploring"
    SKILL_COOKING = "cooking"
    SKILL_CHOICES = [
        (SKILL_FARMING, "Farming"),
        (SKILL_FISHING, "Fishing"),
        (SKILL_CRAFTING, "Crafting"),
        (SKILL_EXPLORING, "Exploring"),
        (SKILL_COOKING, "Cooking"),
    ]

    skill = models.CharField(max_length=32, choices=SKILL_CHOICES, db_index=True)
    level = models.IntegerField(db_index=True)
    order = models.IntegerField(db_index=True)
    silver = models.BigIntegerField(null=True, blank=True)
    gold = models.IntegerField(null=True, blank=True)
    ak = models.IntegerField(null=True, blank=True)
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="skill_level_rewards",
        null=True,
        blank=True,
        db_index=True,
    )
    item_quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["level", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["skill", "level", "order"],
                name="skill_level_reward_level_order",
            ),
            models.CheckConstraint(
                check=models.Q(
                    silver__isnull=False,
                    gold=None,
                    ak=None,
                    item=None,
                    item_quantity=None,
                )
                | models.Q(
                    silver=None,
                    gold__isnull=False,
                    ak=None,
                    item=None,
                    item_quantity=None,
                )
                | models.Q(
                    silver=None,
                    gold=None,
                    ak__isnull=False,
                    item=None,
                    item_quantity=None,
                )
                | models.Q(
                    silver=None,
                    gold=None,
                    ak=None,
                    item__isnull=False,
                    item_quantity__isnull=False,
                ),
                name="skill_level_reward_only_one_type",
            ),
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class TempleReward(models.Model):
    input_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="temple_rewards"
    )
    input_quantity = models.IntegerField()
    silver = models.BigIntegerField(null=True, blank=True)
    gold = models.IntegerField(null=True, blank=True)
    min_level_required = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["input_item", "input_quantity"]
        constraints = [
            models.UniqueConstraint(
                fields=["input_item", "input_quantity"],
                name="input_item_input_quantity",
            ),
        ]


@pghistory.track(pghistory.Snapshot(), exclude=["modified_at"])
class TempleRewardItem(models.Model):
    temple_reward = models.ForeignKey(
        TempleReward, on_delete=models.CASCADE, related_name="items"
    )
    order = models.IntegerField()
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="temple_reward_items"
    )
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["temple_reward", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["temple_reward", "order"],
                name="temple_reward_order",
            ),
        ]
