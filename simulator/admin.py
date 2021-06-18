from django.contrib import admin

from simulator.models import (
    Contestant,
    Houseguest,
    Game,
)


# Register your models here.
class ContestantAdmin(admin.ModelAdmin):
    list_display = ("name",)


class HouseguestAdmin(admin.ModelAdmin):
    list_display = ("name",)


class GameAdmin(admin.ModelAdmin):
    list_display = ("id",)

class EvictionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "evicted",
    )


admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Houseguest, HouseguestAdmin)
admin.site.register(Game, GameAdmin)
