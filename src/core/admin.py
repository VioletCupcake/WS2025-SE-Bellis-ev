
from django.contrib import admin
from core.models import GewalttatArt, FolgenDerGewalt
from core.models import StatistikPreset

@admin.register(GewalttatArt)
class GewalttatArtAdmin(admin.ModelAdmin):
    list_display = ['name', 'ist_unterkategorie', 'hauptkategorie']
    search_fields = ['name']

@admin.register(FolgenDerGewalt)  
class FolgenDerGewaltAdmin(admin.ModelAdmin):
    list_display = ['name', 'kategorie', 'ist_unterkategorie']
    list_filter = ['kategorie']


@admin.register(StatistikPreset)
class StatistikPresetAdmin(admin.ModelAdmin):
    list_display = ["name", "ist_global", "ist_system_preset", "erstellt_von", "erstellungsdatum"]
    list_filter = ["ist_global", "ist_system_preset"]
    search_fields = ["name"]
