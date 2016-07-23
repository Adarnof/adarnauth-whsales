from django.contrib import admin
from whsales.models import Listing, Wormhole, System, Effect

admin.site.register(Effect)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    search_fields = ['system__name', 'owner__character_name']

@admin.register(Wormhole)
class WormholeAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination')
    search_fields = ['name', 'destination']
    ordering = ['name']

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'wormhole_class', 'id')
    search_fields = ['name', 'id']
    ordering = ['name']
