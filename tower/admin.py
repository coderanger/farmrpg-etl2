from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django import forms

from items.models import Item

from .models import TowerReward
from .parsers import parse_tower_txt


class ImportForm(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        parsed = list(parse_tower_txt(cleaned_data["text"] + "\n"))
        if len(parsed) == 0:
            raise forms.ValidationError("No rewards found")
        if parsed[-1].level != 1:
            raise forms.ValidationError("Does not end with level 1")
        expected_level = parsed[0].level
        expected_order = 1
        for p in parsed:
            if p.level != expected_level:
                raise forms.ValidationError(
                    f"Unexpected level, got {p.level} expected {expected_level}"
                )
            if p.order != expected_order:
                raise forms.ValidationError(
                    f"Unexpected order on level {expected_level}, got {p.order} expected {expected_order}"
                )
            expected_order += 1
            if expected_order == 4:
                expected_level -= 1
                expected_order = 1
        cleaned_data["parsed_rewards"] = parsed
        return cleaned_data


@admin.register(TowerReward)
class TowerRewardAdmin(admin.ModelAdmin):
    list_display = ["level", "order", "admin_reward"]

    @admin.display(description="Reward")
    def admin_reward(self, obj: TowerReward) -> str:
        if obj.silver is not None:
            return f"Silver (x{obj.silver})"
        elif obj.gold is not None:
            return f"Gold (x{obj.gold})"
        else:
            return f"{obj.item.name} (x{obj.item_quantity})"

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path(
                "import/",
                self.admin_site.admin_view(self.import_view),
                name="tower_towerreward_import",
            ),
        ]
        return extra_urls + urls

    def import_view(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST":
            form = ImportForm(request.POST)
            if form.is_valid():
                seen_ids = []
                for parsed in form.cleaned_data["parsed_rewards"]:
                    data = {}
                    if parsed.item == "Silver":
                        data["silver"] = parsed.quantity
                    elif parsed.item == "Gold":
                        data["gold"] = parsed.quantity
                    else:
                        data["item_id"] = Item.objects.values_list("id", flat=True).get(
                            name=parsed.item
                        )
                        data["item_quantity"] = parsed.quantity
                    tr, _ = TowerReward.objects.update_or_create(
                        level=parsed.level, order=parsed.order, defaults=data
                    )
                    seen_ids.append(tr.id)
                TowerReward.objects.exclude(id__in=seen_ids).delete()

                return HttpResponseRedirect(
                    reverse("admin:tower_towerreward_changelist")
                )
        else:
            form = ImportForm()

        context = dict(self.admin_site.each_context(request), form=form)
        return TemplateResponse(request, "admin/tower/towerreward/import.html", context)
