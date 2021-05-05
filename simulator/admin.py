from django.contrib import admin

from simulator.models import Houseguest, Game

# Register your models here.
class HouseguestAdmin(admin.ModelAdmin):
    list_display = ('name',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Houseguest, HouseguestAdmin)
admin.site.register(Game, GameAdmin)
