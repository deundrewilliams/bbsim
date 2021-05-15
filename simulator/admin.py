from django.contrib import admin

from simulator.models import *

# Register your models here.
class ContestantAdmin(admin.ModelAdmin):
    list_display = ('name',)

class HouseguestAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('id',)

class CompAdmin(admin.ModelAdmin):
    list_display = ('id', 'winner', )

class EvictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'evicted', )

class FinaleAdmin(admin.ModelAdmin):
    list_display = ('id',)

class NomCeremonyAdmin(admin.ModelAdmin):
    list_display = ('id',)

class VetoCeremonyAdmin(admin.ModelAdmin):
    list_display = ('id',)

class VetoPlayersAdmin(admin.ModelAdmin):
    list_display = ('id',)

class WeekAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Houseguest, HouseguestAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Competition, CompAdmin)
admin.site.register(EvictionCeremony, EvictionAdmin)
admin.site.register(Finale, FinaleAdmin)
admin.site.register(NominationCeremony, NomCeremonyAdmin)
admin.site.register(VetoCeremony, VetoCeremonyAdmin)
admin.site.register(VetoPlayers, VetoPlayersAdmin)
admin.site.register(Week, WeekAdmin)
