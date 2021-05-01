from django.contrib import admin

from simulator.models import Houseguest

# Register your models here.
class HouseguestAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Houseguest, HouseguestAdmin)
