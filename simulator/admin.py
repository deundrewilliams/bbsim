from django.contrib import admin

from simulator.models import (
    Contestant,
    Houseguest,
    Game,
    Week,
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

class WeekAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Houseguest, HouseguestAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Week, WeekAdmin)
