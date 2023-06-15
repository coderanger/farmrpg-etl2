from django.contrib import admin

from utils.admin import ReadOnlyAdmin

from .models import Trade, TradeHistory, CardsTrade


class TradeHistoryInline(admin.TabularInline):
    model = TradeHistory
    extra = 0


@admin.register(Trade)
class TradeAdmin(ReadOnlyAdmin):
    list_display = [
        "input_item",
        "input_quantity",
        "output_item",
        "output_quantity",
        "oneshot",
        "last_seen",
    ]
    inlines = [TradeHistoryInline]


@admin.register(CardsTrade)
class CardsTradeAdmin(ReadOnlyAdmin):
    list_display = [
        "id",
        "spades_quantity",
        "hearts_quantity",
        "diamonds_quantity",
        "clubs_quantity",
        "joker_quantity",
        "output_item",
        "output_quantity",
        "is_disabled",
    ]
