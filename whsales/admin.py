from django.contrib import admin
from whsales.models import Listing, Wormhole, System, Effect

admin.site.register(Listing)
admin.site.register(Effect)

@admin.register(Wormhole)
class WormholeAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination')

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'wormhole_class', 'id')
